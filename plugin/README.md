# Plugin

The nine skills install together as one Claude Code plugin ([plugins docs](https://code.claude.com/docs/en/plugins)).

## Install

Inside Claude Code:

    /plugin install application-organizer --marketplace aliomraniH/application-organizer

That adds this repository as a marketplace and opens the install panel, where you choose a scope. It needs a recent Claude Code. On an older version, add the marketplace and pick the plugin from the Discover tab:

    /plugin marketplace add aliomraniH/application-organizer
    /plugin

From a shell:

    claude plugin install application-organizer --marketplace aliomraniH/application-organizer --scope project

(Older versions take the plugin name and the marketplace name joined by an at sign. This repo's privacy check bans that character in Markdown, so it is spelled out here.)

## How it is wired

Claude Code reads a marketplace only from `.claude-plugin/marketplace.json` at the marketplace root, so the file lives there, at the repository root, not in this folder. Its one entry:

- `source` is `"."`, the repository root, so the root is the plugin.
- `skills` lists the nine folders under `skills/`, so only those load. The docs, prompts and templates are copied with the plugin but are not components.
- With no `plugin.json`, the marketplace entry is the manifest: name, version, description, license and keywords live in it.

BRIEF.md placed the manifest and marketplace entry in this folder. They moved because Claude Code does not look here, and a plugin cannot load skills from outside its own root.

## Checking a change

After editing the marketplace file or adding a skill:

    claude plugin validate .

Then install it from your checkout to confirm the skills arrive:

    claude plugin marketplace add ./
    claude plugin install application-organizer --marketplace application-organizer

Bump `version` in the marketplace entry when the skills change; an installed plugin stays on its version until you do.
