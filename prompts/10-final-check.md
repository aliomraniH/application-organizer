Turn on the gates for this project and run a final check on one document, using the final-check skill from the application-organizer pattern (github.com/aliomraniH/application-organizer; design in docs/gates.md). Change no document text. Ask me the questions in step 1 before writing anything.

1. Ask me, in one message:
   a. Which document I want checked first, and its target's deadline.
   b. For each target, where its AI-use policy is published (a link, or "I don't know"), and what I already believe it says.
   c. Whether I have already submitted anything, and when.
2. If meta/ledger has no gates entry: save templates/final_check.py as the project file final_check.py.txt; update meta/ledger with gates {version "gates 1", enabledAt, tool} and add spans and gates to collections; add deadline and each statement's status "draft" to every programs row. Tell me what you added.
3. For each target, read the policy page yourself and propose a policy row: the mode (open, own-words, feedback-only), the sentence of the policy that decides it, the link and today's date. Where the policy is unclear, propose the stricter mode and say why. Write a row only after my yes. A target whose policy you could not read stays unknown, and you draft nothing for it.
4. Run the preview for the document from 1a and show me every open item in three groups: what needs a fix from me, what you can verify at a source now, and what needs my word. Do not propose waivers.
5. Work the second group: verify each fact at its source and write its claims row with the exact sentence as its span. Then ask me the third group in one numbered message.
6. Tell me how many spans of your own wording are on record for this document, and from what date. Say plainly that wording you wrote before the gates were on is not on record, so for that period the record cannot speak and my own answer is all there is.
7. When nothing is open, and only if the policy is own-words or feedback-only, ask me the authorship question once and store my answer word for word. Then run the check, record the gate, and build the submission file from the text that passed.
8. Add a line to the nightly sync so it runs the preview and returns an edited final document to draft, and add "Gates open" to my weekly review.

You will create the project file final_check.py.txt, the gates entry in meta/ledger, a policy row per target I approve, claims rows for the facts you verify, a gates row for the document, and, on a pass, the submission file. Nothing in any document changes.
