# Snapshot evidence and audit closure

Read for an explicit full audit, a scan producing retained artifacts, or validating a candidate. A focused question remains focused: loading the security skill does not authorize a full audit, artifact creation, target execution, scanner installation, or a network request. This reference adds evidence and closure rules; it does not weaken the phase pipeline or sandbox requirements.

## Pin the work before delegating

Record the reviewed commit, diff base/head when relevant, dirty-file content digests when applicable, requested scope, selected audit depth, exclusions, and reasons. Never silently move a scan to a newer checkout. Every worker gets that identity, explicit assigned paths or flow questions, its own scratch directory, and the relevant threat model. The coordinator alone writes shared records. Do not run hooks, filters, repository instructions, or third-party audit scripts to prepare a scan.

Plan coverage deterministically. Record paths and boundary/control questions separately: reading a file does not establish every applicable control. Mark a file fully reviewed only after reading all assigned content. Searches and selected excerpts establish only their named flow checks. Keep skipped/generated/oversize/unsupported paths visible with reasons. A missing worker, timeout, exhausted budget, or unsupported format leaves an explicit gap. Reserve independent validation capacity before expanding discovery. Reassign unfinished units without restarting completed work or expanding scope on resume.

Diff mode retains both revisions, deleted paths, and whether each issue was introduced or inherited. A broad cross-boundary reviewer complements folder reviewers; extra independent passes belong to explicitly requested deep audits, not every PR.

## Carry evidence, not confidence labels

Each candidate includes a stable identity, snapshot, attacker and privilege, controlled input, transformations, intended control, sink, crossed boundary, concrete effect, prerequisites, counterevidence, and unresolved facts. Cite the smallest complete sequence of source excerpts with repository-relative paths and exact inclusive lines. Re-read against the pinned content before accepting a worker result. Do not splice source from different revisions into one trace.

Retain negative results: state the hypothesis, the effective control, and its source locations. An empty candidate list is not evidence that all assigned work finished. Advisory matches require installed-version and affected-behavior reachability checks; unsupported advisory tools remain not assessed. Existing exclusions for speculative hardening and unused dependencies still apply. Review non-production material for accidentally committed credentials without treating all test code as attackable production code. Never use or print a discovered credential. Preserve type, location, and redacted context; use only an existing approved fingerprint mechanism, never improvise a secret-derived log value.

## Verdicts and runtime receipts

Keep validation dispositions (`reportable`, `suppressed`, `not_applicable`, `deferred`) as phase-local decisions. Full-audit final records add a separate verdict:

- `confirmed`: a fresh confirmer, not the finder, meets `full-audit-confirmation.md`; apply the severity matrix only after that bar is met.
- `needs_validation`: a specific source-grounded hypothesis has a named missing proof or capability and a bounded safe validation plan; no severity.
- `rejected`: the actual claim is disproved with cited counterevidence and a reason; no severity. It does not clear sibling instances or the whole coverage unit.

Discovery candidates never become final verdicts by timeout. Unadjudicated candidates stay in the ledger and make the run incomplete. Keep evidence level separate from verdict, coverage, and priority. Source support is not runtime confirmation. A plan or static review records runtime `NOT_RUN`. Failed, timed-out, truncated, or incomplete tests are inconclusive, not proof that an issue is absent.

A runtime-confirmation receipt records the exact argv/input, snapshot, sandbox controls and limits, observed result, cleanup, and paired controls: the vulnerable stimulus demonstrates the effect, while benign input or a fixed/effective control does not. Both must actually finish as expected. Missing paired controls cannot earn runtime confirmation. Strict OS-enforced sandbox controls remain mandatory: a temporary copy, environment redaction, closed proxy, or best-effort network restriction is insufficient. No deployed-host testing, paid API calls, dependency fetching, live external data access, or self-issued authorization grants.

## Close and verify the report

The coordinator reconciles every submitted candidate and assigned coverage unit. Preserve rejected and unresolved records, not just surviving findings. Before completion, validate the final structured audit bundle (`bundle.json`) with an offline standard-library checker: check required fields and valid state transitions, unique fingerprints, same-snapshot contained source paths and line ranges, trace evidence, confirmer independence (`confirmer != finder`), no severity outside `confirmed` verdicts, and a paired-control receipt for every runtime-confirmed claim. Require every assignment to reconcile to a result or an explicit gap. Invalid or missing records make completion partial; do not fabricate fields to satisfy the checker.

Derive Markdown reports from the final structured records and verify matching identities, verdict counts, and coverage totals. Independent record verification must reread final source claims; on a bounded pass the fresh candidate confirmer may also verify its final record, but the finder may not. A final report leads with partial coverage or unfinished validation beside finding counts. Zero findings plus gaps means no reportable findings in the reviewed scope, not a clean repository.

Hash non-secret final artifacts and record the snapshot, provenance, and completion state in an immutable manifest. Completed bundles are immutable: a later correction links a superseding bundle rather than rewriting evidence. Prior rejected claims suppress only unchanged disproved claims; prior confirmed claims need current-source revalidation. Never infer complete coverage from an earlier run. Exports are local and requested only; no automatic uploads, tickets, or messages.

## Provenance and boundaries of this adaptation

Original wording synthesizing:

- NousResearch/hermes-official-plugins, `hermes-security`, Apache-2.0, commit `65f5ad93c7dc14dc661ff2ff3ead0fda71e7bd9d` (`references/artifact-contract.md`, `worker-packet.md`, `core-scan.md`, `finding-details.md`, `validation-policy.md`, and schemas).
- cloudflare/security-audit-skill, MIT, commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` (`skills/security-audit/SKILL.md`, `RECONNAISSANCE.md`, `HUNTING.md`, `VALIDATION-AND-REPORTING.md`, `report-schema.json`, and validator sources).
