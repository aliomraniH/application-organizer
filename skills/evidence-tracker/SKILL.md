---
name: evidence-tracker
description: Updates the evidence tracker doc after each weekly sweep or when the person dictates a change: one tab per theme with open questions, cumulative evidence, watched people, and rolling last-year, six-month and last-week sections. Use when the post-sweep task fires or the person asks to update the tracker.
---

# Evidence tracker

The tracker is an editable doc with a summary tab and one tab per theme. After each sweep it gets a new version in place and its markdown export overwrites one stable project file `evidence-tracker.md`. The weekly update needs no approval; it is a tracker, never a statement, so it changes no controlled document.

Read first: the tracker's own README in project files (tab ids, exact section format, writing rules). The README wins on format; this skill wins on file naming (stable file, no dated copies).

## After a sweep
1. Read the README, the newest sweep report with any library-pass corrections, the ledger, the current `evidence-tracker.md`. If no sweep is newer than the last version, stop: "No new sweep".
2. Read every tab of the live doc and compare with the file. The person's hand edits win: keep them, edit around them.
3. Map report sections to themes as the README says.
4. Per theme, one guarded update per section: rewrite Last week; add rows to Last six months and drop rows older than six months; extend Last year and drop material older than twelve months; update evidence cells in Open questions (status changes only when the question set changed); change Cumulative evidence only when the state of evidence changed; update Newest work seen for watched people.
5. Summary tab: changed glance cells, all of Across the themes, the as-of date, a version-history row.
6. Version: minor bump each week; major when a theme or section is added, removed or renamed.
7. Export every tab as markdown, concatenate in tab order under `# Tab: <name>` headings with front matter, check no template markup survives, overwrite `evidence-tracker.md`, add a register row to the README.
8. Report one line with the doc link.

## When the person dictates a change
Apply as dictated; minor bump for content, major for structure; log "dictated" in the version history; if the format changed, update the README so future runs follow it.

## Writing rules
Sentences under 25 words; specifics not adjectives; every number with its qualifier; preprints labelled; library-pass corrections win over sweep wording; never frame a watched person's work as limited; never state an affiliation or date not seen in a project file or verified source; questions the update cannot settle go to the Decisions doc.
