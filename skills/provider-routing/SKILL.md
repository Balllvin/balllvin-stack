---
name: provider-routing
description: Use for LLM or AI provider integration work - model routing, adding or swapping a model, model ids, prices, or context limits, OpenRouter calls and zero-data-retention (ZDR) policy, xAI / Grok API and SDK calls, reasoning effort, search tools, structured output, prompt caching, STT, TTS, image, or voice, provider fallbacks and timeouts, or OpenAI docs lookups. Triggers include /provider-routing, /xai-api-mastery, /prompt-cache-optimization, /openai-docs, "xAI", "Grok API", "OpenRouter", "model routing", "which model", "model price", "prompt caching", "cache hit rate", "TTS", "transcribe". Load before editing any LLM router, provider adapter, or audio/voice client.
---

# Provider Routing

Use this skill for LLM, OpenRouter, xAI, search-tool, prompt-cache, STT/TTS, image, and voice-session work. Provider behavior drifts weekly and wrong request shapes fail silently into fallbacks, so keep one routing owner and verify against live endpoints and docs.

**Live facts only.** Every model id, price, context or output limit, rate limit, and supported parameter you write into code, a PR, or a reply comes from a live source read this session: the provider's models API (`GET https://openrouter.ai/api/v1/models`, the xAI models endpoint) or its current docs page. Cite the URL next to the fact. Memory and another model's map are not sources. Pattern from Anthropic's `claude-api` skill.

**OWASP LLM checks this hub owns** (https://genai.owasp.org/llm-top-10/; full threat pass lives in `../security/SKILL.md`):
- **LLM02 sensitive disclosure:** Prompts, keys, and user data never reach logs. Enforce explicit zero-data-retention (ZDR) / privacy policy in the router without ad-hoc host allowlists or denylists that drift.
- **LLM10 unbounded consumption:** Every provider call has a fixed hang timeout, a max output token cap, and a known cost per call. Do not cap an agent tool loop with a turn budget (`max_turns`, `TURN_BUDGET`); hard tasks need many rounds while each individual RPC keeps a bounded deadline.

## Index

| Need | Where |
|---|---|
| Workflow and routing rules | [Workflow](#workflow), [Routing Rules](#routing-rules) |
| Model additions, Gate A and Gate B | [Adding / editing / replacing a model](#adding--editing--replacing-a-model-mandatory) |
| xAI Chat SDK vs Responses API, deadlines | [xAI Chat vs Responses](#xai-chat-vs-responses-request-shape-mandatory), [xai-api-mastery](references/xai-api-mastery.md) |
| Prompt caching and cache keys | [Prompt caching](#prompt-caching), [prompt-cache-optimization](references/prompt-cache-optimization.md) |
| Speech, audio, and voice leases | [Speech and Voice Rules](#speech-and-voice-rules) |
| OpenAI API docs lookup | [openai-docs](references/openai-docs.md) |

## Workflow

1. Search the current routing path in your repo before editing (`rg` for router entrypoints, reasoning-effort maps, search tools, fallback/retry wrappers, and STT/TTS/voice schedulers).
2. Keep one canonical owner per concern (router, model/effort registry, privacy policy, retry policy, reasoning trace capture, shared audio/voice scheduler). Do not duplicate provider logic at callsites.
3. Verify provider behavior against **live** official docs whenever request shape, tool support, model ids, search config, response metadata, **or supported `reasoning.effort` enums** are uncertain:
   - OpenRouter: `GET https://openrouter.ai/api/v1/models` -> `reasoning.supported_efforts` (never memory, never another model's map).
   - xAI: `docs.x.ai` + the installed `xai-sdk` `IncludeOptionMap` / `chat.create` signature.
4. Keep provider details inside routing and transport layers. Callers ask for presets or tool intent, never raw model ids.
5. Add request-shape tests when changing model resolution, search tools, structured output, timeout, token accounting, reasoning effort maps, or provider metadata.

## Routing Rules

- Expose user-facing presets (for example `fast`, `medium`, `high`) plus dedicated internal presets (`structured`, `tool`, `scanner`, etc.); resolve deprecated aliases inside the router only.
- Raw provider model ids must not leak into app or service callsites except through an explicit user model-settings contract.
- Search evidence and structured formatting are different jobs. Do not send research-gathering calls to a structured-output formatter just because the caller wants JSON; gather evidence with search first, then format.
- When search tools are enabled, map intent to the target provider's native search capability (e.g., OpenRouter web search vs xAI SDK `web_search` / `x_search`). Do not silently downgrade platform-specific search intent (such as social/X search) to generic web search.
- One model per preset. Presets differ in reasoning effort, not silent multi-model fallback chains that hide failures or mix capabilities.
- Keep canonical bare wire ids without routing suffixes (such as `:nitro`, `:exacto`, `:free`, or `:floor`) unless an explicit architecture policy requires one; normalize deprecated ids to the canonical bare id.
- **Transport-layer-only retries.** Retries live in the transport that sends the request; never wrap a transport call in a second retry loop. Retry only transient failures (`connect error`, `timeout`, HTTP `429`, HTTP `5xx`); fail immediately on non-retryable `4xx` (`400`, `401`, `403`, `404`), and treat `402` as its own quota/billing class.
- **Stream retry safety.** Retry a stream **only before any answer text has been shown** to the caller/UI. Once streamed text has started, do not resend the turn; surface the plain failure. Bound retries (for example max 5, exponential backoff with jitter, cap `Retry-After`, bounded stream idle timeout) and ensure a retry never writes a result twice.
- **Tool calls and error metadata.** Return streamed tool calls with invalid JSON arguments or unknown names to the agent kernel unchanged so the kernel answers them; preserve `failed_attempts` and `primary_error_type` in result metadata.
- **No turn budgets on agent loops.** A provider call has a deadline, not the outer tool loop.
- **Evidence on latency claims.** A routing latency claim is not a result until the limiter is named and alternative explanations are ruled out with a run ([Explain the number](../build/references/principle-explain-the-number.md)).

## Adding / editing / replacing a model (mandatory)

Every catalog add, edit, or replace must pass **both** gates below before shipping. Skipping either gate is a routing bug.

### Gate A — the wire id

Before adding any non-direct-SDK model (such as OpenRouter):

1. Confirm the model exists on `GET https://openrouter.ai/api/v1/models` and meets your ZDR / data-retention policy.
2. Store the canonical bare wire id with no undocumented routing suffix (`:nitro`, `:exacto`, `:free`, `:floor`).
3. Do not inject ad-hoc `provider` host allowlists/denylists or routing suffixes to work around an upstream outage.

### Gate B — Reasoning levels + cost-per-intelligence Pareto

Reasoning effort is part of the model contract. Wrong enums fail requests or silently drop thinking. **Never copy another model's map or reuse a `medium`/`high`/`xhigh` template.**

1. **Fetch live `reasoning.supported_efforts`** from `GET https://openrouter.ai/api/v1/models` (or current provider docs for direct SDKs).
   - Models vary widely: some use `low` / `high` / `max` (not `medium` / `xhigh`), some list `high` / `xhigh`, some omit `xhigh`, some omit `medium`, and some expose no `supported_efforts` at all.
   - **No `supported_efforts` (or no `reasoning_effort` param):** omit the model from the effort map so the transport skips the `reasoning` payload completely. Do **not** invent enums.
2. **Map public tiers deliberately** (`fast` -> lightest supported, `medium` -> default/mid, `high` -> deepest useful supported effort on that model), keeping any enum still needed by fixed internal presets.
3. **Update every registry the model touches** (plan/model catalogs, deprecated remaps, fixed presets, reasoning-level tables).
4. **Choose model + effort from the Intelligence vs Cost-per-Task Pareto frontier**, not sticker `$/M` input/output rates alone (use [Artificial Analysis models](https://artificialanalysis.ai/models) or equivalent cost-per-task benchmarks that fold in input, cache, reasoning, and answer tokens):
   - `fast`: cheapest near-frontier effort clearing the quality floor for light turns.
   - `medium`: mid-frontier default (best cost per task for typical chat).
   - `high` / `tool`: deepest effort that earns its cost; do not burn `max` on recurring scanner or summarizer jobs without measured quality need.
5. **Add tests** for effort resolution on `fast`/`medium`/`high`, bare-id normalization, fixed presets, omit-effort models (asserting the `reasoning` payload is skipped), and explicit `reasoning_effort=` pins.

## xAI Chat vs Responses request shape (mandatory)

When calling Grok via the **xAI Python Chat SDK** (`client.chat.create` -> `chat.sample()` / stream), do not mix in Responses API (`/v1/responses`) parameters:

| Intent | Chat SDK (`client.chat.create`) | Responses API (`/v1/responses`) |
| --- | --- | --- |
| Encrypted reasoning | `use_encrypted_content=True` | `include: ["reasoning.encrypted_content"]` |
| Tool/search outputs | Chat `IncludeOption` only (see SDK `IncludeOptionMap`) | Different include vocabulary |

**Rules:**
1. Request encrypted traces via `use_encrypted_content=True` only. Never pass `reasoning.encrypted_content` in Chat `include` — the SDK raises `ValueError: Invalid include option` before the RPC.
2. Chat `include` accepts only Chat `IncludeOption` values (`inline_citations`, `web_search_call_output`, `x_search_call_output`, `code_execution_call_output`, `collections_search_call_output`, `attachment_search_call_output`, `mcp_call_output`, `verbose_streaming`). Re-check `IncludeOptionMap` when upgrading `xai-sdk`.
3. Enable encrypted capture only when reasoning effort is truthy **and not** `"none"`.
4. `store_messages` / `previous_response_id` are valid Chat params for continuity; stateless agent runs may force `store_messages=False`.
5. `xai_sdk.Client(timeout=...)` / `AsyncClient(timeout=...)` sets the **total gRPC RPC deadline**, not an idle hang timer. Long tool/reasoning loops can hit `DEADLINE_EXCEEDED` at ~120s if given a short interactive timeout (official generate-text examples use `timeout=3600` for reasoning models). Do not "fix" a client deadline by retrying the same short timeout; configure distinct deadlines per workload (short interactive vs long agent loops). See [xai-api-mastery](references/xai-api-mastery.md).

## Displayable reasoning traces

Encrypted blocks are for continuity and audit, not for user-facing trace UIs:
- **xAI Chat SDK:** read `reasoning_content` / `reasoning_summary` from the sample or stream chunk.
- **OpenRouter:** read `message.reasoning` and displayable `reasoning_details` (`reasoning.summary`, `reasoning.text`), falling back to `message.reasoning` when details are encrypted-only.
- Persist displayable summaries cleanly on the chat message metadata alongside tool steps so the traces UI never degrades to tool-count-only when the provider returned a summary.

## Prompt caching

Provider caches reuse only an exact leading prefix, and misses are invisible unless measured. Keep system text byte-stable (no dates, tickers, quotes, or volatile per-run state in `role=system`), append only, and derive the cache key from the leading system prefix plus owner scope (never hash the first user message; omit the key when no leading system message exists). Send the key via the provider's header/field (e.g., `x-grok-conv-id` for xAI, `session_id` for OpenRouter without hashing the model id into it when retries share a host). Measure hit rates (`cached_tokens` / input tokens) after prompt or routing changes. See [prompt-cache-optimization](references/prompt-cache-optimization.md).

## Speech and Voice Rules

- Route product STT, TTS, and image generation through one shared scheduler/rate limiter so a single global budget sees every call across workers (never a process-local limiter).
- Keep realtime voice sessions under explicit shared leases that refresh on reconnect/rotation and release cleanly on teardown.
- Preserve `tool_call_id`, turn ids, user attribution, and timeout settings across voice and tool paths.

## Verification Checklist

- Current callsites and tests searched.
- Official provider docs / live model metadata checked and URLs cited.
- Router owns model id resolution, ZDR/privacy policy, and provider-specific knobs.
- Wire ids are canonical bare ids with no undocumented routing suffix; one model per preset, transport-only retries, never retry after streamed text starts.
- Reasoning effort maps verified against live `supported_efforts`; omit-effort models asserted to skip the payload.
- Model/effort choice justified against Intelligence Index vs cost per task (Pareto), not `$/M` alone.
- Chat SDK calls never pass Responses-only `include` strings; `use_encrypted_content` gated off for `"none"` effort; long agent RPC deadlines separated from short interactive deadlines.
- Prompt cache prefixes remain byte-stable with owner-scoped cache keys.
- Structured-output paths do not suppress required search evidence; `failed_attempts` and `primary_error_type` preserved.
