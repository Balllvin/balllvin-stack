---
name: agent-plugins
description: >-
  Use when creating, editing, scoping, wording, or reviewing an agent harness
  plugin, or when adding a runtime feature that plugins call. Covers the single
  YAML manifest as source of truth, model-facing card, self-test, discovery,
  versioned lifecycle, and held-out evals. Triggers: "write a plugin", "add a
  plugin", "plugin skill", "harness plugin", "plugin manifest", "edit a plugin
  in use", "how broad should this plugin be".
---

# Agent Plugins

A plugin is one job with one done-condition. It has five parts: a YAML manifest, the action code, a card the model reads, state, and a self-test. The YAML manifest is the single source of truth across runtimes (both sandboxed code runners and host agent harnesses). Keep one compiler/importer per target runtime; never maintain a second hand-written copy of the actions.

## Pages

| Page | Open it for |
|---|---|
| [concepts](references/concepts.md) | What a plugin is, the five parts, runtime targets, wake vs inject |
| [design and scope](references/design-and-scope.md) | How broad or narrow, when to split, shared workspaces |
| [wording](references/wording.md) | Names, 160-character descriptions, typed failures, caps, two failure kinds |
| [manifest](references/manifest.md) | Full field list, lint rules, and a complete YAML example |
| [lifecycle](references/lifecycle-editing.md) | Draft, validate, promote, pin, rollback, deprecation |
| [options](references/options.md) | Every field, its default, and when to change it |
| [eval](references/eval.md) | Held-out eval, three baseline runs, the spread as the noise floor |
| [code plugin](references/code-plugin-example.md) | Worked example: run, wake, edit failing files, rerun, done when green |
| [checklist](references/checklist.md) | The pass before you promote or open a PR |

## Start here

1. Name the job and the done-condition in one sentence each. If you need two done-conditions, you need two plugins ([design and scope](references/design-and-scope.md)).
2. Fill the manifest first ([manifest](references/manifest.md), [options](references/options.md)).
3. Write the loop in a sibling `card-loop.md` by hand. Lint must pass. Failures fail; they do not warn ([wording](references/wording.md)).
4. Write the code and the self-test. The self-test must fail when the plugin is broken, and it must pass when the work itself is allowed to fail in a declared way (`work_failed`).
5. Run the checklist. Promote only after schema validation and the self-test pass ([lifecycle](references/lifecycle-editing.md)).
