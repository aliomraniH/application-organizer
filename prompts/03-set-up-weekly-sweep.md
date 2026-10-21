Set up a weekly literature or market sweep for this project using the weekly-sweep skill (github.com/aliomraniH/application-organizer). Ask first, then build.

1. Ask me: the theme in one paragraph; the search axes (3–8 topics); the people or organizations to watch by name; the sources I can reach (open web, a library login through my browser, APIs such as Crossref, PubMed, arXiv, OpenAlex, or an MCP server); what the sweep must never do (edit a statement, name a competitor, put my email in a request); the day, time and model.
2. Write sweep-axes.md from my answers as a stable project file: axes, watch list, identifiers (ORCIDs if I give them), tooling notes. The exclusion list and the window come from the findings collection in the tracker's ledger, not from a prose file; if the project has an old prose ledger, run prompt 08 first.
3. Create the scheduled task with a six-line prompt that invokes the skill, points at sweep-axes.md, names where the report goes, says that every identifier seen is written as a findings row, and says that every decision goes to the Decisions doc, never only into the report.
4. If updating an evidence tracker or an approved summary follows the sweep, create a second task that runs later the same day on the cheapest model, so a failed sweep does not take the updates down with it.
5. Run the sweep once now with "Run now", read the transcript, and tell me what it found, what it could not reach, and what to change in sweep-axes.md.

You will create sweep-axes.md, the sweep task, the optional post-sweep task, one dated report, the findings rows from that first run, and any Decisions-doc rows it queued.
