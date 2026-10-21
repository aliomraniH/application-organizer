Add a database as a data source for this project using an MCP server, read-only, following extensions/connectors-and-mcp.md in github.com/aliomraniH/application-organizer.

1. Ask me: the database (Postgres, MySQL, SQLite, Snowflake, BigQuery, Databricks, MongoDB, other); where it runs; whether a read-only role exists (if not, give me the SQL to create one and stop until I confirm); which tables or views are in scope; the questions the weekly sweep or a skill should answer from it; where secrets will live (environment variable, network secret, never a project file).
2. Choose the server (vendor or reference) and write the .mcp.json entry from extensions/mcp-config-examples with placeholders for secrets. Tell me where it goes for claude.ai (a connector), Claude Code (project-scope .mcp.json) and scheduled tasks (connector included on the task).
3. Write the queries the skill will run as named, parameterized statements in a project file; the skill runs only those, never free SQL, unless I ask in chat.
4. Test with one query, show the result shape and row count, and confirm the role cannot write (attempt a harmless write and show the refusal).
5. Add a line to project instructions naming the source and its limits.
