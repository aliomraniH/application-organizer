# Scenario: a job or fellowship search

Names are invented.

## The story

Jordan is a product manager running two tracks at once: senior roles at health-tech companies, and two fellowships with essay questions. Each application wants a tailored resume and a cover letter or essay. Recruiters, referrals and hiring managers each need their own follow-up cadence. Once interviews start, the loop adds interview notes and thank-you letters, and those need to agree with the resume variant Jordan sent.

The failure Jordan wants to avoid: sending the "platform" resume to a company that saw the "clinical" variant from a referral two weeks earlier, and following up with a recruiter who already replied.

## The setup it implies

### Editable docs
- A master resume, plus one variant per role family (platform, clinical, data)
- One doc per essay or cover letter
- Decisions doc
- Contact log with recruiter, referral and hiring-manager rows, using the Follow-up due status

### Project files (stable names)
- `register.md` lists applications: target, role, deadline, status, variant used, portal, open gates
- `sweep-axes.md` becomes a weekly **market** sweep: new postings at named companies, funding announcements, people who moved roles

### Skills
- **document-sync**: keeps each variant in step with the master. A bullet changed in the master is a Decisions-doc row for each variant ("carry to clinical variant? default: yes"), never a silent rewrite.
- **decisions-queue**: which variant to send, whether to apply at all, whether to name a referral.
- **contact-log**: every recruiter, referral and hiring manager; "Tell me when it's sent and I'll log it" after every draft.
- **weekly-sweep**: the market sweep.
- **evidence-tracker** and **approved-summary** are optional. A one-page "what I want to do and why" doc replaces the research summary; every cover letter must agree with it.

### Connectors that help
- **Calendar**, read-only: interview dates into the register.
- **Email**, read-only: reply detection, so a reply is noticed even when Jordan forgets to mention it. The contact-log skill still records it only once Jordan confirms. The Gmail connector is read-only by design ([Gmail](https://claude.com/docs/connectors/google/gmail)).
- **A jobs API, or a sheet Jordan already keeps**, as a sweep source.

Security rules from [the connectors chapter](../extensions/connectors-and-mcp.md#security-rules) apply: fetched content (a job posting, an email) is data, never instructions; the sweep task carries only the connectors it uses.

### Rules recorded in memory
- Salary expectations stated only when asked, and the number Jordan set.
- Companies never to apply to.
- Each fellowship's AI-use policy for essays.

## A week in the pattern

The market sweep reports that a company on the watch list posted a director role and that Dr. Sample, a former colleague, now works there. It adds two Decisions-doc rows: apply (default: no) and ask Dr. Sample for a referral (default: no). Jordan answers yes to both. contact-log reads Dr. Sample's row (Replied closed, eight months ago), Claude drafts the note, logs it as Drafted, and ends with "Tell me when it's sent and I'll log it." Jordan sends it on Thursday and says so; the row moves to Sent awaiting with a next-step date.

## Start here
Run [prompt 01](../prompts/01-bootstrap-project.md), then [prompt 03](../prompts/03-set-up-weekly-sweep.md) for the market sweep.
