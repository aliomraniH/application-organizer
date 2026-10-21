Set up and run the source tests for this project using the source-check skill (github.com/aliomraniH/application-organizer). Test first, change nothing: no write tool enabled, no scope widened, no credential pasted.

1. Ask me, in one message:
   a. Which sources this project reads: connectors in claude.ai, MCP servers in Claude Code (.mcp.json), public APIs, databases. Say for each whether it should be read-only.
   b. The scope of each: the folders, spaces, channels, schemas or watch lists it may read, and one thing just outside that scope it must not reach.
   c. One harmless read for each that proves it works (a search term, a file name, a named query), and what a normal result looks like (roughly how many items, which fields).
   d. For each database: the named harmless write to attempt against the read-only role, inside a transaction that is rolled back.
   e. Which scheduled tasks use which sources, and the names of the environment variables that hold any secrets (names only, never values).
   f. Whether to run the check on a schedule, on what day and time, and on which model (the cheapest is the default).
2. Write sources.md from templates/sources.md as a stable project file: one row per source, its probes, an empty results table, a change log.
3. Run the source-check skill once now, with me watching. Show me a table of source by check (Pass, Fail, Unverified) and, for each Fail or Unverified, what you saw.
4. Add a Decisions-doc row for each Fail, and for each Unverified that blocks a scheduled task, with options and the default "pause the dependent task". Do not fix anything yourself.
5. If I asked for a schedule, create a scheduled task with a short prompt that invokes source-check and points at sources.md, on the model I chose, carrying exactly the connectors under test and no others. Schedule it to run before the tasks that depend on those sources.
6. End with what I must do myself: settings only I can see or change (tool approval levels, task connectors, sign-ins), and the rows still Unverified.

You will create sources.md, the Decisions-doc rows for anything that failed, and, if I asked, one scheduled task.
