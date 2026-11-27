# Full audit confirmation

Load this on a full audit, a pen test, or any pass that might label a lead `confirmed`. A diff review stays in `security-review.md`. A requested fix stays in `security-fix-verification.md`.

Adapted from Cloudflare's `security-audit-skill` (MIT, commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`).

## When target code may run

Source inspection is read-only. Run the application, its tests, a fuzzer, or a browser only inside an OS sandbox that enforces all four controls:

- **No external network.** Local client and server traffic uses an isolated loopback, not the host loopback.
- **Empty environment.** The process starts from an empty environment. An explicit allowlist holds safe values only; `HOME`, temp, and caches sit in that run's scratch directory.
- **Read-only target and toolchain.** The target repo and toolchain are read-only; the process writes only inside its private scratch directory.
- **Strict resource limits.** CPU, memory, process count, file size, disk, and wall-clock limits are set and kept low.

A missing control means you do not run the target. Record the missing control on the lead, leave the lead at `needs_validation`, and do not assign a severity.

Never probe deployed/production hosts, third-party APIs, payment/broker systems, or spend paid API quota. Use dummy principals. If a credential appears in command output, replace it with `REDACTED` before the next write and never reconstruct secrets or connection strings.

## Who may confirm

The confirmer is not the finder. A fresh agent re-reads the cited functions at the pinned commit. That agent did not write the candidate. Confirmation is a reproduction inside the sandbox above (with paired positive and negative controls per `snapshot-evidence-and-closure.md`), or a trace that shows the claim is false. The finder does not promote their own lead.

Only a `confirmed` lead gets a severity. `needs_validation` means a source-grounded hypothesis is blocked and has no severity.

A trace names the entrypoint and ends at the sink. Evidence paths are git paths at the pinned commit, not files under site-packages. Cite the function and re-read it before moving a line number onto a later commit.

## Ledger

- `needs_validation` does not mark a coverage unit covered.
- Rejecting a claim marks that claim covered; it does not clear the rest of the unit or sibling instances.
- A rejected claim stays rejected while the cited functions are unchanged.
- A second run does not make the first run exhaustive. State explicitly what was not traced.

Artifacts stay outside the repo, where `scan-artifacts.md` says. An audit does not patch product code.

## High-value controls to trace on any full audit

Trace each applicable boundary rather than assuming enforcement from a directory or helper name:

- **Session and account state:** Token/session loading rechecks active/enabled status, email/token verification does not auto-mint sessions for inactive or unauthenticated flows (login-CSRF), and logout/disable revokes refresh tokens and active sockets.
- **Client identity and proxy trust:** Proxy headers (`X-Forwarded-For`, `X-Real-IP`) are trusted only from an explicit non-empty trusted-proxy CIDR/envelope check; an empty allowlist fails closed (`trust no proxy`).
- **Billing and entitlements:** Webhook/billing handlers claim idempotency keys atomically (without clock-based keys) and enforce entitlements at the spending boundary across all surfaces (HTTP, CLI, MCP, bots, background workers).
- **Captured authority:** Background jobs, streams, sandboxes, and scheduled tasks recheck the captured user/admin flags and scopes before writing or spending.
- **Public errors and secrets:** Health/error endpoints never leak exception strings, internal URLs, or database DSNs; deployed startup rejects dev/built-in DB URLs; logs carry IDs only.
- **Sandbox execution bounds:** Subprocess/VM runs enforce cancellation from outside the process, bind files to the run, and cap input/output sizes.
- **Installers and release feeds:** Follow `supply-chain.md`.
