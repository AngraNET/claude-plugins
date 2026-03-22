---
name: para:tasks
description: View, add, complete, or link tasks to PARA projects. Use when the user wants to manage tasks tied to their projects or see what actions are pending.
argument-hint: [list [<project-name>] | add <project-name> <task> | done <task-id> | today]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Task Management

Manage tasks linked to PARA projects. Supports Google Tasks and Todoist backends.

Requires: Google Tasks or Todoist MCP server configured in `.mcp.json`.

## Arguments

$ARGUMENTS

## Subcommands

### `list [<project-name>]`

- If project name given: show all open tasks for that specific project
- If no project name: show all open tasks across all active projects, grouped by project

```
Tasks — All Active Projects
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Website Redesign
  ☐ Review wireframes with design team        due: 2026-03-25
  ☐ Get budget approval from John             no due date
  ☐ Write copy for homepage hero              due: 2026-03-28

Q2 Planning
  ☐ Schedule kickoff with stakeholders        due: 2026-03-24

Marathon Training 2026
  ☐ Book physio appointment                   no due date
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 5 open tasks
```

### `today`

Show only tasks due today or overdue across all projects.

### `add <project-name> <task>`

1. Find the project `_index.md` to get its `task-list-id`
2. If no `task-list-id` exists, create a new task list in the task backend named after the project, and save the ID
3. Create the task in the backend under that project's list
4. Ask: "Due date? (optional, press enter to skip)"
5. Append the task ID to the project `_index.md` (or update the list reference)
6. Update `next-action` in `_index.md` if this is the first task or user confirms it as the next action
7. Confirm: "Task added to {project-name}"

### `done <task-id or task-name>`

1. Look up the task by ID or fuzzy name match
2. Mark it complete in the task backend via MCP
3. Read the project `_index.md` and recalculate `completion-pct` based on ratio of complete tasks
4. Update `last-updated` in `_index.md`
5. If the completed task was the `next-action`, ask: "What's the new next action for this project?"
6. Confirm: "Marked complete: {task name}"
