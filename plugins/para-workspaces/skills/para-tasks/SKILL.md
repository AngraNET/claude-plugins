---
name: para:tasks
description: View, add, complete, or link tasks to PARA projects. Use when the user wants to manage tasks tied to their projects or see what actions are pending.
argument-hint: [list [<project-name>] | add <project-name> <task> | done <task-id> | today]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Task Management

Manage tasks linked to PARA projects. Supports Google Tasks, Todoist, and Microsoft To Do backends.

Detect backend from `~/.claude/para-workspaces.local.md`:
- `task-backend: google-tasks` → use the `google-tasks` MCP server
- `task-backend: todoist` → use the `todoist` MCP server
- `task-backend: microsoft-todo` → use the `microsoft-graph` MCP server (To Do API)
- `task-backend: none` → inform user no backend is configured

## Arguments

$ARGUMENTS

## Backend Detection

At the start of every subcommand:
1. Read `~/.claude/para-workspaces.local.md` and extract `task-backend`
2. Route all task MCP calls:
   - `google-tasks` → MCP server `google-tasks`, tools: `list_tasks`, `create_task`, `complete_task`
   - `todoist` → MCP server `todoist`, tools: `get_tasks`, `add_task`, `close_task`
   - `microsoft-todo` → MCP server `microsoft-graph`, tools: `list_todo_tasks`, `create_todo_task`, `complete_todo_task`

## Permission Escalation (Microsoft To Do only)

Read operations require only `Tasks.Read` — always available.

Before any write operation (`add`, `done`), check if `Tasks.ReadWrite` is in `MS_SCOPES`:

```bash
echo $MS_SCOPES | grep -q "Tasks.ReadWrite"
```

If missing, tell the user:
> "Adding or completing tasks requires the **Tasks.ReadWrite** permission, which hasn't been granted yet.
> Grant it now? (y/n)"

If yes, run:
```bash
source ~/.bashrc
python3 ~/.claude/ms-add-scope.py Tasks.ReadWrite
```

Then tell the user: "Open the URL in your browser to approve. When done, say 'done'."
After approval: `source ~/.bashrc` and proceed.

---

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

Q2 Planning
  ☐ Schedule kickoff with stakeholders        due: 2026-03-24
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 3 open tasks
```

---

### `today`

Show only tasks due today or overdue across all projects.

---

### `add <project-name> <task>`

1. Check write permission (see Permission Escalation above) before proceeding
2. Find the project `_index.md` to get its `task-list-id`
3. If no `task-list-id` exists, create a new task list in the backend named after the project and save the ID
4. Create the task in the backend under that project's list
5. Ask: "Due date? (optional, press enter to skip)"
6. Append the task ID to the project `_index.md`
7. Update `next-action` in `_index.md` if this is the first task or user confirms it
8. Confirm: "Task added to {project-name}"

---

### `done <task-id or task-name>`

1. Check write permission (see Permission Escalation above) before proceeding
2. Look up the task by ID or fuzzy name match
3. Mark it complete via the configured backend
4. Read the project `_index.md` and recalculate `completion-pct`
5. Update `last-updated` in `_index.md`
6. If the completed task was the `next-action`, ask: "What's the new next action for this project?"
7. Confirm: "Marked complete: {task name}"
