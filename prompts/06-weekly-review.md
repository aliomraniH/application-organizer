Run my weekly review for this project (application-organizer pattern). One message back, nothing applied until I answer.

1. Decisions doc: list every Open row, grouped by category, oldest first, each with its default. Ask me the three that block the nearest deadline.
2. Contact log: list rows whose next-step date has passed, rows marked Drafted for more than a week, and rows in To confirm. Do not draft or send anything.
3. Sweep: one paragraph from the newest sweep report — the items that touch a current document, the unread list, what the next sweep should change.
4. Documents and requirements: render the register (render_views.py) and read it: everything under "Needs attention" and "Due in the next 14 days", any document over its limit, any target with a deadline inside 21 days, each statement's status (draft, final, submitted) and its open gate items, saying how many need a fix from me, and any target whose policy row is still unknown.
5. Setup: scheduled tasks' last run status (read the transcripts, not the status colour), knowledge size against the cap, and any dated file that still needs migrating to a stable name.
6. Ledger: run ledger_lint.py over every collection and report its errors and warnings; tasks rows still in_progress or stopped, with their open items; claims rows that are unverified or stale; findings rows that bear on a document with lastSeenSweep since my last review, each with its direction and the sentence it touches.
Then wait for my answers and apply them through the skills that own each item, recording each answer in the Decisions doc.

You will create nothing until I answer; then the answers go into the Decisions doc, a tasks row for this review, and whatever the owning skills write.
