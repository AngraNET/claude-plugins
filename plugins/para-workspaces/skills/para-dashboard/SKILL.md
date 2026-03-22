---
name: para
description: Show the PARA dashboard — an overview of all active Projects (with deadlines and status), Areas of responsibility, Resources, and inbox items pending processing. Use this when the user asks what they are working on, wants to see their priorities, or needs a status overview.
argument-hint: [--brief | --full]
allowed-tools: [Read, Glob, Grep, Bash]
---

# PARA Dashboard

Show a live status dashboard for the user's PARA system.

## Arguments

$ARGUMENTS (optional: `--brief` for summary only, `--full` for all details)

## Instructions

1. Read the PARA settings from `~/.claude/para-workspaces.local.md` to find `para-dir` (default: `~/para`)

2. Run the stats script if it exists:
   ```
   bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/para-stats.sh
   ```
   Otherwise, manually count items in each PARA bucket.

3. Read all `_index.md` files under `1-projects/` and display:
   - Project name, status, goal (one line), deadline, completion-pct, next-action
   - Flag projects past their deadline with ⚠ OVERDUE
   - Flag projects not updated in >14 days with ⚡ STALE

4. List areas from `2-areas/` with their standard and last-reviewed date

5. Show resource count by topic from `3-resources/`

6. Show inbox count from `0-inbox/` — if >0 items, suggest running `/para:inbox`

7. Show archive count from `4-archives/`

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PARA Dashboard  —  {today's date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 PROJECTS (N active)
  ● Project Name          [active]  35%  Due: 2026-04-15  → Next: review wireframes
  ⚠ Overdue Project       [active]   0%  Due: 2026-03-01  → Next: not defined
  ⚡ Stale Project         [paused]  80%  Due: 2026-05-01  → Next: write final report

🗂 AREAS (N)
  • Health & Fitness        Standard: exercise 4x/week    Last reviewed: 2026-03-01
  • Team Management         Standard: 1:1s weekly          Last reviewed: 2026-02-15

📚 RESOURCES (N topics)
  Topics: Frontend Development, GTD, Cooking, Finance

📥 INBOX  →  N items pending  [run /para:inbox to process]

🗃 ARCHIVES  →  N items
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If `--full` is passed, also show full notes for each project.
If `--brief` is passed, show only counts and the most urgent project.

If the PARA directory does not exist, suggest running `/para:setup` to initialize.
