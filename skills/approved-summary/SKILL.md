---
name: approved-summary
description: Maintains the person's approved summary doc (the statement of direction every other document must agree with): proposes numbered changes, applies only what the person approves, keeps one approved file and one proposals file. Use when the person says update or approve the summary, dictates a change, or the post-sweep task asks for the weekly proposal.
---

# Approved summary

Expects schema **project-ledger v1**; the ledger is at <TRACKER_URL>. The summary is an editable doc in the person's voice. Controlled documents, outreach and the sweep must agree with it, so it changes only by the person's command or approval. Files: `summary.md` (approved copy, overwritten on each approval) and `summary-PROPOSED.md` (every pending numbered change, overwritten as changes are added, applied or rejected). The pending decision is one row in the Decisions doc; every new proposal updates that row.

Read the summary's README first for section structure and content rules; this skill wins on file naming.

## A. The person approves (all or named changes)
1. Read the proposals file and the approved copy; read the live doc since the last known revision (hand edits win).
2. Apply only the approved changes by find-and-replace on the quoted current text; change nothing else.
3. Add a version-history row (version, date, one-line change, approved by the person).
   Claims: for each approved change that states a cited fact or number, write or update its claims row (`set · claims/summary-<section>-<nn> · {text, docBlockId, docRev, source, qualifier, verifiedAt, verifiedBy, verifiedHow, status: "verified", findingId?, decisionId}`); a fact whose source was not verified stays `unverified` and gets a Decisions-doc row.
4. Export; overwrite `summary.md` with front matter (version, date, status APPROVED, link, one-line change).
5. Rewrite the proposals file to hold only what is still pending; close the Decisions row; add a ledger line.
6. Reply in one or two lines.

## B. The person asks for an update (no proposal pending)
Read the approved copy and everything since its date (sweep reports, ledger, register, memory rules, decisions stated in the conversation). Write numbered changes into the proposals file: section, current text verbatim, proposed text, reason, source with identifier and verification status. Show the numbers in chat; apply nothing until approved.

## C. The person dictates a change
Treat as approved; plant the section, fill it, then follow A. If it collides with a pending proposal, say so in one line and ask which comes first.

## D. Weekly proposal (post-sweep task)
Compare the newest sweep's verified findings and any decision recorded since the approved version with the approved copy and the pending proposals. For each candidate sentence, build the cumulative brief: every findings row that touches it (`query · findings · where touches array-contains "summary ¶n"`), with count, direction and dates, and read the sentence as it stood at the last decision on it (`atRev`). Propose only where the cumulative record moved or a decision changed the direction; one new finding that repeats the record is not a proposal; no stylistic rewrites. Add to the proposals file and the Decisions row. Report "No change proposed" or the change numbers.

## Working memory
Open a tasks row at the start of A, B, C or D and close it before the final reply (project-ledger).

## Content rules
First person, plain words, no product language; every number traces to a verified source and keeps its qualifier; preprints labelled; a change that would contradict a submitted document goes to the Decisions doc instead of being applied; version information lives only in the version-history table.

## Related skills
The pending-proposal row lives in <DECISIONS_DOC_URL> and is kept by decisions-queue. When an approved change means a controlled document no longer agrees, add a Decisions-doc row naming the document; document-sync carries the person's resulting edit.
