---
name: approved-summary
description: Maintains the person's approved summary doc (the statement of direction every other document must agree with): proposes numbered changes, applies only what the person approves, keeps one approved file and one proposals file. Use when the person says update or approve the summary, dictates a change, or the post-sweep task asks for the weekly proposal.
---

# Approved summary

The summary is an editable doc in the person's voice. Controlled documents, outreach and the sweep must agree with it, so it changes only by the person's command or approval. Files: `summary.md` (approved copy, overwritten on each approval) and `summary-PROPOSED.md` (every pending numbered change, overwritten as changes are added, applied or rejected). The pending decision is one row in the Decisions doc; every new proposal updates that row.

Read the summary's README first for section structure and content rules; this skill wins on file naming.

## A. The person approves (all or named changes)
1. Read the proposals file and the approved copy; read the live doc since the last known revision (hand edits win).
2. Apply only the approved changes by find-and-replace on the quoted current text; change nothing else.
3. Add a version-history row (version, date, one-line change, approved by the person).
4. Export; overwrite `summary.md` with front matter (version, date, status APPROVED, link, one-line change).
5. Rewrite the proposals file to hold only what is still pending; close the Decisions row; add a ledger line.
6. Reply in one or two lines.

## B. The person asks for an update (no proposal pending)
Read the approved copy and everything since its date (sweep reports, ledger, register, memory rules, decisions stated in the conversation). Write numbered changes into the proposals file: section, current text verbatim, proposed text, reason, source with identifier and verification status. Show the numbers in chat; apply nothing until approved.

## C. The person dictates a change
Treat as approved; plant the section, fill it, then follow A. If it collides with a pending proposal, say so in one line and ask which comes first.

## D. Weekly proposal (post-sweep task)
Compare the newest sweep's verified findings and any decision recorded since the approved version with the approved copy and the pending proposals. Propose only where a finding bears on a specific sentence or a decision changed the direction; no stylistic rewrites. Add to the proposals file and the Decisions row. Report "No change proposed" or the change numbers.

## Content rules
First person, plain words, no product language; every number traces to a verified source and keeps its qualifier; preprints labelled; a change that would contradict a submitted document goes to the Decisions doc instead of being applied; version information lives only in the version-history table.
