Set up a new Claude Project for a long, document-heavy campaign using the application-organizer pattern (github.com/aliomraniH/application-organizer). Work in this order and ask me the questions in step 1 before creating anything.

1. Ask me, in one message:
   a. What the campaign is (e.g. PhD applications, job search, grant cycle, a team's document set) and its end date.
   b. The targets (programs, employers, funders, or document sets) and the documents each one needs.
   c. Which documents already exist (attach them or paste links) and which are still to write.
   d. Where my data lives: connectors already connected in this account (Google Drive, Microsoft 365, Notion, Slack, email, calendar), MCP servers, or none.
   e. Which skills from the repo I have saved (document-sync, decisions-queue, contact-log, weekly-sweep, evidence-tracker, approved-summary, source-check, project-ledger, capability-check) and which I want.
   f. The schedule: do I want a nightly sync and a weekly sweep, and at what times and model.
   g. The rules I already know I want (voice, facts that must stay exact, things never to name, each target's AI-use policy).
2. Create, in this order, and give me each link once:
   - a Claude Doc "Decisions waiting on <my name>" from templates/decisions-doc.md
   - a Claude Doc "Contact log" from templates/contact-log.md
   - one Claude Doc per document I will edit, with the current text
   - project files with stable names: register.md, sweep-axes.md (if a sweep), ledger-schema.md (from templates/ledger-schema.md), project-instructions.md
   - the tracker artifact: publish templates/console-page.html with my project name filled in, declaring the db capability (read: view, write: admin), and mcp only if I want a "Run sync now" button
3. Set up the ledger in the tracker's database with the project-ledger skill: write meta/ledger (schemaVersion "project-ledger v1", schemaDoc ledger-schema.md) and meta/config, one programs row per target, and open the first tasks row for this setup chat. Close that tasks row before your last reply.
4. Write the project instructions (under 500 words) from templates/project-instructions.md with my answers filled in, including the tracker link and the line "application-organizer v0.3.0", and tell me to paste them into the project's instructions field.
5. Record each rule from 1g in project memory as a dated line in my words. Do not record status (what was sent, what is current); that lives in the docs.
6. If I asked for scheduled tasks, create them with short prompts that invoke the skills, on the cheapest model that can do the job, with only the connectors each task needs, and tell me which approval setting each one got.
7. End with a checklist of what I must do myself: save skill cards, paste instructions, connect any connector I named but have not connected, remove unneeded connectors from the tasks, and open the tracker page once to see the registry, the first tasks row and the activity line.

You will create the Decisions doc, the Contact log, one doc per document, the stable project files, the tracker artifact with its console page and ledger (meta rows, one programs row per target, the first tasks row), the project instructions, dated memory rules, and any scheduled tasks I asked for.
