# What a plugin is

A plugin does one job and has one done-condition. "Run the tests and leave them green" is a plugin. "Run the tests, and also value this company" is two plugins.

The five parts:

1. **Manifest.** A small YAML file. It names the plugin, its version, a one-line when-to-use, the actions, the result schema, permissions, budget, wake events, retry and idempotency, and where state lives. This file is the source of truth across runtimes.
2. **Code.** The functions that implement each action. A generic runtime wrapper loads `entrypoint` and registers each action from the manifest, or a build-time generator imports the manifest into host tool definitions. Never branch on plugin id inside the generic wrapper.
3. **Card.** What the model reads. The actions, args, and results section is generated from the manifest so it cannot drift. The loop section is hand-written in a sibling `card-loop.md`: the order of actions, and a line that starts with `Done when:`. The loop fits on about one screen. It is not a field in the YAML. A linter checks that every named action exists and that the done line is present. A lint failure fails the build; it does not warn.
4. **State.** Where the plugin keeps work in progress: a workspace path, a store row, or both. The manifest points at it. A running job pins the plugin version it started with, so an edit mid-run cannot change the job under it.
5. **Self-test.** A small, deterministic check the plugin runs on itself before promote, and that the harness can run again later. It proves the plugin works (`ok`, `work_failed`, `plugin_error`), not that a particular user job succeeded.

## Target runtimes

- **Sandboxed runner:** An isolated VM/container turn where a generic runtime wrapper reads promoted manifests and registers each action as a tool without per-plugin wrapper code.
- **Host harness:** A host-side tool registry / compiled kernel where a generator compiles first-party YAML manifests into typed tool definitions and promoted user-authored plugins mount as host tools.
- **Repo agent plugins:** Editor/CLI plugins (like MCP configs or repo rules) are developer tooling, not product runtime plugins, and do not use this YAML format.

Do not invent extra per-consumer formats or hand-edit generated tool catalogs.

## Wake, inject, and followup

A wake starts or continues an agent turn after the plugin finishes asynchronous work the turn did not wait for.

- **Default wake path:** The host job posts a webhook when the job finishes, keyed by `retry_key` so duplicate delivery cannot double-wake.
- **In-session shortcut:** When a job finishes inside the active session, wake via an explicit followup message carrying the same canonical result object the webhook would post, plus a typed source kind. If the followup hook is unavailable, skip the shortcut and let the host webhook wake the next turn.
- **Never treat context injection as a wake:** `inject()` only appends context for the next model request; an idle agent stays idle and a one-shot session exits before a long job ends.

## Discovery

Every plugin publishes its `when` line into a short index. The model (and a person) should be able to scan the index and pick a plugin without opening the card. Keep `when` to one sentence. If two plugins could claim the same sentence, rewrite both.

## What a plugin is not

A plugin is not a custom bot, a specialist prompt, a scheduled automation, or a skill file. Those already have homes. A plugin is also not a GUI command, panel, or composer pill.
