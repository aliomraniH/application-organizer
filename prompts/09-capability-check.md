Run a capability check for this project and for the application-organizer repo (github.com/aliomraniH/application-organizer), using the capability-check skill. Propose first; change nothing until I approve a numbered item.

1. Read what the current Claude surfaces offer: the tool descriptions available in this session, the artifact runtime contract version, the docs guide index, the connectors pages named in extensions/connectors-and-mcp.md. Record the date.
2. Diff against docs/capabilities.md row by row: new, changed, removed, and anything there that you cannot verify today. Mark each row verified (one real call), documented, or unverified.
3. Propose, as a numbered list with a default of "no change": (a) repo changes — skills, templates, prompts, the capabilities doc, the version bump; (b) changes to this project — instructions, scheduled tasks, the console page, the ledger schema version. For each, one sentence on what it fixes or enables and one on the risk.
4. After my answers: apply only the approved items, bump versions, add the CHANGELOG entry, update meta/ledger.schemaVersion where the schema changed, and add a Decisions-doc row for anything that still needs me.
5. If I asked for a schedule, create a scheduled task that runs this check monthly on the cheapest model, with no connectors beyond the ones it reads from.
