#!/usr/bin/env python3
"""
Check .raw/ files against wiki/ to find files that need syncing.
Detects ALL file types (not just .md), with XMind-aware mapping.
"""
import os, re, sys
from datetime import datetime

# Windows consoles default to a legacy code page (GBK/cp936) that cannot encode
# the emoji in this report, so a plain `python scripts/check_raw_updates.py`
# dies with UnicodeEncodeError before printing anything useful.
try:
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]
except Exception:
    pass

RAW = '.raw'
WIKI = 'wiki'

# Tolerance: allow this many seconds difference (batch writes)
TOLERANCE = 120  # 2 min

# Files to skip (not wiki content)
SKIP_FILES = {'.gitkeep', '.manifest.json'}

# Directories holding URL-ingest scratch material rather than vault content.
# Files here are REPORTED as exclusions — never dropped from the report, since
# content that vanishes from the report is content nobody notices is missing.
SCRATCH_DIRS = ('assets/', 'screenshots/', 'data/', 'transcripts/')

# Image/media extensions. These are attachments: they count as "in the wiki"
# only when some wiki page actually embeds their _attachments/ copy. That
# catches both directions of drift — an image never copied, and an image
# copied but referenced by nobody (a silent orphan attachment).
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.avif'}
ATTACHMENTS = '_attachments'

_referenced_cache: set[str] | None = None

# XMind prefix-to-wiki-name mapping
XMINDI_MAP = {
    '01-': '计算机基础总结',
    '02-': '测试理论总结',
    '03-': '禅道与移动端测试',
    '04-': 'Linux总结',
    '05-': 'MySQL总结',
    '06-': 'Python基础总结',
    '07-': 'Python高级总结',
    '08-': 'Web自动化总结',
    '09-': '接口自动化总结',
    '10-': 'APP测试',
    '11-': 'DRF框架基础总结',
}

# Special filename rewrites (raw -> wiki name, no extension)
FILENAME_MAP = {
    'flask平台代码简介(泛微)': 'flask平台代码简介',
    'Django 学习笔记': 'Django 学习笔记',
    '邓万鹏-AI自动化测试-18584874420': '邓万鹏-AI自动化测试',
    'claude-obsidian-ecosystem-research': 'claude-obsidian生态调研',
}


def normalize_name(base: str) -> str:
    """Remove numbering prefix like '01-', '04-' from filename."""
    return re.sub(r'^\d{2}-', '', base)


def referenced_attachments() -> set[str]:
    """Every _attachments/ path mentioned by any wiki page (built once)."""
    global _referenced_cache
    if _referenced_cache is None:
        refs: set[str] = set()
        for root, _dirs, files in os.walk(WIKI):
            for f in files:
                if not f.endswith('.md'):
                    continue
                try:
                    text = open(os.path.join(root, f), encoding='utf-8-sig').read()
                except OSError:
                    continue
                for m in re.findall(r'_attachments/[^)\]\s"\'<>]+', text):
                    refs.add(m)
        _referenced_cache = refs
    return _referenced_cache


def attachment_paths(raw_rel: str) -> list[str]:
    """Where a raw file's copy under _attachments/ would live.

    .raw/<cat>/images/<sub>/<file>  -> _attachments/images/<cat>/<sub>/<file>
    .raw/<cat>/<file>               -> _attachments/images/<cat>/<file>
    """
    parts = raw_rel.replace(os.sep, '/').split('/')
    if len(parts) >= 3 and parts[1] == 'images':
        tail = parts[2:]
    elif len(parts) >= 2:
        tail = [parts[-1]]
    else:
        return []
    # Build with forward slashes: wiki pages embed `_attachments/...`, and on
    # Windows os.path.join would yield backslashes that never string-match.
    return ['/'.join((ATTACHMENTS, 'images', parts[0], *tail))]


def find_wiki(raw_rel: str) -> str | None:
    parts = raw_rel.replace(os.sep, '/').split('/')
    fname = parts[-1]
    base, ext = os.path.splitext(fname)

    # 0. Attachments: mapped iff a wiki page embeds the _attachments/ copy.
    #    Not referenced -> fall through to the rules below, so a raw image that
    #    has its own 1:1 wiki page still maps (e.g. .raw/学习简图/x.png).
    if ext.lower() in IMAGE_EXTS:
        refs = referenced_attachments()
        for candidate in attachment_paths(raw_rel):
            if candidate in refs:
                return candidate

    # 1. Skip non-content files
    if fname in SKIP_FILES:
        return None

    # 2. XMind files in 软件测试学习资料-XMind/
    for prefix, wiki_name in XMINDI_MAP.items():
        if fname.startswith(prefix) and ext == '.xmind':
            wiki_path = os.path.join(WIKI, '软件测试学习资料-XMind', wiki_name + '.md')
            if os.path.isfile(wiki_path):
                return wiki_path

    # 3. yuque .md files -> wiki/语雀/
    if ext == '.md' and parts[0] == 'yuque':
        target_base = normalize_name(base)
        # Check special name map
        if base in FILENAME_MAP:
            target_base = FILENAME_MAP[base]
        target = target_base + '.md'
        yq_dir = os.path.join(WIKI, '语雀')
        for r2, d2, f2 in os.walk(yq_dir):
            if target in f2:
                return os.path.join(r2, target)

    # 4. Direct same-path mapping (Codex/, 笔记/)
    wiki_path = os.path.join(WIKI, raw_rel.replace(ext, '.md'))
    if os.path.isfile(wiki_path):
        return wiki_path

    # 4b. Basename fallback within the same top-level category.
    #     The vault does not always mirror raw subdirectories 1:1: raw content
    #     under a subdir is sometimes flattened into the category root
    #     (e.g. .raw/X/pi/Foo.md -> wiki/X/Foo.md). Without this rule those
    #     files are reported as "未映射" forever even though they ARE ingested.
    if len(parts) > 1:
        target_name = base + '.md'
        cat_dir = os.path.join(WIKI, parts[0])
        if os.path.isdir(cat_dir):
            for r2, d2, f2 in os.walk(cat_dir):
                if target_name in f2:
                    return os.path.join(r2, target_name)

    # 5. 软件测试学习资料-XMind .md / .txt (no prefix numbering)
    if parts[0] == '软件测试学习资料-XMind':
        target_base = normalize_name(base)
        for r2, d2, f2 in os.walk(os.path.join(WIKI, '软件测试学习资料-XMind')):
            md_candidates = [x for x in f2 if x.endswith('.md')
                             and (x.startswith(target_base) or x == target_base + '.md'
                                  or normalize_name(x.replace('.md', '')) == target_base)]
            if md_candidates:
                return os.path.join(r2, md_candidates[0])

    # 6. Check FILENAME_MAP as fallback
    if base in FILENAME_MAP:
        target = FILENAME_MAP[base] + '.md'
        wiki_parent = os.path.join(WIKI, parts[0])
        # A raw file at the .raw/ root has no category directory to scope the
        # search to, so fall back to the whole wiki. Without this, a root-level
        # source could never be mapped via FILENAME_MAP.
        if not os.path.isdir(wiki_parent):
            wiki_parent = WIKI
        if os.path.isfile(os.path.join(wiki_parent, target)):
            return os.path.join(wiki_parent, target)
        # Search one level deeper
        for r2, d2, f2 in os.walk(wiki_parent):
            if target in f2:
                return os.path.join(r2, target)

    # 7. 面试题/ files
    if parts[0] == '面试题':
        sdir = os.path.join(WIKI, '软件测试学习资料-XMind')
        target_base = normalize_name(base)
        for r2, d2, f2 in os.walk(sdir):
            for ff in f2:
                if ff.endswith('.md') and (target_base in ff or normalize_name(ff.replace('.md', '')) in target_base):
                    return os.path.join(r2, ff)

    return None


def exclusion_reason(rel: str) -> str | None:
    """Why this raw file is out of the wiki's scope — or None if it is in scope.

    Every scanned file must land in a VISIBLE bucket. A previous version of this
    script also hard-coded ``claude-obsidian-ecosystem-research.md`` as skipped;
    because skipped files appear in neither "已同步" nor "未映射", that content
    silently fell outside every report and never got a wiki page. Nothing that
    holds content may be excluded without saying so.
    """
    fname = os.path.basename(rel)
    if fname in SKIP_FILES:
        return '元数据文件（非内容）'
    if fname == '.gitkeep':
        return '占位文件'
    if rel.endswith('.stackdump'):
        return '崩溃转储'
    if any(rel.startswith(d) for d in SCRATCH_DIRS):
        return 'URL 抓取暂存目录（非 vault 内容）'
    return None


def main():
    needs_update = []
    unlinked = []
    excluded = []       # (rel, reason) — visible, never silent
    up_to_date = 0      # prose pages
    attached = []       # images embedded by a wiki page

    for root, dirs, files in os.walk(RAW):
        for f in files:
            raw_path = os.path.join(root, f)
            rel = os.path.relpath(raw_path, RAW).replace(os.sep, '/')

            reason = exclusion_reason(rel)
            if reason:
                excluded.append((rel, reason))
                continue

            raw_mtime = os.path.getmtime(raw_path)
            wiki_path = find_wiki(rel)

            if wiki_path and os.path.isfile(wiki_path):
                # An image counts as filed when a wiki page embeds its copy.
                if os.path.splitext(f)[1].lower() in IMAGE_EXTS and \
                        wiki_path.replace(os.sep, '/').startswith(ATTACHMENTS + '/'):
                    attached.append((rel, os.path.relpath(wiki_path)))
                    continue
                wiki_mtime = os.path.getmtime(wiki_path)
                diff = raw_mtime - wiki_mtime
                if diff > TOLERANCE:
                    rd = datetime.fromtimestamp(raw_mtime).strftime('%m-%d %H:%M')
                    wd = datetime.fromtimestamp(wiki_mtime).strftime('%m-%d %H:%M')
                    needs_update.append((rel, rd, os.path.relpath(wiki_path), wd, int(diff)))
                else:
                    up_to_date += 1
            else:
                unlinked.append(rel)

    print('=' * 60)
    print(f'Raw → Wiki 同步检查')
    print(f'容差: {TOLERANCE}s')
    print('=' * 60)
    print()

    print(f'■ 待更新文件 ({len(needs_update)})')
    if needs_update:
        for rel, rd, wp, wd, sec in sorted(needs_update, key=lambda x: -x[4]):
            print(f'  🔴 {rel}')
            print(f'     raw: {rd}  →  wiki: {wp} ({wd})  [差距 {sec}s]')
    else:
        print('  ✅ 无，所有 raw 文件与 wiki 保持同步')
    print()

    print(f'■ 已同步的正文页面 ({up_to_date})')
    print()

    print(f'■ 图片素材（已被 wiki 页嵌入引用）({len(attached)})')
    print('  （图片不单独建页——它们的 wiki 归属就是引用它们的那篇页面）')
    for rel, wp in sorted(attached)[:10]:
        print(f'  🖼️ {rel}')
        print(f'     → {wp}')
    if len(attached) > 10:
        print(f'  … 其余 {len(attached) - 10} 个同类')
    print()

    print(f'■ 未映射到 wiki ({len(unlinked)})')
    if unlinked:
        for u in sorted(unlinked):
            print(f'  ❓ {u}')
    else:
        print('  ✅ 全部已映射')
    print()

    print(f'■ 已排除（显式列出，非静默跳过）({len(excluded)})')
    for rel, reason in sorted(excluded):
        print(f'  ⏭️ {rel}  —  {reason}')
    print()

    # Summary
    total = (len(needs_update) + up_to_date + len(attached)
             + len(unlinked) + len(excluded))
    status = '✅' if not needs_update and not unlinked else '⚠️'
    print(f'📊 总计扫描: {total} 个文件 | '
          f'待更新: {len(needs_update)} | '
          f'已同步: {up_to_date} | '
          f'图片: {len(attached)} | '
          f'未映射: {len(unlinked)} | '
          f'已排除: {len(excluded)}')
    print(f'{status} 扫描完成')

    # Non-zero when content is unaccounted for, so a caller can gate on it.
    return len(needs_update) + len(unlinked)


if __name__ == '__main__':
    code = main()
    sys.exit(code)
