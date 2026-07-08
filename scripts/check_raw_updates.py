#!/usr/bin/env python3
"""
Check .raw/ files against wiki/ to find files that need syncing.
Detects ALL file types (not just .md), with XMind-aware mapping.
"""
import os, re, sys
from datetime import datetime

RAW = '.raw'
WIKI = 'wiki'

# Tolerance: allow this many seconds difference (batch writes)
TOLERANCE = 120  # 2 min

# Files to skip (not wiki content)
SKIP_FILES = {'.gitkeep', '.manifest.json'}

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
}


def normalize_name(base: str) -> str:
    """Remove numbering prefix like '01-', '04-' from filename."""
    return re.sub(r'^\d{2}-', '', base)


def find_wiki(raw_rel: str) -> str | None:
    parts = raw_rel.replace(os.sep, '/').split('/')
    fname = parts[-1]
    base, ext = os.path.splitext(fname)

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


def should_skip(rel: str) -> bool:
    """Check if a raw file should be excluded from scanning."""
    fname = os.path.basename(rel)
    if fname in SKIP_FILES:
        return True
    if rel.startswith('assets/') or rel.startswith('screenshots/') or rel.startswith('data/') or rel.startswith('transcripts/'):
        return True
    if rel == 'claude-obsidian-ecosystem-research.md':
        return True
    if rel == '.gitkeep':
        return True
    if rel.endswith('.stackdump'):
        return True
    return False


def main():
    needs_update = []
    unlinked = []
    skipped = 0
    up_to_date = 0

    for root, dirs, files in os.walk(RAW):
        for f in files:
            raw_path = os.path.join(root, f)
            rel = os.path.relpath(raw_path, RAW).replace(os.sep, '/')

            if should_skip(rel):
                skipped += 1
                continue

            raw_mtime = os.path.getmtime(raw_path)
            wiki_path = find_wiki(rel)

            if wiki_path and os.path.isfile(wiki_path):
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

    print(f'■ 已同步（最新）({up_to_date})')
    print()

    print(f'■ 未映射到 wiki ({len(unlinked)})')
    if unlinked:
        for u in sorted(unlinked):
            print(f'  ❓ {u}')
    else:
        print('  ✅ 全部已映射')
    print()

    print(f'■ 已跳过（非文档文件）({skipped})')
    print()

    # Summary
    total = len(needs_update) + up_to_date + len(unlinked) + skipped
    status = '✅' if not needs_update else '⚠️'
    print(f'📊 总计扫描: {total} 个文件 | '
          f'待更新: {len(needs_update)} | '
          f'已同步: {up_to_date} | '
          f'未映射: {len(unlinked)} | '
          f'已跳过: {skipped}')
    print(f'{status} 扫描完成')

    return len(needs_update)


if __name__ == '__main__':
    code = main()
    sys.exit(code)
