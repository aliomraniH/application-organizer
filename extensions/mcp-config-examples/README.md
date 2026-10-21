# MCP config examples

`.mcp.json` entries for Claude Code. Copy the server you need into a `.mcp.json` at your project root (project scope, shared through git and approved on first use) or add it with `claude mcp add` ([MCP in Claude Code](https://code.claude.com/docs/en/mcp)). Claude Code expands `${VAR}` from the environment, so no secret is ever written into the file.

Before you use any of these, read the server's own page. Commands, flags and URLs change; the pages are linked in [connectors-and-mcp.md](../connectors-and-mcp.md).

## postgres-readonly.mcp.json

Two ways to read a Postgres database. Use one.

- `reporting-db-supabase`: Supabase's hosted server. `read_only=true` runs queries as a read-only role, `project_ref` scopes it to one project, `features=database` limits it to the database tools. Supabase calls prompt injection the primary risk and says to keep manual approval of tool calls ([Supabase MCP](https://supabase.com/docs/guides/ai-tools/mcp)). Sign-in is OAuth on first use.
- `reporting-db-reference`: the MCP project's reference Postgres server. It is archived and unmaintained ([servers](https://github.com/modelcontextprotocol/servers)); treat it as a starting point only. `PG_READONLY_URL` is a connection string for a role with SELECT only on one schema.

Whichever you use, the database still needs its own read-only role. A switch on the server is not a security control on its own. [Prompt 05](../../prompts/05-add-a-database.md) walks through the role, the named queries and a write-refusal test.

| Variable | Holds |
| --- | --- |
| `SUPABASE_PROJECT_REF` | the project ref, from the Supabase dashboard |
| `PG_READONLY_URL` | a Postgres connection string for the read-only role |

## google-drive.mcp.json

A remote Drive server over Streamable HTTP. The URL is a placeholder on purpose: copy it from the connector directory rather than guessing. On claude.ai, use the Google Drive connector instead ([Drive](https://claude.com/docs/connectors/google/drive)); claude.ai connectors also appear in Claude Code when you sign in with the same account ([MCP in Claude Code](https://code.claude.com/docs/en/mcp)).

| Variable | Holds |
| --- | --- |
| `GOOGLE_DRIVE_MCP_URL` | the server URL from the connector directory |

## research-sources.mcp.json

Two community servers for the weekly sweep. Maintenance unchecked; read each repository before use.

- `pubmed`: [pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server), E-utilities, PMC full text, MeSH.
- `arxiv`: [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server), search, download to Markdown, BibTeX.

The sweep can also call the public APIs directly (Crossref REST, PubMed E-utilities, the arXiv export API, OpenAlex) with no server at all.

| Variable | Holds |
| --- | --- |
| `NCBI_API_KEY` | an NCBI API key (optional; raises the rate limit) |
| `ARXIV_STORAGE_PATH` | a local folder for downloaded papers |

Local (stdio) servers like these two run in Claude Code only. They do not work on claude.ai ([getting started](https://support.claude.com/en/articles/11175166-getting-started-with-connectors-on-claude-ai)) A scheduled task cannot see a server that exists only on your machine; give it a connector or a committed `.mcp.json` ([scheduled tasks](https://code.claude.com/docs/en/routines)).
