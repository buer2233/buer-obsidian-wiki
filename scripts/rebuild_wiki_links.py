#!/usr/bin/env python3
"""Rebuild Obsidian wiki link indexes and graph-visible relationships."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
GRAPH = ROOT / ".obsidian" / "graph.json"
TODAY = date.today().isoformat()

AUTO_START = "<!-- AUTO-LINK-INDEX:START -->"
AUTO_END = "<!-- AUTO-LINK-INDEX:END -->"
CATALOG_START = "<!-- AUTO-CATALOG:START -->"
CATALOG_END = "<!-- AUTO-CATALOG:END -->"

EXCLUDED_FILENAMES = {
    "hot.md",
    "log.md",
    "overview.md",
    "dashboard.md",
}

STOPWORDS = {
    "index",
    "_index",
    "md",
    "and",
    "the",
    "with",
    "学习",
    "资料",
    "总结",
    "记录",
    "笔记",
    "基础",
    "入门",
    "使用",
    "问题",
    "整理",
}

TOPIC_KEYWORDS = [
    ("接口自动化", ["接口", "API", "pytest", "抓包", "用例", "Controller", "自动化"]),
    ("UI自动化", ["UI", "Appium", "移动端", "Web自动化", "browser-use"]),
    ("性能测试", ["性能", "Locust", "压测", "并发"]),
    ("测试平台", ["测试平台", "Django", "Flask", "Vue", "TypeScript", "DRF"]),
    ("云原生与运维", ["Docker", "Jenkins", "Linux", "MySQL", "CI/CD"]),
    ("AI测试", ["AI", "LLM", "RAG", "Agent", "大模型", "LangChain", "eval", "安全测试"]),
    ("Claude Code", ["Claude", "Codex", "SKILL", "Agent SDK", "Harness", "vibecoding"]),
    ("数据结构算法", ["数据结构", "算法", "设计模式"]),
    ("面试", ["面试", "八股文", "真实面试题"]),
    ("个人信息", ["个人档案", "邓万鹏", "简历", "名片"]),
]


@dataclass
class Note:
    path: Path
    rel: str
    stem: str
    target: str
    folder: str
    body: str
    frontmatter: str = ""
    title: str = ""
    links: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)
    topics: set[str] = field(default_factory=set)

    @property
    def is_index(self) -> bool:
        return self.path.name in {"index.md", "_index.md"}

    @property
    def is_meta(self) -> bool:
        return self.rel.startswith("元数据/") or self.path.name in EXCLUDED_FILENAMES

    @property
    def display(self) -> str:
        return self.title or self.stem


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5 :]
    return "", text


def title_from_frontmatter(frontmatter: str, fallback: str) -> str:
    match = re.search(r"(?m)^title:\s*[\"']?(.+?)[\"']?\s*$", frontmatter)
    return match.group(1).strip() if match else fallback


def tags_from_frontmatter(frontmatter: str) -> set[str]:
    tags: set[str] = set()
    in_tags = False
    for line in frontmatter.splitlines():
        if re.match(r"^tags:\s*$", line):
            in_tags = True
            continue
        if in_tags:
            if line.startswith("  - "):
                tags.add(line[4:].strip().strip("\"'"))
                continue
            if line and not line.startswith(" "):
                in_tags = False
        inline = re.match(r"^tags:\s*\[(.+)\]\s*$", line)
        if inline:
            tags.update(t.strip().strip("\"'") for t in inline.group(1).split(","))
    return {t for t in tags if t}


def wiki_target(path: Path) -> str:
    return path.relative_to(WIKI).with_suffix("").as_posix()


def extract_links(text: str) -> set[str]:
    links: set[str] = set()
    for raw in re.findall(r"!?\[\[([^\]]+)\]\]", text):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            links.add(target)
    return links


def strip_auto_sections(text: str) -> str:
    pattern = re.compile(r"\n?## 🔗 自动关联索引\n\n" + re.escape(AUTO_START) + r".*?" + re.escape(AUTO_END) + r"\n?", re.S)
    return pattern.sub("\n", text)


def tokenize(text: str) -> set[str]:
    tokens = set(re.findall(r"[A-Za-z][A-Za-z0-9+#.-]{1,}|[\u4e00-\u9fff]{2,}", text))
    return {t for t in tokens if t not in STOPWORDS and len(t) >= 2}


def detect_topics(text: str) -> set[str]:
    lowered = text.lower()
    topics = set()
    for topic, keys in TOPIC_KEYWORDS:
        for key in keys:
            if key.lower() in lowered:
                topics.add(topic)
                break
    return topics


def load_notes() -> list[Note]:
    notes: list[Note] = []
    for path in sorted(WIKI.rglob("*.md")):
        text = path.read_text(encoding="utf-8-sig")
        frontmatter, body = split_frontmatter(text)
        rel = path.relative_to(WIKI).as_posix()
        target = wiki_target(path)
        haystack = f"{rel}\n{frontmatter}\n{body[:5000]}"
        note = Note(
            path=path,
            rel=rel,
            stem=path.stem,
            target=target,
            folder=path.parent.relative_to(WIKI).as_posix() if path.parent != WIKI else "",
            body=body,
            frontmatter=frontmatter,
            title=title_from_frontmatter(frontmatter, path.stem),
            links=extract_links(text),
            tags=tags_from_frontmatter(frontmatter),
            topics=detect_topics(haystack),
        )
        notes.append(note)
    return notes


def resolve_links(notes: list[Note]) -> tuple[dict[str, Note], dict[str, list[Note]], dict[str, Note]]:
    by_target = {n.target: n for n in notes}
    by_stem: dict[str, list[Note]] = defaultdict(list)
    for note in notes:
        by_stem[note.stem].append(note)

    unique: dict[str, Note] = {}
    for stem, matches in by_stem.items():
        non_index = [m for m in matches if not m.is_index]
        if len(matches) == 1:
            unique[stem] = matches[0]
        elif len(non_index) == 1:
            unique[stem] = non_index[0]
    return by_target, by_stem, unique


def link_for(note: Note, by_stem: dict[str, list[Note]]) -> str:
    matches = by_stem.get(note.stem, [])
    if len(matches) == 1:
        return f"[[{note.stem}]]"
    return f"[[{note.target}|{note.stem}]]"


def resolve_target(target: str, by_target: dict[str, Note], unique: dict[str, Note]) -> Note | None:
    normalized = target.strip().strip("/")
    if normalized in by_target:
        return by_target[normalized]
    if normalized in unique:
        return unique[normalized]
    return None


def repair_target(target: str, notes: list[Note], by_target: dict[str, Note], unique: dict[str, Note]) -> str | None:
    normalized = target.strip().strip("/")
    if not normalized:
        return None
    if normalized in by_target or normalized in unique:
        return None

    # Links to generated canvas files are valid Obsidian links, even though they
    # are not Markdown notes and therefore are not in the note map.
    if (WIKI / normalized).exists() or (WIKI / f"{normalized}.canvas").exists():
        return None

    folder_index = WIKI / normalized / "index.md"
    folder_underscore_index = WIKI / normalized / "_index.md"
    if folder_index.exists():
        return f"{normalized}/index"
    if folder_underscore_index.exists():
        return f"{normalized}/_index"

    suffix_matches = [note.target for note in notes if note.target.endswith(f"/{normalized}")]
    if len(suffix_matches) == 1:
        return suffix_matches[0]

    stem = normalized.rsplit("/", 1)[-1]
    stem_matches = [note.target for note in notes if note.stem == stem and not note.is_index]
    if len(stem_matches) == 1:
        return stem_matches[0]

    index_name_matches = [
        note.target
        for note in notes
        if note.is_index and (note.title == normalized or note.stem == normalized)
    ]
    if len(index_name_matches) == 1:
        return index_name_matches[0]

    return None


def repair_dead_wikilinks(notes: list[Note], by_target: dict[str, Note], unique: dict[str, Note], dry_run: bool) -> int:
    changed = 0
    link_pattern = re.compile(r"(!?)\[\[([^\]]+)\]\]")

    for note in notes:
        if note.rel.startswith("元数据/lint-report-"):
            continue
        text = note.path.read_text(encoding="utf-8-sig")
        replacements = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal replacements
            prefix, raw = match.group(1), match.group(2)
            target_and_heading, alias = (raw.split("|", 1) + [None])[:2] if "|" in raw else (raw, None)
            target, heading = (target_and_heading.split("#", 1) + [None])[:2] if "#" in target_and_heading else (target_and_heading, None)
            repaired = repair_target(target, notes, by_target, unique)
            if not repaired:
                return match.group(0)
            replacements += 1
            rebuilt = repaired
            if heading:
                rebuilt += f"#{heading}"
            if alias:
                rebuilt += f"|{alias}"
            return f"{prefix}[[{rebuilt}]]"

        new_text = link_pattern.sub(replace, text)
        if replacements and new_text != text:
            changed += 1
            if not dry_run:
                note.path.write_text(new_text, encoding="utf-8", newline="\n")
    return changed


def relation_reason(a: Note, b: Note) -> str:
    shared_topics = sorted(a.topics & b.topics)
    if shared_topics:
        return f"{shared_topics[0]}主题关联"
    if a.folder and a.folder == b.folder:
        return "同目录知识群"
    if a.tags & b.tags:
        return "标签关联"
    return "内容关键词关联"


def build_relations(notes: list[Note], by_target: dict[str, Note], unique: dict[str, Note]) -> dict[str, list[tuple[Note, str]]]:
    content_notes = [n for n in notes if not n.is_meta and not n.is_index]
    clean_bodies = {n.rel: strip_auto_sections(n.body) for n in content_notes}
    manual_links = {n.rel: extract_links(n.frontmatter + "\n" + clean_bodies[n.rel]) for n in content_notes}
    tokens = {n.rel: tokenize(f"{n.target} {n.title} {clean_bodies[n.rel][:3000]} {' '.join(n.tags)} {' '.join(n.topics)}") for n in content_notes}
    relations: dict[str, list[tuple[Note, str]]] = {}

    content_by_rel = {n.rel: n for n in content_notes}

    for note in content_notes:
        scores: Counter[str] = Counter()

        for target in manual_links[note.rel]:
            other = resolve_target(target, by_target, unique)
            if other and other.rel != note.rel and other.rel in content_by_rel:
                scores[other.rel] += 8

        for other in content_notes:
            if other.rel == note.rel:
                continue
            if note.folder and note.folder == other.folder:
                scores[other.rel] += 5
            if note.topics & other.topics:
                scores[other.rel] += 4 * len(note.topics & other.topics)
            if note.tags & other.tags:
                scores[other.rel] += 3 * len(note.tags & other.tags)
            shared = tokens[note.rel] & tokens[other.rel]
            if shared:
                scores[other.rel] += min(4, len(shared))
            if other.stem in clean_bodies[note.rel]:
                scores[other.rel] += 6

        ranked_items = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        ranked = [(content_by_rel[rel], score) for rel, score in ranked_items if score >= 5 and rel in content_by_rel][:8]
        relations[note.rel] = [(other, relation_reason(note, other)) for other, _ in ranked]

    # Make relation graph symmetric for the strongest edges.
    rel_sets: dict[str, dict[str, str]] = {
        rel: {other.rel: reason for other, reason in items}
        for rel, items in relations.items()
    }
    note_by_rel = {n.rel: n for n in content_notes}
    for rel, items in list(rel_sets.items()):
        for other_rel, reason in list(items.items())[:5]:
            rel_sets.setdefault(other_rel, {})
            if rel not in rel_sets[other_rel] and len(rel_sets[other_rel]) < 8:
                rel_sets[other_rel][rel] = reason

    return {
        rel: [(note_by_rel[other_rel], reason) for other_rel, reason in items.items()]
        for rel, items in rel_sets.items()
    }


def generated_related_block(note: Note, relations: list[tuple[Note, str]], by_stem: dict[str, list[Note]]) -> str:
    lines = ["## 🔗 自动关联索引", "", AUTO_START]
    if relations:
        for other, reason in relations:
            lines.append(f"- {link_for(other, by_stem)} — {reason}")
    else:
        lines.append("- 暂无自动发现的强关联页面。")
    lines.extend([AUTO_END, ""])
    return "\n".join(lines)


def update_note_related_sections(notes: list[Note], relations: dict[str, list[tuple[Note, str]]], by_stem: dict[str, list[Note]], dry_run: bool) -> int:
    changed = 0
    for note in notes:
        if note.is_meta or note.is_index or note.path.name in {"overview.md"}:
            continue
        text = note.path.read_text(encoding="utf-8-sig")
        text = strip_auto_sections(text).rstrip() + "\n\n"
        block = generated_related_block(note, relations.get(note.rel, []), by_stem)
        new_text = text + block
        if new_text != note.path.read_text(encoding="utf-8-sig"):
            changed += 1
            if not dry_run:
                note.path.write_text(new_text, encoding="utf-8", newline="\n")
    return changed


def folder_title(folder: str) -> str:
    return folder.split("/")[-1] if folder else "知识库"


def index_frontmatter(title: str) -> str:
    return f"---\ntype: index\ntitle: \"{title}\"\ncreated: {TODAY}\nupdated: {TODAY}\ntags:\n  - wiki/index\nstatus: active\n---\n\n"


def update_folder_indexes(notes: list[Note], by_stem: dict[str, list[Note]], dry_run: bool) -> int:
    changed = 0
    by_folder: dict[str, list[Note]] = defaultdict(list)
    for note in notes:
        if note.folder and not note.is_meta and not note.is_index:
            by_folder[note.folder].append(note)

    for folder, items in sorted(by_folder.items()):
        folder_path = WIKI / folder
        index_path = folder_path / "index.md"
        if not index_path.exists() and (folder_path / "_index.md").exists():
            index_path = folder_path / "_index.md"
        title = f"{folder_title(folder)}索引"
        existing = index_path.read_text(encoding="utf-8-sig") if index_path.exists() else index_frontmatter(title) + f"# {title}\n\n"
        block_lines = [CATALOG_START, f"\n## 自动页面目录\n"]
        for item in sorted(items, key=lambda n: n.stem):
            block_lines.append(f"- {link_for(item, by_stem)} — {item.display}")
        block_lines.extend(["", CATALOG_END, ""])
        block = "\n".join(block_lines)
        if CATALOG_START in existing and CATALOG_END in existing:
            new_text = re.sub(re.escape(CATALOG_START) + r".*?" + re.escape(CATALOG_END), block.rstrip(), existing, flags=re.S)
        else:
            new_text = existing.rstrip() + "\n\n" + block
        if new_text != existing:
            changed += 1
            if not dry_run:
                index_path.write_text(new_text, encoding="utf-8", newline="\n")
    return changed


def update_root_index(notes: list[Note], by_stem: dict[str, list[Note]], dry_run: bool) -> bool:
    path = WIKI / "index.md"
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"(?m)^updated:\s*.+$", f"updated: {TODAY}", text)
    by_folder: dict[str, list[Note]] = defaultdict(list)
    for note in notes:
        if note.path.name == "index.md" and note.folder == "":
            continue
        if note.path.name in {"hot.md", "log.md"}:
            continue
        by_folder[note.folder or "根目录"].append(note)

    lines = [CATALOG_START, "\n## 全量页面索引\n"]
    for folder, items in sorted(by_folder.items()):
        lines.append(f"### {folder}")
        for item in sorted(items, key=lambda n: n.stem):
            lines.append(f"- {link_for(item, by_stem)}")
        lines.append("")
    lines.append(CATALOG_END)
    block = "\n".join(lines)
    if CATALOG_START in text and CATALOG_END in text:
        new_text = re.sub(re.escape(CATALOG_START) + r".*?" + re.escape(CATALOG_END), block, text, flags=re.S)
    else:
        new_text = text.rstrip() + "\n\n" + block + "\n"
    if new_text != path.read_text(encoding="utf-8-sig"):
        if not dry_run:
            path.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False


def graph_color(folder: str, index: int) -> int:
    palette = [
        0x3366CC,
        0xDC3912,
        0xFF9900,
        0x109618,
        0x990099,
        0x0099C6,
        0xDD4477,
        0x66AA00,
        0xB82E2E,
        0x316395,
    ]
    return palette[index % len(palette)]


def update_graph(notes: list[Note], dry_run: bool) -> bool:
    data = json.loads(GRAPH.read_text(encoding="utf-8-sig"))
    data["search"] = "path:wiki"
    data["hideUnresolved"] = True
    data["showOrphans"] = False
    data["showArrow"] = True
    groups = data.get("colorGroups", [])
    normalized = []
    seen = set()
    for group in groups:
        query = group.get("query", "").rstrip()
        if query == "path:wiki/语雀  ":
            query = "path:wiki/语雀"
        key = query
        if key and key not in seen:
            new_group = dict(group)
            new_group["query"] = query
            normalized.append(new_group)
            seen.add(key)

    top_folders = sorted({n.folder.split("/", 1)[0] for n in notes if n.folder})
    for idx, folder in enumerate(top_folders):
        query = f"path:wiki/{folder}"
        if query not in seen:
            normalized.append({"query": query, "color": {"a": 1, "rgb": graph_color(folder, idx)}})
            seen.add(query)

    data["colorGroups"] = normalized
    new_text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if new_text != GRAPH.read_text(encoding="utf-8-sig"):
        if not dry_run:
            GRAPH.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False


def write_dashboard(notes: list[Note], dead_links: list[tuple[str, str]], orphans: list[Note], dry_run: bool) -> bool:
    path = WIKI / "元数据" / "dashboard.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"""---
type: meta
title: "知识库仪表盘"
updated: {TODAY}
tags:
  - meta/dashboard
status: active
---

# 知识库仪表盘

## 链接健康
- 页面总数：{len(notes)}
- 待处理死链：{len(dead_links)}
- 无入链页面：{len(orphans)}

## 最近活动
```dataview
TABLE type, status, updated FROM "wiki" SORT updated DESC LIMIT 15
```

## 自动索引入口
- [[index|索引]]
- [[语雀/index|语雀索引]]
- [[软件测试学习资料/index|软件测试学习资料索引]]
- [[软件测试学习资料-XMind/index|软件测试学习资料-XMind索引]]
- [[面试题/index|面试题索引]]
- [[个人信息/index|个人信息索引]]

## 待复核页面
```dataview
LIST FROM "wiki" WHERE status = "seed" SORT updated ASC
```
"""
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if text != existing:
        if not dry_run:
            path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def write_lint_report(notes: list[Note], dead_links: list[tuple[str, str]], orphans: list[Note], dry_run: bool) -> bool:
    path = WIKI / "元数据" / f"lint-report-{TODAY}.md"
    dead_lines = "\n".join(f"- `{target}` referenced in [[{source}]]" for source, target in dead_links[:100]) or "- 无"
    orphan_lines = "\n".join(f"- [[{note.target}|{note.stem}]]: no inbound links before/after generated index review." for note in orphans[:100]) or "- 无"
    text = f"""---
type: meta
title: "Lint Report {TODAY}"
created: {TODAY}
updated: {TODAY}
tags:
  - meta
  - lint
status: developing
---

# Lint Report: {TODAY}

## Summary
- Pages scanned: {len(notes)}
- Dead links found: {len(dead_links)}
- Orphan pages found: {len(orphans)}
- Auto-fixed: generated folder indexes, root catalog, and page-level automatic relation sections.
- Needs review: dead links below may be aliases, renamed notes, or intentionally unresolved future pages.

## Orphan Pages
{orphan_lines}

## Dead Links
{dead_lines}

## Cross-Reference Work Completed
- Added `## 🔗 自动关联索引` managed sections to content pages.
- Added or refreshed folder-level `index.md` / `_index.md` catalogs.
- Refreshed [[index|索引]] with a full-page catalog.
- Updated [[元数据/dashboard]] for graph and Dataview entry points.
"""
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if text != existing:
        if not dry_run:
            path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def write_canvas(notes: list[Note], relations: dict[str, list[tuple[Note, str]]], dry_run: bool) -> bool:
    path = WIKI / "元数据" / "overview.canvas"
    top_folders = sorted({n.folder.split("/", 1)[0] for n in notes if n.folder})
    nodes = []
    edges = []
    nodes.append({"id": "root", "type": "file", "file": "wiki/index.md", "x": 0, "y": 0, "width": 320, "height": 140, "color": "1"})
    for idx, folder in enumerate(top_folders):
        index_file = WIKI / folder / "index.md"
        if not index_file.exists():
            index_file = WIKI / folder / "_index.md"
        if index_file.exists():
            node_id = f"folder-{idx}"
            nodes.append({
                "id": node_id,
                "type": "file",
                "file": index_file.relative_to(ROOT).as_posix(),
                "x": (idx % 4) * 380 - 570,
                "y": math.floor(idx / 4) * 220 + 240,
                "width": 320,
                "height": 140,
                "color": str((idx % 6) + 1),
            })
            edges.append({"id": f"edge-root-{idx}", "fromNode": "root", "toNode": node_id})

    data = {"nodes": nodes, "edges": edges}
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if text != existing:
        if not dry_run:
            path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def append_log(dry_run: bool) -> bool:
    path = WIKI / "log.md"
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    entry = f"""## {TODAY} - 重建 Wiki 链接索引

- 扫描 `wiki/` 全部 Markdown 页面。
- 刷新主索引、目录索引、页面级自动关联索引。
- 更新 Obsidian 图谱颜色分组、仪表盘和概览 Canvas。
- 生成 `[[元数据/lint-report-{TODAY}|链接健康报告]]`。

"""
    if entry in existing:
        return False
    if not dry_run:
        path.write_text(entry + existing, encoding="utf-8", newline="\n")
    return True


def update_hot(dry_run: bool) -> bool:
    path = WIKI / "hot.md"
    text = f"""---
type: meta
title: "热缓存"
created: 2026-07-01
updated: {TODAY}
---

# 最近上下文

## 最后更新
{TODAY} — 重建当前 Wiki 的链接索引与图谱关系。

## 关键事实
- `wiki/` 已完成全量页面扫描，并刷新主索引、目录索引与页面级自动关联索引。
- 页面之间新增 `## 🔗 自动关联索引` 托管段落，用 Obsidian wikilink 暴露关联关系。
- Obsidian 图谱配置已保持 `path:wiki` 视图，并补齐顶层目录颜色分组。

## 最近变更
- 更新：[[index|索引]]、[[元数据/dashboard]]、[[元数据/lint-report-{TODAY}]]
- 更新：各目录 `index.md` / `_index.md` 自动页面目录
- 创建/更新：[[元数据/overview.canvas]]

## 活跃线程
- 当前任务：Wiki 关系图谱维护与链接健康检查。
- 后续建议：人工复核 lint 报告中的死链，确认是否需要创建别名页或修正旧链接。
"""
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if text != existing:
        if not dry_run:
            path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def graph_stats(notes: list[Note], by_target: dict[str, Note], unique: dict[str, Note]) -> tuple[list[tuple[str, str]], list[Note]]:
    inbound: Counter[str] = Counter()
    dead_links: list[tuple[str, str]] = []
    for note in notes:
        for target in note.links:
            other = resolve_target(target, by_target, unique)
            if other:
                inbound[other.rel] += 1
            elif (WIKI / target).exists() or (WIKI / f"{target}.canvas").exists():
                continue
            elif not target.startswith(("http://", "https://")):
                dead_links.append((note.target, target))
    orphans = [
        n for n in notes
        if inbound[n.rel] == 0 and not n.is_meta and n.path.name not in {"index.md"}
    ]
    return dead_links, orphans


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    notes = load_notes()
    by_target, by_stem, unique = resolve_links(notes)
    repaired_links = repair_dead_wikilinks(notes, by_target, unique, args.dry_run)

    if repaired_links and not args.dry_run:
        notes = load_notes()
        by_target, by_stem, unique = resolve_links(notes)

    dead_before, orphans_before = graph_stats(notes, by_target, unique)
    relations = build_relations(notes, by_target, unique)

    changes = {
        "related_sections": update_note_related_sections(notes, relations, by_stem, args.dry_run),
        "repaired_dead_link_files": repaired_links,
        "folder_indexes": update_folder_indexes(notes, by_stem, args.dry_run),
        "root_index": update_root_index(notes, by_stem, args.dry_run),
        "graph": update_graph(notes, args.dry_run),
        "canvas": write_canvas(notes, relations, args.dry_run),
        "log": append_log(args.dry_run),
        "hot": update_hot(args.dry_run),
    }

    if not args.dry_run:
        notes_after = load_notes()
        by_target_after, _, unique_after = resolve_links(notes_after)
        dead_after, orphans_after = graph_stats(notes_after, by_target_after, unique_after)
    else:
        notes_after = notes
        dead_after, orphans_after = dead_before, orphans_before

    changes["dashboard"] = write_dashboard(notes_after, dead_after, orphans_after, args.dry_run)
    changes["lint_report"] = write_lint_report(notes_after, dead_after, orphans_after, args.dry_run)

    print(json.dumps({
        "pages": len(notes),
        "dead_links_before": len(dead_before),
        "orphans_before": len(orphans_before),
        "dead_links_after": len(dead_after),
        "orphans_after": len(orphans_after),
        "changes": changes,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
