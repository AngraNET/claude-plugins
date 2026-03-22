---
name: para:email
description: Read or compose emails in the context of a PARA project. Use when the user wants to find emails related to a project, compose an email with project context, or log a key email decision to a project.
argument-hint: [read <project-name> | compose <project-name> | log <project-name>]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Email Integration

Surface and compose emails in the context of PARA projects.

Requires: Gmail MCP server configured in `.mcp.json` with valid credentials.

## Arguments

$ARGUMENTS

## Subcommands

### `read <project-name>`

1. Find the project `_index.md` — read its title, goal, tags, and `email-threads` list
2. Search Gmail via the Gmail MCP:
   - Search for project title in subject/body
   - Fetch any threads listed in `email-threads`
   - Date range: from project `created` date to today
3. Display summaries of matching threads, grouped by recency:

```
Emails for: Website Redesign
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recent (last 7 days):
  ● "Wireframe feedback" — Sarah Chen, 2 days ago (3 messages)
  ● "Budget approval needed" — John Smith, 1 day ago (1 message)

Older:
  ● "Kickoff meeting notes" — Team, 2 weeks ago (5 messages)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

4. Ask: "Open a thread to read in full? Or log a decision?"

### `compose <project-name>`

1. Read the project `_index.md` for context
2. Ask the user for:
   - To (recipient email or name)
   - Subject (pre-fill with project name if empty)
   - What to communicate (user describes in natural language)
3. Draft the email using project context (goal, current status, next-action)
4. Show draft to user for review/edit
5. Ask: "Send this email? (y/n)"
6. If yes, send via Gmail MCP
7. Ask: "Log this thread to the project? (y/n)" — if yes, append thread ID to `email-threads` in `_index.md`

### `log <project-name>`

1. Show recent email threads for this project (same as `read`)
2. For selected thread(s), ask: "What was the key decision or outcome from this thread?"
3. Append to the project `_index.md` notes section:

```markdown
### Email Decision — {date}
Thread: "{subject}"
Decision: {user's summary}
```

4. Also append thread ID to `email-threads` in `_index.md` if not already there
