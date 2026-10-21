# Plugin

The six skills can install as one Claude Code plugin ([plugins docs](https://code.claude.com/docs/en/plugins)).

- `plugin.json` is the plugin manifest: name, version, description, author, license.
- `marketplace.json` is the marketplace entry. Its `source` is `"."`, the repository root, and its `skills` list names the six skill folders, so only those load.

## TODO: location

Claude Code reads a marketplace from `.claude-plugin/marketplace.json` at the marketplace root, and a manifest from `.claude-plugin/plugin.json` at the plugin root. A component path must stay inside the plugin root (`../skills` does not load). The files here follow the layout in [BRIEF.md](../BRIEF.md), which puts them in `plugin/`, so `/plugin marketplace add` does not find them yet.

To make the repository installable, a maintainer copies `marketplace.json` to `.claude-plugin/marketplace.json` at the repository root (not `plugin.json`: with the root as the plugin's source, the marketplace entry is the manifest), then checks it:

    claude plugin validate .

Untested: whether `"."` as `source` loads the listed skills as expected. Run the validator and a local install before announcing the plugin.

## Install, once the marketplace file is at the root

Inside Claude Code:

    /plugin marketplace add aliomraniH/application-organizer
    /plugin

then pick application-organizer from the Discover tab and choose a scope.

From a shell:

    claude plugin install application-organizer --marketplace aliomraniH/application-organizer --scope project

(The `--marketplace` form needs a recent Claude Code; older versions take the plugin name and marketplace name joined by an at sign. This repo's privacy check bans that character in Markdown, so it is spelled out here.)
