---
name: prompt-cache-optimization
description: >
  Build and change prompts so LLM prefill/prompt caches hit. Use when writing or
  editing system prompts, message ordering, conversation/session-id derivation, or
  provider routing that affects xAI / OpenRouter prompt caching, or when a tier
  shows a near-zero cache hit rate.
---

# Prompt cache

Provider caches reuse the exact leading prefix. Misses are invisible unless measured.

## Rules

1. Keep a byte-stable leading prefix.
   - System/developer text and static few-shots must be identical across calls that share a cache.
   - Do not put dates, tickers, live quotes, or other volatile per-run values in the system prompt. Put them in the user message.
2. Derive the conversation/session key from the system prefix + owner scope only.
   - Hash the provider, the leading system messages, and the owner scope (`application`, `caller`, `user_id`, workspace/resource id). For direct xAI calls, include the model id; for OpenRouter `session_id`, leave the model id out so retries share one host.
   - Do not hash the first user message. With no leading system message, omit the key. Do not fall back to another message.
   - Keep owner scope in the key. Different owners must never share a provider cache key.
   - Send that key to xAI as `conversation_id` (`x-grok-conv-id`) and to OpenRouter as `session_id` (max 256 chars) on both standard and agentic tool paths. No key means those fields stay off the request.
3. Append only. Do not edit, drop, or reorder earlier messages. Compact old turns into a summary block rather than sliding the leading window.
4. Order: instructions, few-shots, reference docs, then volatile input.
5. After a prompt or routing change, measure cache hit rates (`cached_tokens`, `cache_write_tokens`, input/output/total tokens, and cost). A tier near 0% is a bug unless the system prompt is tiny and the user message always changes.

## Check

- Same system + two different user messages -> same cache key.
- Two owners -> different cache keys.
- Changed system prompt -> different cache key.
- No system message -> no cache key sent.
- OpenRouter request body carries `session_id` only when the key exists.
