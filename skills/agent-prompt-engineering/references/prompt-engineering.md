---
name: prompt-engineering
description: "Construct and optimize effective prompts for LLM API calls, agent workflows, and chat interactions across fast, medium, and high-tier models. Use when the user wants to write, rewrite, audit, or improve any prompt — system prompt, API call, agent instruction, or chat query. Also use when designing prompt chains, evaluation criteria, or context for multi-step workflows. Tailor every prompt to the right tier for speed, cost, and quality."
---

# Prompt Engineering

Turn raw intent into clear, goal-driven guidance that LLMs follow reliably and efficiently.
Prompt engineering is **context and outcome engineering**: curating the right goals, information, tools, and advice so the model can adapt intelligently and deliver what is needed.

Choose the model tier that fits the task unless the user specified one:

- **Fast tier**: Quick, low-complexity tasks (single-document summaries, simple extraction, rapid answers). Keep prompts concise and direct.
- **Medium tier**: Synthesis of a few documents, moderate analysis, light reasoning, or search. Balanced guidance for thoughtful, efficient work.
- **High tier**: Complex, novel, or deep tasks (multi-step planning, ambiguous problems, long-horizon analysis). Allow room for exploration and judgment.

## Workflow

1. **Understand:** What is the goal, what does success look like, which tier fits, and what tools or context are available?
2. **Apply:** Use the principles below. Match depth to the chosen tier; never over-structure a fast-tier task.
3. **Produce:** Output the prompt in a clean code block, labeling system vs user prompt when both are needed.
4. **Explain:** Summarize main changes and why they help in 2 to 4 sentences. Ask clarifying questions only if critical ambiguity remains.

## Principles

### Start with the Goal and Success Criteria
Lead every prompt with a clear, outcome-focused north star. Tell the model what needs to be achieved and how to know it worked.

### Give Guidelines and Advice, Not Brittle Rules
Offer clear principles and suggestions instead of rigid if-else scripts when judgment is required. State gaps transparently rather than speculating.

### Describe Tools Clearly and Naturally
Explain what tools are available, when they are useful, and practical bounds without forcing a rigid sequence unless order is an invariant.

### Organize for Readability and Flow
Use natural Markdown sections or paragraphs that serve the goal. Keep fast-tier prompts short and paragraph-style; place static context early (for prompt caching) and volatile input near the end.

### Use Examples When They Add Value
Include 1 to 3 short, realistic examples only when format or style really matters. Show what good looks like rather than overfitting one specific task.

### Calibrate Depth to Tier and Complexity
- **Fast:** Direct and minimal; no deep reasoning requests.
- **Medium:** Balanced reasoning and tool use as needed.
- **High:** Explore edge cases, alternatives, and synthesis.

### Prune and Structure Context
Keep only what matters; delete duplicate and unnecessary words while preserving required context.

### Specifying Output Format
When a task requires a specific output format (JSON, structured data, bullet lists, tables), place the output instructions **at the bottom of the prompt**, immediately before or after the query. Use direct phrasing ("Respond only with the following JSON structure.").
