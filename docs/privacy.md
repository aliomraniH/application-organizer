# Privacy

This repository is public. Your campaign is not. The pattern keeps them apart: the repo holds the method, your Claude Project holds your material.

## Never in this repository

- A real person's name, email address, phone number or handle
- A real institution, program, employer, funder or team, when it identifies you or someone else
- A document URL (Claude Docs, Google Docs, SharePoint, Notion, anything with an id in it)
- Any private fact: a deadline you are working to, a recommender, a reply you got, a decision you made
- Secrets: API keys, connection strings, tokens. `.mcp.json` files use `${VAR}` and the value lives in an environment variable or a network secret

## Never in a shared doc

Shared docs (a Decisions doc you show a mentor, a register you share with a team) follow the same rules as the repo, plus:

- No other person's contact details unless they are already shared with everyone who can open the doc.
- No content from another person's private message pasted in full; summarize the gist and the date.
- Your own email address is not written anywhere new (the [contact-log skill](../skills/contact-log/SKILL.md) enforces this).

## Placeholder convention

Placeholders are angle-bracketed and upper-case with underscores. They are filled in your project, never in the repo.

| Placeholder | Means |
| --- | --- |
| `<PROJECT_NAME>` | the name of your Claude Project |
| `<PERSON>` | the person whose campaign it is |
| `<DECISIONS_DOC_URL>` | link to your Decisions doc |
| `<CONTACT_LOG_URL>` | link to your Contact log |
| `<TRACKER_URL>` | link to your sync tracker |
| `<project-files>` | the folder or prefix your project files live under |
| `<url>`, `<date>`, `<orcid>` | a value filled per row |

Lower-case angle-bracketed phrases in templates (`<what the project is about, in plain words>`) are instructions to the person filling them in.

Worked examples use invented names only: Dr. Example, Dr. Sample, Northfield University. Add new invented names in the same style and list them in your pull request.

## The at-sign check

An email address is the most common leak, so the repo bans the at sign in Markdown. [CONTRIBUTING.md](../CONTRIBUTING.md#privacy-check) has the pre-commit check. The only documented exceptions are the two lines in [BRIEF.md](../BRIEF.md) that state the rule itself by quoting the character.

## If something leaks

Removing a file in a new commit does not remove it from history. If a real name, address or secret is pushed, rotate any secret first, then rewrite history (for example with `git filter-repo`) and force-push, and tell the maintainers so forks can be checked.
