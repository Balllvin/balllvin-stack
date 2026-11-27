# Insecure defaults and sharp edges

A fail-open default turns a missing config value or an easy call into a
vulnerability. Written in our own words from ideas in Trail of Bits
`insecure-defaults` and `sharp-edges`
(https://github.com/trailofbits/skills, CC-BY-SA-4.0; no text copied).

## Fail-open patterns to grep for

| Pattern | Where it bites | Search |
|---------|--------------------|--------|
| Fallback secret: `os.getenv("X", "dev-secret")`, `settings.X or "changeme"` | JWT signing, webhook secrets, vault keys | `rg -n 'getenv\([^)]*,\s*["'"'"'][^"'"'"']+' backend/` |
| Empty or `None` secret skips the check | Bot webhook secret, API-key header | Read every `if not secret: return` in auth code. Missing config must fail closed. |
| `0` means unlimited | timeouts, retries, size limits | `rg -n 'timeout=0|max_[a-z_]*=0' backend/ crates/` |
| Debug or wildcard CORS in production | FastAPI `DEBUG`, `allow_origins=["*"]` with credentials | `rg -n 'allow_origins|DEBUG' backend/` |
| TLS verify off | httpx, requests, Node fetch agents | `rg -n 'verify=False|rejectUnauthorized' backend/ web/` |
| JWT algorithm from the token header, or `verify_signature: False` | Auth module, admin JWT | Decode must pin `algorithms=[...]`. |
| `==` on tokens, MACs, key hashes | API keys, webhook secrets, OAuth `state` | Use `hmac.compare_digest` / `secrets.compare_digest`. |
| Autonomy, payment tools, or kill switch default permissive | Agent autonomy and money settings | New account, empty row, and parse failure must all mean "off". |
| Broad scope accepted, narrowed later | Third-party account connects (OAuth) | Dangerous scopes (withdraw, transfer, admin) refused at connect, not filtered at call time. |
| Dev database URL accepted in production (SQLite, localhost) | App boot | Boot must refuse it. |
| `except Exception: pass` around auth or policy | Any gate | A failed check that continues is fail-open. |
| Empty trusted-proxy allowlist defaults to "trust all private ranges" | Proxy identity / client IP extraction | An empty allowlist must mean "trust no proxy"; unsigned `x-real-ip` / `x-forwarded-for` headers must never be trusted from an untrusted peer, and production boot should require an explicit allowlist. |
| Client-supplied `x-real-ip` / `x-forwarded-for` used as a rate-limit or admission key | Per-IP rate limiters, signed public owner tokens | Rate-limit scopes and admission tokens must derive from the socket peer or a signed proxy envelope the app itself issued, and token verification must re-bind the scope to the requester. |
| URL-borne single-use token redeemed with session cookies set | `/verify-email?token=...` or magic verification links | Verification may mark the account verified but must not open an authenticated session; sessions open only from an explicit login. Otherwise the link is a login-CSRF vector. |

## Sharp edges in our own APIs

An API whose easy path is insecure is a finding against the API. Examples:

- A key helper that can mint without a scope or expiry.
- A file lookup that accepts a global id where callers should pass a scoped one.
- A path tool that joins before it canonicalizes.
- A redaction helper that is opt-in per log call.

Fix the API so the safe call is the default call, then migrate callers.

## Before reporting

Trace the default to the security decision it reaches in a production
config. A permissive default that production always overrides, with a boot
check that fails without the override, is not a finding.
