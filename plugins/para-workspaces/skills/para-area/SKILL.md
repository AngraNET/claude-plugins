---
name: para:area
description: Create, view, update, or list PARA Areas of Responsibility. Areas are ongoing standards to maintain with no end date (e.g. Health, Finances, Team Management). Use when the user wants to manage their ongoing responsibilities.
argument-hint: [new <name> | view <name> | update <name> | list]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Area Management

Manage areas of responsibility. Areas are ongoing commitments with no end date — they define standards you maintain, not outcomes you achieve.

## Arguments

$ARGUMENTS

## Subcommands

### `new <name>`

1. Ask the user for:
   - **Standard**: What does success look like for this area? (e.g., "Exercise 4x/week, annual checkups")
   - **Review frequency**: How often to review? (weekly / monthly / quarterly)
   - **Description**: Brief description of this area

2. Create directory: `{para-dir}/2-areas/{slugified-name}/`

3. Write `_index.md`:

```markdown
---
type: area
title: "{name}"
standard: "{standard}"
review-frequency: {frequency}
last-reviewed: {today}
created: {today}
tags: []
linked-projects: []
---

# {name}

## Standard

{What does maintaining this area well look like?}

## Current State

## Notes

```

4. Confirm and suggest: "Link projects to this area by setting `area: {name}` in their `_index.md`"

---

### `view <name>`

1. Find and read the area `_index.md`
2. Display full area card including standard, review frequency, last reviewed date
3. Find all projects in `1-projects/` where `area:` matches this area name
4. Show those linked projects with their status and deadlines

---

### `update <name>`

1. Read current `_index.md`
2. Interactively update: standard, review-frequency, notes
3. Update `last-reviewed` if the user is doing a review

---

### `list`

1. Read all areas from `2-areas/`
2. Display table:

```
Area                    Review Freq    Last Reviewed    Linked Projects
────────────────────────────────────────────────────────────────────────
Health & Fitness        monthly        2026-03-01       Marathon Training
Team Management         weekly         2026-03-15       Q2 Planning
Finances                monthly        2026-02-01       (none)
```

3. Highlight areas not reviewed recently (overdue by their frequency).
