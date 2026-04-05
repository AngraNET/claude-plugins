---
name: para:inbox
description: Process items in the PARA inbox, routing each capture to the correct bucket using the PARA decision tree (Organize step of CODE). Use when the user wants to clear their inbox and organize recent captures.
argument-hint: [--all | --one]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Inbox — The "O" in CODE (Organize)

Process raw captures from the inbox using Tiago Forte's official PARA routing decision tree.

> "With some practice, this decision will only take a few seconds." — Tiago Forte

## The Official PARA Routing Decision (in order)

For every item, cascade through these questions:

1. **What project would this be useful for?** → File in that Project
2. If no project fits → **Which area will this be useful for?** → File in that Area
3. If no area fits → **Which resource does this belong to?** → File in that Resource folder
4. If none of the above → **Don't save it** (or archive it)

This order is intentional. Information has the most value when it's closest to an active project.

## Arguments: $ARGUMENTS
- `--all`: process all items without pausing between each
- `--one`: process only the next item, then stop
- Default: interactive, one at a time

## Instructions

1. Read `para-dir` from settings (default: `~/para`)
2. List all `.md` files in `{para-dir}/00-inbox/` sorted by `captured-at` oldest first
3. If inbox is empty: "Inbox is empty. Nothing to process." and stop.

4. For each item, show:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Inbox item {N} of {total}
Captured: {captured-at}  Source: {source-ref}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{content}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Route this to:
  [P] A Project     → most actionable, directly useful now
  [A] An Area       → relevant to ongoing responsibility
  [R] Resources     → interesting topic, no current action
  [S] Someday/Maybe → want to revisit but not now
  [X] Don't save    → no longer relevant
  [K] Skip          → leave in inbox for later
```

5. **Based on choice:**

   **P - Project**: Show list of active projects. User picks one (or "new project").
   - Append under `## Notes` in project `CLAUDE.md`: `### Capture — {date}\n{content}`
   - Delete inbox file.

   **A - Area**: Show list of areas. User picks one.
   - Append to area `CLAUDE.md` notes section.
   - Delete inbox file.

   **R - Resource**: Ask for topic name (show existing topics, allow new).
   - If topic exists: append as dated note.
   - If new: create resource directory and `CLAUDE.md`.
   - Delete inbox file.

   **S - Someday/Maybe**: Ask for brief label.
   - Move file to `{para-dir}/00-inbox/someday-maybe/` with the label added to frontmatter.
   - These surface during monthly reviews.

   **X - Don't save**: Confirm once ("This will be deleted. Confirm? y/n"), then delete.

   **K - Skip**: Leave in inbox, move to next item.

6. After all items, show summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Inbox cleared: {N} items processed
  → {n} filed to projects
  → {n} filed to areas
  → {n} filed to resources
  → {n} moved to Someday/Maybe
  → {n} deleted
  Inbox remaining: {n} items
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
