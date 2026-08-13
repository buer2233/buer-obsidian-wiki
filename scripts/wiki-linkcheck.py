#!/usr/bin/env python3
"""wiki-linkcheck.py — Obsidian wikilink 图谱与健康检查工具

用法:
  python scripts/wiki-linkcheck.py scan                 # 全库扫描：节点/链接/枢纽/孤儿/断链/歧义
  python scripts/wiki-linkcheck.py file <vault相对路径>   # 单文件检查：逐条链接解析状态

约定:
  - vault 根 = 本项目根目录（.obsidian 所在处）
  - 路径式链接 [[a/b/X]] 按 vault 根路径解析（须存在 a/b/X.md）
  - basename 链接 [[X]] 按文件名解析；同名 >1 视为歧义
"""
import os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")
RAW = os.path.join(ROOT, ".raw")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def norm_target(inner):
    return inner.split("|")[0].split("#")[0].strip()


def index_vault():
    files = []
    for base in (WIKI, RAW):
        for r, _, fs in os.walk(base):
            for f in fs:
                if f.endswith(".md"):
                    rel = os.path.relpath(os.path.join(r, f), ROOT).replace("\\", "/")
                    files.append(rel)
    pathset = set(os.path.splitext(r)[0] for r in files)
    bare = defaultdict(list)
    for r in files:
        bare[os.path.splitext(os.path.basename(r))[0]].append(r)
    return files, pathset, bare


def links_in(rel):
    try:
        txt = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    except Exception:
        return []
    return [norm_target(m) for m in LINK_RE.findall(txt)]


def resolve(target, pathset, bare):
    if "/" in target:
        return ("resolved" if target in pathset else "broken", target)
    n = len(bare.get(target, []))
    if n == 0:
        return ("broken", "无同名文件")
    if n > 1:
        return ("ambiguous", f"{n} 个同名: {bare[target]}")
    return ("resolved", bare[target][0])


def cmd_scan():
    files, pathset, bare = index_vault()
    outlinks = {r: links_in(r) for r in files}
    total = sum(len(v) for v in outlinks.values())
    print(f"笔记文件总数: {len(files)}")
    print(f"wikilink 总数: {total}")
    deg = {}
    for r in files:
        b = os.path.splitext(os.path.basename(r))[0]
        ins = sum(1 for v in outlinks.values() if b in v)
        deg[r] = ins + len(outlinks[r])
    print("\n连接度 Top 15:")
    for r, d in sorted(deg.items(), key=lambda x: -x[1])[:15]:
        print(f"  {d:3d}  {r}")
    orphans = [r for r in files if not outlinks[r] and not any(
        os.path.splitext(os.path.basename(r))[0] in v for v in outlinks.values())]
    print(f"\n孤儿页(无入链无出链): {len(orphans)}")
    for o in orphans[:25]:
        print(f"  {o}")
    broken, amb = set(), set()
    for targets in outlinks.values():
        for t in targets:
            st, _ = resolve(t, pathset, bare)
            if st == "broken":
                broken.add(t)
            elif st == "ambiguous":
                amb.add(t)
    print(f"\n断链(路径式解析失败, 去重): {len(broken)}")
    for b in sorted(broken)[:40]:
        print(f"  X  [[{b}]]")
    print(f"\nbasename 歧义(同名>1, 去重): {len(amb)}")
    for a in sorted(amb)[:40]:
        print(f"  ~  [[{a}]]")


def cmd_file(rel):
    _, pathset, bare = index_vault()
    targets = links_in(rel)
    print(f"{rel}  共 {len(targets)} 条 wikilink")
    br = am = rs = 0
    for t in targets:
        st, det = resolve(t, pathset, bare)
        if st == "broken":
            br += 1; mark = "X"
        elif st == "ambiguous":
            am += 1; mark = "~"
        else:
            rs += 1; mark = " "
        print(f"  {mark} [[{t}]]  -- {st}: {det}")
    print(f"\n解析成功 {rs} / 断链 {br} / 歧义 {am}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if mode == "file" and len(sys.argv) > 2:
        cmd_file(sys.argv[2])
    else:
        cmd_scan()
