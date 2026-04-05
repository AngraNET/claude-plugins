---
name: para:calendar
description: View, add, or link calendar events to PARA projects and areas. Supports Google Calendar and Outlook Calendar. Use when the user wants to see their schedule in PARA context, add a calendar event, or connect a meeting to a project.
argument-hint: [view today|week|<project-name> | add <title> | link <project-name>]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Calendar Integration

Bridge your calendar with PARA projects and areas.

Supports two backends — detect from `~/.claude/para-workspaces.local.md`:
- `calendar-backend: google` → use the `google-calendar` MCP server
- `calendar-backend: outlook` → use the `microsoft-graph` MCP server

If `calendar-backend` is not set or `none`, tell the user:
> "No calendar backend is configured. Run `/para:setup --reset` to set one up."

## Arguments

$ARGUMENTS

## Backend Detection

At the start of every subcommand:
1. Read `~/.claude/para-workspaces.local.md` and extract `calendar-backend`
2. Route all calendar MCP calls to the correct server:
   - `google` → MCP server `google-calendar`, tools: `list_events`, `create_event`
   - `outlook` → MCP server `microsoft-graph`, tools: `list_calendar_events`, `create_calendar_event`

## Permission Escalation (Outlook only)

Read operations require only `Calendars.Read` — always available.

Before any write operation (`add`, `update`, `delete`), check if `Calendars.ReadWrite` is in `MS_SCOPES`:

```bash
echo $MS_SCOPES | grep -q "Calendars.ReadWrite"
```

If missing, tell the user:
> "Creating or modifying calendar events requires the **Calendars.ReadWrite** permission, which hasn't been granted yet.
> Grant it now? (y/n)"

If yes, run:
```bash
source ~/.bashrc
python3 ~/.claude/ms-add-scope.py Calendars.ReadWrite
```

Then tell the user: "Open the URL in your browser to approve. When done, say 'done'."
After approval: `source ~/.bashrc` and proceed.

---

## Subcommands

### `view today`

1. Fetch today's events via the configured backend:
   - **Google:** `list_events` with `timeMin` and `timeMax` for today
   - **Outlook:** `list_calendar_events` with `startDateTime` and `endDateTime` for today
2. For each event, check if it matches any PARA project:
   - Look at `calendar-events` in all project `CLAUDE.md` files
   - Or fuzzy match event title against project names
3. Display:

```
Today — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  9:00  Team Standup (30m)          → [Team Management area]
 10:30  Design Review               → [Website Redesign project]
 14:00  1:1 with Alex (60m)         → [Team Management area]
 16:00  Focus time (no events)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Unlinked events are shown without annotation. Suggest linking them.

---

### `view week`

Same as `view today` but for the full current week. Group by day.

---

### `view <project-name>`

1. Read the project `CLAUDE.md` to get `calendar-events` list
2. Fetch those specific events from the calendar backend by ID
3. Also search for events with the project name in the title
4. Display upcoming and recent past events for this project

---

### `add <title>`

1. Check write permission (see Permission Escalation above) before proceeding
2. Ask the user for:
   - Date and time
   - Duration
   - Description (optional)
   - Link to a PARA project? (optional — show project list)
3. Create the event via the configured backend
4. If linked to a project, append the event ID to `calendar-events` in `CLAUDE.md`
5. Confirm: "Event created: {title} on {date}"

---

### `link <project-name>`

1. Show today's and this week's unlinked calendar events
2. Ask user which event(s) to link to the project
3. Update the project `CLAUDE.md` `calendar-events` list with the selected event IDs
4. Confirm linkage
