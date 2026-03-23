---
name: para:project
description: Create, view, update, list, or close PARA projects. Projects must have a specific outcome and an endpoint. Use when the user wants to manage their projects — creating new ones, checking status, updating progress, or closing completed ones.
argument-hint: [new <name> | view <name> | update <name> | list | close <name> | someday]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Project Management

Manage projects in the PARA system.

> "A project is a short-term effort with a specific goal and an endpoint." — Tiago Forte

**The critical test:** Does it have a finish line? → Project. Does it continue indefinitely? → Area.

**Why this matters:** Without breaking responsibilities into Projects, you can't know your true workload or connect daily effort to long-term goals.

## Arguments: $ARGUMENTS

## Subcommands

### `new <name>`

1. Ask the user for:
   - **Goal**: What specific outcome will this achieve? (must be a finish line, not ongoing)
   - **Deadline**: When does this need to be done? (required — even an estimate)
   - **Area**: Which area of responsibility does this serve? (optional)
   - **Priority**: high / medium / low (default: medium)
   - **Next action**: What is the very first physical, concrete action?

2. If the user can't define a specific outcome or deadline, gently ask: "Could this be an Area of Responsibility instead? Areas are ongoing standards with no endpoint."

3. Determine the next project number:
   - List all directories in `{para-dir}/1-projects/` matching the pattern `[0-9][0-9]-*`
   - Find the highest two-digit prefix (e.g. `03` from `03-my-project`)
   - Increment by 1 and zero-pad to 2 digits (e.g. `04`)
   - If no numbered projects exist yet, start at `00`
   - Final folder name: `{NN}-{slugified-name}` (e.g. `04-my-project`)

4. Create directory: `{para-dir}/1-projects/{NN}-{slugified-name}/`
   Also create: `{para-dir}/1-projects/{NN}-{slugified-name}/packets/` (for Intermediate Packets)

5. Write `_index.md`:

```markdown
---
type: project
title: "{name}"
status: active
goal: "{goal}"
outcome: ""
deadline: {YYYY-MM-DD}
created: {today}
last-updated: {today}
area: "{area}"
next-action: "{next-action}"
completion-pct: 0
priority: {priority}
tags: []
task-list-id: ""
calendar-events: []
email-threads: []
review-log: []
---

# {name}

## Goal

{One-sentence specific outcome — the finish line}

## Background

{Why does this project exist?}

## Key Decisions

## Notes

```

6. Confirm and remind: "Add tasks with `/para:tasks add {name} <task>` — or capture ideas with `/para:capture`"

---

### `view <name>`

1. Find the project (fuzzy match)
2. Read `_index.md` and display:
   - All frontmatter fields in a readable layout
   - Days until deadline (or overdue by N days)
   - Full notes content
   - Intermediate Packets in `packets/` directory
   - Tasks from backend if MCP available
   - Upcoming linked calendar events if MCP available
   - Last 3 review log entries

---

### `update <name>`

1. Read current `_index.md`
2. Ask which fields to update (show current values)
3. Common updates: status, completion-pct, next-action, deadline, notes, goal
4. Update `last-updated` to today
5. If `completion-pct` reaches 100 or status changes to `complete`: offer to archive

---

### `list`

Read all `_index.md` files in `1-projects/`. Display sorted by priority then deadline:

```
Active Projects
──────────────────────────────────────────────────────────────
Name                    Status       %    Deadline     Next Action
Website Redesign        active       35%  2026-04-15   Review wireframes
⚠ Tax Filing            active        0%  2026-04-15   Gather receipts [OVERDUE]
Q2 Planning             active       10%  2026-04-30   Schedule kickoff

Someday/Maybe
──────────────────────────────────────────────────────────────
Learn Spanish                                            (no deadline)
Renovate bathroom                                        (no deadline)
```

---

### `someday`

List all projects with `status: someday-maybe`. These are ideas you're not committed to yet.

For each:
- Promote to active (set deadline + next action)
- Archive (no longer relevant)
- Keep as Someday/Maybe

> Someday/Maybe items are reviewed during the monthly review.

---

### `close <name>`

1. Read the project `_index.md`
2. Ask: "What was the final outcome?" (record in `outcome` field)
3. Set `status: complete`, `completion-pct: 100`, `last-updated: today`
4. Ask: "Archive this project? (y/n)"
5. If yes, run archive flow — moves to `4-archives/{YYYY-MM}/{name}/`
6. Celebrate: "Project '{name}' complete. Well done."
