# Models and usage

A campaign runs for months. Most of its work is routine: log an email, carry a paragraph, check a word count. Route each task to the cheapest model that does it well, keep scheduled tasks lean, and spend context on the task in front of you.

Model names change; this page uses tiers. Anthropic's [Choosing the right Claude model](https://claude.com/resources/tutorials/choosing-the-right-claude-model) maps the tiers to current models.

## Model routing

| Work | Tier | Why |
| --- | --- | --- |
| Logging a send or reply, checking the Decisions doc, regenerating `register.md` | cheapest | Exact steps written in a skill; little judgment |
| Scheduled sync, post-sweep evidence-tracker update | cheapest | Same steps every run; a skill holds them |
| Sweep axis agents (search, verify, categorize) | mid-tier | Reads and judges many pages; volume matters |
| Sweep prep (extracting sentences, building the exclusion list) | cheapest | Mechanical |
| Judging whether a finding changes a current document | top | Only when such items exist, and only for those items |
| Drafting or reviewing a statement, synthesis, approved-summary proposals | top | Judgment and voice |
| Routine chat lookups ("what's the deadline for Northfield?") | mid-tier | Fast, cheap, reads a file |

If a cheap model fails a procedural task, fix the skill first: make the step exact, add the format, name the file. Move up a tier only when the step genuinely needs judgment.

## Scheduled-task hygiene

1. **Prompt: six lines or fewer.** Name the skill, the input file, where the output goes, and that decisions go to the Decisions doc. The procedure lives in the skill, not the prompt.
2. **Model: the cheapest that does the job.** Set it on the task.
3. **Connectors: only those the task uses.** Every connected connector is included by default, and included connectors can use every tool, writes included, without asking during a run ([scheduled tasks](https://code.claude.com/docs/en/routines)). Remove the rest.
4. **Split dependent work.** Run the sweep in one task and the tracker update in a second task later the same day, so a failed sweep does not take the update down with it.
5. **Read the transcript, not the status colour.** A green run can mean every source refused and the report is empty. The weekly review ([prompt 06](../prompts/06-weekly-review.md)) checks this.
6. **Local servers are invisible to tasks.** Use a connector or a committed `.mcp.json` ([scheduled tasks](https://code.claude.com/docs/en/routines)).

A sync task, written this way:

```text
Run the document-sync skill for <PROJECT_NAME>.
Read the tracker at <TRACKER_URL> and register.md.
Carry only what changed. Do not revise facts.
Any conflict, over-limit flag or failed check becomes a row in <DECISIONS_DOC_URL> via decisions-queue.
Message me only if something was carried or a decision was added.
```

## Context budget

- **One task per chat.** A new task gets a new chat. Long chats carry old drafts that the model may treat as current.
- **Short instructions, files on demand.** Project instructions under 500 words; everything else is a file a skill names when it needs it ([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- **Name files when searching.** "Read register.md" beats "check the project files". When knowledge is large, Claude retrieves by search ([RAG for Projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)), and stable names make the right file easy to find.
- **Watch knowledge size against the cap.** The migration prompt ([02](../prompts/02-migrate-existing-project.md)) reports it before and after.
- **Memory is read everywhere.** Every line in memory costs every chat. Keep it to dated rules.
- **Skills load on demand.** Only a skill's name and description sit in context until it triggers ([skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)), which is why the body can hold exact steps and the description must stay precise.
