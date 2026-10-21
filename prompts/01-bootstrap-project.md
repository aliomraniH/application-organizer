Set up a new Claude Project for a long, document-heavy campaign using the application-organizer pattern (github.com/aliomraniH/application-organizer). Work in this order and ask me the questions in step 1 before creating anything.

1. Ask me, in one message:
   a. What the campaign is (e.g. PhD applications, job search, grant cycle, a team's document set) and its end date.
   b. The targets (programs, employers, funders, or document sets) and the documents each one needs.
   c. Which documents already exist (attach them or paste links) and which are still to write.
   d. Where my data lives: connectors already connected in this account (Google Drive, Microsoft 365, Notion, Slack, email, calendar), MCP servers, or none.
   e. Which skills from the repo I have saved (document-sync, decisions-queue, contact-log, weekly-sweep, evidence-tracker, approved-summary) and which I want.
   f. The schedule: do I want a nightly sync and a weekly sweep, and at what times and model.
   g. The rules I already know I want (voice, facts that must stay exact, things never to name, each target's AI-use policy).
2. Create, in this order, and give me each link once:
   - a Claude Doc "Decisions waiting on <my name>" from templates/decisions-doc.md
   - a Claude Doc "Contact log" from templates/contact-log.md
   - one Claude Doc per document I will edit, with the current text
   - project files with stable names: register.md, sweep-axes.md (if a sweep), project-instructions.md
3. Write the project instructions (under 500 words) from templates/project-instructions.md with my answers filled in, and tell me to paste them into the project's instructions field.
4. Record each rule from 1g in project memory as a dated line in my words. Do not record status (what was sent, what is current); that lives in the docs.
5. If I asked for scheduled tasks, create them with short prompts that invoke the skills, on the cheapest model that can do the job, with only the connectors each task needs, and tell me which approval setting each one got.
6. End with a checklist of what I must do myself: save skill cards, paste instructions, connect any connector I named but have not connected, remove unneeded connectors from the tasks.
