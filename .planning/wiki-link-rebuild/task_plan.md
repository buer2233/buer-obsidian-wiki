# Wiki Link Rebuild Plan

Goal: rebuild link indexes for `wiki/`, add direct wikilink relationships between related files, and make those relationships visible in Obsidian Graph.

## Phases

- [x] Phase 1: Load repository and wiki skill instructions.
- [x] Phase 2: Analyze current pages, links, dead links, orphans, and folder coverage.
- [x] Phase 3: Generate/refresh indexes and managed related-link sections.
- [x] Phase 4: Update Obsidian graph/color support files and wiki cache/log.
- [x] Phase 5: Verify graph health and summarize changed files.

## Constraints

- Do not modify `.raw/`.
- Prefer Obsidian wikilinks (`[[Note Name]]` or path-disambiguated links) over Markdown file links.
- Preserve existing prose and user-authored content.
- Use managed sections for generated relationships where possible.

## Errors Encountered

| Error | Attempt | Resolution |
|---|---|---|
| Missing `session-catchup.py` under `.codebuddy` | Ran planning-with-files session catchup command | Continue with local `.planning/wiki-link-rebuild/` files and record progress manually. |
| `StopIteration` in `build_relations` | First `--dry-run` of link rebuild script | Root cause: scores included resolved index/meta notes while ranking only searched content notes. Filtered candidates to the content-note map before ranking. |
