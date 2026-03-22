---
name: para:calendar
description: View, add, or link calendar events to PARA projects and areas. Use when the user wants to see their schedule in PARA context, add a calendar event, or connect a meeting to a project.
argument-hint: [view today|week|<project-name> | add <title> | link <project-name>]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Calendar Integration

Bridge Google Calendar with your PARA projects and areas.

Requires: Google Calendar MCP server configured in `.mcp.json` with valid credentials.

## Arguments

$ARGUMENTS

## Subcommands

### `view today`

1. Fetch today's calendar events via the Google Calendar MCP tool
2. For each event, check if it matches any PARA project:
   - Look at `calendar-events` field in all project `_index.md` files
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

Unlinked events are shown without a PARA context annotation. Suggest linking them.

### `view week`

Same as today but for the full current week. Group by day.

### `view <project-name>`

1. Read the project `_index.md` to get `calendar-events` list
2. Fetch those specific events from the calendar MCP
3. Also search for events with the project name in the title
4. Display upcoming and recent past events for this project

### `add <title>`

1. Ask the user for:
   - Date and time
   - Duration
   - Description (optional)
   - Link to a PARA project? (optional — shows project list)
2. Create the event via the Google Calendar MCP
3. If linked to a project, append the event ID to `calendar-events` in `_index.md`
4. Confirm: "Event created: {title} on {date}"

### `link <project-name>`

1. Show today's and this week's unlinked calendar events
2. Ask user which event(s) to link to the project
3. Update the project `_index.md` `calendar-events` list with the selected event IDs
4. Confirm linkage
