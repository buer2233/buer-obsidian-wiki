# Wiki Link Rebuild Findings

## Initial Context

- Repository root: `D:\AI\Hermes\claude-obsidian`
- Wiki root: `wiki/`
- Current wiki page count from PowerShell: 107 Markdown files.
- Project rule: `.raw/` is immutable source material; generated knowledge lives in `wiki/`.
- Project rule: update index pages and establish bidirectional wikilinks so Obsidian Graph reflects relationships.

## Skill Notes

- `wiki` skill requires updating index, log, and hot cache after meaningful wiki operations.
- `wiki-lint` focuses on orphans, dead links, missing cross-references, stale index entries, dashboards, and canvas maps.
- `obsidian-markdown` requires exact wikilink filename matching; path links should be used when filenames are ambiguous.

## Early Observations

- Existing wiki already contains many `related:` frontmatter entries and `## 🔗 关联文档` sections.
- `wiki/index.md` has a large manual catalog but likely does not cover every page after recent imports.
- Obsidian graph visibility depends on body wikilinks and YAML wikilinks; generated relation sections are the safest visible path.

## Dry-Run Analysis

- `scripts/rebuild_wiki_links.py --dry-run` scanned 107 pages.
- Planned generated relation sections: 85 content pages.
- Planned folder index refreshes: 17 directories.
- Initial unresolved/dead wikilinks: 58.
- Initial pages without inbound links: 23.
- The dry-run does not simulate post-write graph statistics; actual verification must rerun after writes.

## Final Verification

- Final page count: 119 Markdown pages under `wiki/`.
- Final dead wikilinks: 0.
- Final orphan pages: 0.
- Final idempotence check: `python scripts\rebuild_wiki_links.py --dry-run` reports no pending changes.
- `wiki/元数据/lint-report-2026-07-08.md` and `wiki/元数据/dashboard.md` both show 0 dead links and 0 orphan pages.
