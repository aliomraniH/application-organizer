# Twenty lessons

Lessons 1 to 10 come from three months of one real campaign, run first without the pattern and then with it. Lessons 11 to 15 come from adding structured memory to the same campaign. Lessons 16 to 20 come from its last four weeks, when the documents were finished and submitted, and are the reasons for the [gates](gates.md). Each lesson names the failure it prevents.

## 1. One editable doc per thing people edit

**Rule.** Each document the person edits has one editable doc. Published copies, project files and the register follow it through document-sync.

**Failure it prevents.** Copies multiply writes. In the origin campaign, one approved sentence cost about 35 writes across four copies of the same statement, and every write was a chance for the copies to drift apart.

## 2. Stable filenames

**Rule.** Project files keep one name forever and are overwritten in place, with the version inside the file. No `statement-v3-final-oct12.md`.

**Failure it prevents.** Dated copies fill project knowledge with history, and search returns the wrong version. Once knowledge outgrows the context window, Claude retrieves the most relevant chunks ([RAG for Projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)); five near-identical files compete for the same query. History belongs in the editable doc's version history.

## 3. Short project instructions

**Rule.** Project instructions stay under 500 words and point to files loaded just in time.

**Failure it prevents.** A 27 KB rules file kept in memory is read by every chat, including the ones that only log an email. It crowds out the task and dilutes the rules that matter ([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

## 4. Memory holds dated rules, never tracking state

**Rule.** Memory records what the person decided, dated, in their words. It never records which email was sent or which version is current.

**Failure it prevents.** Tracking lines rot. In the origin campaign, memory recorded drafts as sent emails; later chats repeated the error with confidence. Status lives in the Contact log and the register, where it is visible and correctable.

## 5. One Decisions doc

**Rule.** Every question for the person goes to one Decisions doc, as a row with options and a default. Answered once, never asked again.

**Failure it prevents.** Decisions scattered across sweep reports, tracker notes and chat asides. The person is asked the same thing three times, or never, and silence is read differently each time. A default makes silence safe.

## 6. A Contact log is the only record of outreach

**Rule.** The Contact log is the only place outreach status lives. A draft is not a send until the person says so.

**Failure it prevents.** A draft logged as sent, so the follow-up never happens; or a send the person made from their phone never logged, so a second, duplicate email goes out.

## 7. Scheduled tasks: short prompt, skill, cheap model, few connectors

**Rule.** A scheduled task's prompt is a few lines that invoke a skill. It runs on the cheapest model that can do the job and carries only the connectors it uses. Read the transcript; a green run status is not success.

**Failure it prevents.** Long task prompts that drift from the skill they duplicate; top-model runs for logging work; a task that can write to Drive because every connected connector was included by default ([scheduled tasks](https://code.claude.com/docs/en/routines)); a "successful" run that found nothing because a source refused every request.

## 8. Disable unrelated skills

**Rule.** Enable only the skills the project uses. Write descriptions that say what the skill does and when, in the third person, without "ALWAYS use" ([skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).

**Failure it prevents.** Descriptions compete for the same request. A skill with shouting in its description triggers on tasks it was never meant for, and an unrelated skill runs its own procedure on your documents.

## 9. Verify citations at a primary page

**Rule.** A citation reaches a document only after it is checked at a primary page (the publisher, the registry, the preprint server). Preprints are labelled. Numbers keep their qualifiers ("in one sample of 212 adults", not "in adults").

**Failure it prevents.** A plausible but wrong year, journal or effect size in a submitted statement, and a preprint presented as peer-reviewed.

## 10. Know each target's AI-use policy before drafting

**Rule.** Before Claude drafts anything for a target, record that target's AI-use policy in memory and keep an authorship record per document: what Claude suggested, what the person wrote.

**Failure it prevents.** A submission to a target that requires sole authorship, or an attestation the person cannot sign honestly. Where a target requires it, Claude's text is a suggestion the person rewrites. From 0.4.0 the policy is a registry row with a mode and the authorship record is the `spans` collection ([gates.md](gates.md#authorship), lesson 16).

## 11. Status in prose rots; status in a row does not

**Rule.** Status lives in a row with a timestamp, an author and a source ([structured-memory.md](structured-memory.md)), never in prose or memory.

**Failure it prevents.** A tracking line in memory said two drafts were sent. A row with `at`, `by` and `source` would have said who claimed it and when, and the claim could have been checked.

## 12. An exclusion list is a set, not a document

**Rule.** Every identifier a sweep has seen is a `findings` row. The sweep's exclusion list is a query or a list to disk, never a prose file loaded whole.

**Failure it prevents.** A prose ledger grew to 40 KB in four weeks, and every sweep loaded it whole. 866 rows queried by identifier cost nothing.

## 13. A claim without a row is a claim nobody checked

**Rule.** A cited fact that reaches a controlled document has a `claims` row with its source and verification date. Forward-only is fine.

**Failure it prevents.** Provenance is cheap at write time and expensive at submission time. The first week's rows are the ones that matter, because they cover the sentences being edited now.

## 14. The judge must see the record, not the week

**Rule.** The sweep's judge and the weekly summary proposal receive a cumulative brief per watched sentence: every earlier finding on it, with direction and date. `atRev` says what the sentence said when the last decision was made.

**Failure it prevents.** A new paper weighed against nothing always looks important. Recency bias turns every Monday into a rewrite.

## 15. Write a page's rows, then look at the page

**Rule.** When a console page is built in the same session as its data layer, say that it has not been rendered, and let the first look be the person's.

**Failure it prevents.** A session that cannot render the page reports it as working. The rows can be checked from the session (seed them, read them back at viewer level, try a write the rules must refuse); the page cannot.

## 16. Put the control where the problem starts

**Rule.** A rule about what Claude may write is enforced when Claude writes: the target's policy is a row with a mode, read before the first draft, and the mode decides whether wording is written, suggested or withheld. The check at the end only confirms what the record shows.

**Failure it prevents.** A rule that lives as a sentence in the instructions is read at the start of a chat and is far away by the fortieth turn. A check that first runs on the day of the deadline finds text that is already written, and a block with no time to fix it gets skipped.

## 17. Bind a claim to its words, not to a revision

**Rule.** A claims row carries the exact sentence that states the fact. The row holds for as long as that sentence is in the text.

**Failure it prevents.** In the origin campaign, claims rows pointed at a doc revision. Every edit anywhere in the document left rows to re-point, and re-pointing was the step most often still open when a chat ended. A row bound to its sentence needs no attention until that sentence changes, which is exactly when it should get some.

## 18. A check must find what has no row

**Rule.** The final check scans the text for the shapes a fact takes (figures, years, citations, names) and reports every one that no claims row covers.

**Failure it prevents.** A check that walks the rows can only confirm the rows. A provenance row gets written when someone remembers to write it, so the number nobody recorded is both the one most likely to be wrong and the one a row-based check passes in silence.

## 19. Final is a property of a text, not of a day

**Rule.** "Final" is stored with a hash of the text that passed the check. Any edit returns the document to draft. One path builds the submission file, from the text that was hashed.

**Failure it prevents.** In the origin campaign, documents were marked final and edited again the same day, more than once. The register said final about a text that no longer existed, and the file that went out was built by hand from whichever version was open.

## 20. A gate needs a way through that leaves a mark

**Rule.** Every gate item is pass, fail or waived. A waiver is the person's, for one item, in their words, with a reason, and it stays on the record. Only what cannot honestly be waived is fix-only: a source that contradicts the sentence, and Claude's wording under a policy that requires the person's own.

**Failure it prevents.** A gate with no way through is bypassed whole, and then it protects nothing. A gate with a quiet way through is decoration. The person's word wins in this pattern, so the gate cannot stop them and should not try; its job is that they decide each item knowingly, and that the decision can be read later.
