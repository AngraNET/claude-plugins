---
name: para:email
description: Read or compose emails in the context of a PARA project. Supports Gmail and Outlook (Microsoft 365). Use when the user wants to find emails related to a project, compose an email with project context, or log a key email decision to a project.
argument-hint: [read <project-name> | compose <project-name> | log <project-name>]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Email Integration

Surface and compose emails in the context of PARA projects.

Supports two backends — detect from `~/.claude/para-workspaces.local.md`:
- `email-backend: gmail` → use the `gmail` MCP server
- `email-backend: outlook` → use the `microsoft-graph` MCP server

If `email-backend` is not set or `none`, tell the user:
> "No email backend is configured. Run `/para:setup --reset` to set one up."

## Arguments

$ARGUMENTS

## Backend Detection

At the start of every subcommand:
1. Read `~/.claude/para-workspaces.local.md` and extract `email-backend`
2. Route all email MCP calls to the correct server:
   - `gmail` → MCP server `gmail`, tools: `search_emails`, `get_thread`, `send_email`
   - `outlook` → MCP server `microsoft-graph`, tools: `search_messages`, `get_message_thread`, `send_message`

## Permission Escalation (Outlook only)

Read operations require only `Mail.Read` — always available.

Before any write operation (`compose`, `send`, `reply`), check if `Mail.Send` is in `MS_SCOPES`:

```bash
echo $MS_SCOPES | grep -q "Mail.Send"
```

If missing, tell the user:
> "Sending email requires the **Mail.Send** permission, which hasn't been granted yet.
> Grant it now? (y/n)"

If yes, run:
```bash
source ~/.bashrc
python3 ~/.claude/ms-add-scope.py Mail.Send Mail.ReadWrite
```

Then tell the user: "Open the URL in your browser to approve. When done, say 'done'."
After approval: `source ~/.bashrc` and proceed.

---

## Subcommands

### `read <project-name>`

1. Find the project `_index.md` — read its title, goal, tags, and `email-threads` list
2. Search emails via the configured backend:
   - **Gmail:** `search_emails` with query `subject:{project-title} OR body:{project-title}`
   - **Outlook:** `search_messages` with `$search="{project-title}"`
   - Also fetch any threads listed in `email-threads` directly by ID
3. Display summaries grouped by recency:

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

---

### `compose <project-name>`

1. Check write permission (see Permission Escalation above) before proceeding
2. Read the project `_index.md` for context (goal, status, next-action)
3. Ask the user for:
   - To (recipient email or name)
   - Subject (pre-fill with project name if empty)
   - What to communicate (user describes in natural language)
4. Draft the email using project context
5. Show draft to user for review/edit
6. Ask: "Send this email? (y/n)"
7. If yes, send via the configured backend
8. Ask: "Log this thread to the project? (y/n)" — if yes, append thread ID to `email-threads` in `_index.md`

---

### `log <project-name>`

1. Show recent email threads for this project (same as `read`)
2. For selected thread(s), ask: "What was the key decision or outcome from this thread?"
3. Append to the project `_index.md` notes section:

```markdown
### Email Decision — {date}
Thread: "{subject}"
Decision: {user's summary}
```

4. Append thread/message ID to `email-threads` in `_index.md` if not already there
