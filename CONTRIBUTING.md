# Contributing

Contributions that make the pattern easier to adopt are welcome: a new skill, a new scenario, a sharper lesson, a correction to the connectors chapter. Keep the repo small; every file should earn its place.

## Proposing a skill

1. Open an issue first, naming the recurring procedure the skill would own and the doc or file it would write. If an existing skill could own it with one more step, propose the step instead.
2. Follow Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):
   - `name` and `description` frontmatter; the description says what the skill does and when to use it, in the third person
   - body under 500 lines (ours are under 50)
   - exact steps for fragile operations: writes, syncs, anything with a lock or a guard
   - no time-sensitive wording, no CRITICAL or ALWAYS shouting
3. End every open question as a row in the Decisions doc through decisions-queue, never in a report or chat.
4. Keep placeholders angle-bracketed: `<DECISIONS_DOC_URL>`, `<CONTACT_LOG_URL>`, `<TRACKER_URL>`, `<PROJECT_NAME>`.
5. Add one row to [skills/README.md](skills/README.md) and the folder to the `skills` list in [plugin/marketplace.json](plugin/marketplace.json).

## Proposing a scenario

1. Write a short story with invented names, then the setup it implies: editable docs, project files, skills, connectors, rules in memory. Follow the shape of the files in [scenarios/](scenarios/).
2. Include one "week in the pattern" paragraph that shows a change passing through the Decisions doc.
3. If the scenario adds a source, write the [security rules](extensions/connectors-and-mcp.md#security-rules) into it.

## Proposing a starter prompt change

The prompts in [prompts/](prompts/) are copied byte for byte into [README.md](README.md). Change both in the same commit, and keep each prompt self-contained: its questions in one numbered block, ending with what it will create.

## Facts and sources

Cite the page a rule or feature comes from. Do not describe a product feature you have not seen documented. Where a fact is uncertain, say "unverified". New external links go in the Sources list of [BRIEF.md](BRIEF.md) in the same pull request.

## Privacy rule for contributions

The repo is public. See [docs/privacy.md](docs/privacy.md). In short:

- No real person's name, email, institution, program, document URL or private fact. Use invented names (Dr. Example, Dr. Sample, Northfield University).
- No secrets. `.mcp.json` uses `${VAR}`.
- If you adapted a skill from your own project, strip every filled placeholder back to its angle-bracketed form before you commit.

### Privacy check

The check fails on any at sign in a Markdown file, the usual sign of an email address. The one documented exception is a line that quotes the character itself in double quotes, as BRIEF.md does when it states this rule. The script writes the character as the octal escape `\100`, so this file passes its own check.

Save as `.git/hooks/pre-commit` and make it executable (`chmod +x .git/hooks/pre-commit`):

```sh
#!/bin/sh
# Fail the commit if any Markdown file contains an at sign,
# except a line that quotes the character itself in double quotes.
at=$(printf '\100')
hits=$(grep -rnF --include='*.md' --exclude-dir=.git -e "$at" . | grep -vF "\"$at\"")
if [ -n "$hits" ]; then
  echo "Privacy check failed: at sign found in Markdown."
  echo "$hits"
  echo "Replace addresses and handles with an angle-bracketed placeholder."
  exit 1
fi
```

Run the same check by hand before opening a pull request:

```sh
sh .git/hooks/pre-commit && echo "privacy check passed"
```

## Pull requests

- One change per pull request.
- Say which acceptance checks in [BRIEF.md](BRIEF.md) you ran.
- By contributing, you agree your contribution is licensed under the [MIT License](LICENSE).
