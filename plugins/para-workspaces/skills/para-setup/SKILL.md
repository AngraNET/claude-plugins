---
name: para:setup
description: First-time setup for PARA Workspaces. Initializes the vault, explains the CODE framework, and optionally runs the migration protocol to archive existing files. Run this first.
argument-hint: [--reset]
allowed-tools: [Read, Write, Bash]
---

# PARA Workspaces Setup

Welcome to your Second Brain. This setup walks you through initializing the PARA system based on Tiago Forte's "Building a Second Brain" methodology.

## Arguments: $ARGUMENTS
`--reset` to reconfigure an existing setup.

---

## Step 0: Explain the System (briefly)

Tell the user:

> "Building a Second Brain organizes all digital information using **PARA** — Projects, Areas, Resources, Archives — and a four-step workflow called **CODE**:
>
> - **Capture** — Save what resonates (`/para:capture`)
> - **Organize** — Route captures to the right bucket (`/para:inbox`)
> - **Distill** — Extract the essential meaning (`/para:distill`)
> - **Express** — Create output using what you've collected (`/para:express`)
>
> Everything lives in human-readable Markdown files you own completely."

Ask: "Ready to set up? (y/n)"

---

## Step 1: Choose PARA Directory

Ask: "Where should your PARA vault live? (default: ~/para)"
Save as `para-dir`.

---

## Step 2: Migration Protocol

> **Tiago Forte's official advice:** Do NOT try to reorganize existing files into PARA. Instead:
> 1. Create an "Archive" folder with today's date
> 2. Move ALL existing files into it
> 3. This creates a clean starting point — nothing is deleted, but you work forward unburdened

Ask: "Do you have existing notes or files to migrate? (y/n)"

If yes:
- Ask where they are (directory path)
- Create: `{para-dir}/04-archives/Archive-{YYYY-MM-DD}/`
- Ask: "Move all files from {path} into this archive? This is reversible — nothing gets deleted. (y/n)"
- If confirmed, run:
  ```bash
  cp -r "{source-path}/." "{para-dir}/04-archives/Archive-{YYYY-MM-DD}/"
  ```
- Confirm: "Your existing files are archived. You're starting fresh."

---

## Step 3: Scaffold Directory Structure

Create:
```
{para-dir}/
├── 00-inbox/
│   └── someday-maybe/
├── 01-projects/
├── 02-areas/
├── 03-resources/
├── 04-archives/
├── 05-reviews/
└── 06-memory/
```

Also create `{para-dir}/05-reviews/life-goals.md`:

```markdown
---
type: life-goals
last-updated: {today}
---

# Life Goals

## Short-term (1–2 years)

## Medium-term (3–5 years)

## Long-term (5+ years)

## Archived Goals
```

And `{para-dir}/05-reviews/personal-vision.md`:

```markdown
---
type: personal-vision
last-updated: {today}
---

# Personal Narrative Vision

*Describe your ideal typical day one year from now. Cover your main life areas, what you've achieved, how you spend your time. This is reviewed monthly and rewritten annually.*

```

Read the script file and write it to `~/.local/bin/start-brain.sh`, replacing `{para-dir}` with the actual vault path, then `chmod +x` it:

```
{skill-base-dir}/references/start-brain.sh
```

If `~/.local/bin` is not already in `$PATH`, add it:
```bash
grep -q '\.local/bin' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

Then create a reference note at `{para-dir}/03-resources/tools/start-brain.md`:

```markdown
---
type: resource
topic: tools
created: {today}
---

# start-brain.sh

A shell script that launches Claude Code directly inside the PARA vault.

## Location
`~/.local/bin/start-brain.sh`

## Usage
\`\`\`bash
start-brain.sh
\`\`\`

Reads `$PARA_DIR` (set during setup) so it always opens in the right vault.
Override at any time by setting `PARA_DIR` in your shell profile.
```

Also create `{para-dir}/CLAUDE.md`:

```markdown
# PARA Vault — Claude Instructions

This is a personal knowledge management vault using the PARA system (Projects, Areas, Resources, Archives) and the CODE framework (Capture → Organize → Distill → Express) from Tiago Forte's *Building a Second Brain*.

## Vault Structure

\`\`\`
00-inbox/        — Unprocessed captures, pending triage
01-projects/     — Active projects (specific outcome + end date)
02-areas/        — Ongoing responsibilities (no end date)
03-resources/    — Reference material by topic
04-archives/     — Completed/inactive items from all categories
05-reviews/      — Weekly, monthly, annual review documents + life goals
06-memory/       — Claude's persistent memory for this vault
\`\`\`

## Skills to Use

This vault has the `para-workspaces` plugin installed. Always prefer its skills over manual file edits for PARA operations:

| Task | Skill |
|------|-------|
| Quick capture / brain dump | `para-workspaces:para-capture` |
| Process inbox | `para-workspaces:para-inbox` |
| Create / update / close a project | `para-workspaces:para-project` |
| Create / update an area | `para-workspaces:para-area` |
| Create / update a resource | `para-workspaces:para-resource` |
| View dashboard / priorities | `para-workspaces:para-dashboard` |
| Search across all items | `para-workspaces:para-search` |
| Run a weekly/monthly/annual review | `para-workspaces:para-review` |
| Distill a note (Progressive Summarization) | `para-workspaces:para-distill` |
| Create output from notes | `para-workspaces:para-express` |
| Archive an item | `para-workspaces:para-archive` |
| Manage tasks | `para-workspaces:para-tasks` |

## Project File Convention — Source Repository Section

Every project `_index.md` that has an associated source repository **must** include a `## Source Repository` section near the top (after the goal, before Background). This lets Claude find the source without searching.

\`\`\`markdown
## Source Repository

| | |
|---|---|
| **VCS** | git \| mercurial \| svn \| other |
| **Remote** | \`<url>\` |
| **Local path** | \`/path/to/local/clone\` |
| **Subdirectory** | \`<subdirectory if applicable>\` |

> When asked to commit, push, or edit code for this project — use **Local path** above. Do not search.
\`\`\`

When creating a new project (`/para:project new`), Claude detects code projects automatically (by keywords such as app, plugin, script, API, repo, build, deploy, library, CLI) or asks the user. If a repository exists, it prompts for VCS type, remote URL, local path, and optional subdirectory before writing `_index.md`.

## File Conventions

- All notes are Markdown (`.md`)
- Files use YAML frontmatter for metadata
- Dates use ISO format: `YYYY-MM-DD`
- Project folders live under `01-projects/<NN>-<project-slug>/` (e.g. `00-my-project`, `01-next-project`)
- Each project has an `_index.md` as its main file

## Common Frontmatter Fields

**Projects:**
\`\`\`yaml
---
type: project
status: active          # active | on-hold | completed | cancelled
created: YYYY-MM-DD
deadline: YYYY-MM-DD    # optional
outcome: "One sentence describing the specific desired result"
area: <area-name>       # optional parent area
---
\`\`\`

**Areas:**
\`\`\`yaml
---
type: area
created: YYYY-MM-DD
last-reviewed: YYYY-MM-DD
---
\`\`\`

**Resources:**
\`\`\`yaml
---
type: resource
topic: <topic>
created: YYYY-MM-DD
---
\`\`\`

## Memory

Claude's persistent memory for this vault lives in `memory/` at the vault root (not in `~/.claude`).

On startup in this vault:
1. Derive the Claude project memory path from the vault path (replace `/` with `-` in the path, prefix with `~/.claude/projects/`, append `/memory/`).
2. Check that directory for any `.md` files.
3. If files exist, ask: "I found memory files in `~/.claude`. Move them into your PARA vault at `memory/` so they follow OneDrive? (y/n)"
4. If confirmed: move all files to `{para-dir}/06-memory/`, delete the originals from `~/.claude`, then confirm to the user.
5. Read memory from `{para-dir}/06-memory/` at the start of each session.

Always write new memories to `{para-dir}/06-memory/` and keep `{para-dir}/06-memory/MEMORY.md` up to date as the index.

## Behavioural Guidelines

- When the user mentions something actionable with a clear outcome, suggest creating a project.
- When the user mentions an ongoing responsibility, suggest creating an area.
- When the user shares reference material or a link, suggest capturing it.
- When asked "what am I working on?" or "what's my focus?", use `para-dashboard`.
- Keep note content concise — distilled, not verbose.
- Never delete files outright; archive them instead.
- Today's date is always available via the `currentDate` context injected at runtime.
```

---

## Step 4: Task Backend

Ask: "Which task backend do you want to use?"
- [1] Google Tasks (shared OAuth with Calendar/Gmail)
- [2] Todoist (separate API token)
- [3] Microsoft To Do (shared OAuth with Outlook Calendar/Mail)
- [4] None for now

---

## Step 4b: Email Backend

Ask: "Which email backend do you want to use?"
- [1] Gmail (shared OAuth with Google Calendar/Tasks)
- [2] Outlook / Microsoft 365 (shared OAuth with Outlook Calendar/Tasks)
- [3] None for now

Save as `email-backend` (gmail|outlook|none).

---

## Step 4c: Calendar Backend

Ask: "Which calendar backend do you want to use?"
- [1] Google Calendar (shared OAuth with Gmail/Tasks)
- [2] Outlook Calendar / Microsoft 365 (shared OAuth with Mail/Tasks)
- [3] None for now

Save as `calendar-backend` (google|outlook|none).

---

## Step 5: Integration Credentials

### Google credentials (if any Google service was selected)

- Explain: "You need a Google OAuth refresh token. Set up a Google Cloud project, enable the Calendar/Gmail/Tasks APIs, create OAuth2 credentials (Desktop app), and complete the OAuth flow."
- Ask for: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`
- Suggest adding to `~/.bashrc` or `~/.zshrc`

### Microsoft credentials (if any Microsoft/Outlook service was selected)

First, deploy the OAuth helper scripts:

```bash
cp {skill-base-dir}/references/ms-oauth.py ~/.claude/ms-oauth.py
cp {skill-base-dir}/references/ms-add-scope.py ~/.claude/ms-add-scope.py
chmod +x ~/.claude/ms-oauth.py ~/.claude/ms-add-scope.py
```

Then read the companion file and follow its steps:

```
{skill-base-dir}/references/ms-setup.md
```

Where `{skill-base-dir}` is the base directory shown in the skill header at the top of this conversation (e.g. `~/.claude/plugins/cache/.../skills/para-setup/`). Use the Read tool to load it before proceeding.

### Todoist credentials (if Todoist was selected)

- Ask for: `TODOIST_API_TOKEN` (from todoist.com/app/settings/integrations/developer)

### Notion (optional)

- Ask: "Enable Notion sync? (y/n)"

---

## Step 6: Dashboard Preference

Ask: "Show PARA summary at the start of each Claude session? (y/n)"

---

## Step 7: Export PARA_DIR to shell

Add the following to `~/.bashrc` (replace if a previous `PARA_DIR` export already exists):

```bash
export PARA_DIR="{para-dir}"
```

Run:
```bash
grep -q "^export PARA_DIR=" ~/.bashrc \
  && sed -i "s|^export PARA_DIR=.*|export PARA_DIR=\"{para-dir}\"|" ~/.bashrc \
  || echo 'export PARA_DIR="{para-dir}"' >> ~/.bashrc
```

Tell the user: "PARA_DIR has been added to ~/.bashrc. It will be available in all new shells. For the current session, run: `export PARA_DIR=\"{para-dir}\"`"

---

## Step 8: Write Settings

Write `~/.claude/para-workspaces.local.md`:

```markdown
---
enabled: true
para-dir: "{para-dir}"
task-backend: {google-tasks|todoist|microsoft-todo|none}
email-backend: {gmail|outlook|none}
calendar-backend: {google|outlook|none}
show-dashboard-on-start: {true|false}
inbox-reminder: true
log-sessions: false
review-day: sunday
notion-enabled: {true|false}
---

# PARA Workspaces Configuration
```

---

## Step 9: Write `.mcp.json` and enable MCP servers

Based on the backends the user selected, write `{para-dir}/.mcp.json` containing only the relevant servers. `filesystem` is always included. Map backends to servers:

- `email-backend: outlook` OR `calendar-backend: outlook` OR `task-backend: microsoft-todo` → include `outlook`
- `email-backend: gmail` → include `gmail`
- `calendar-backend: google` → include `google-calendar`
- `task-backend: google-tasks` → include `google-tasks`
- `task-backend: todoist` → include `todoist`
- `notion-enabled: true` → include `notion`

Copy only the matching server entries from the plugin's master `.mcp.json` (at `{skill-base-dir}/../../.mcp.json`) into `{para-dir}/.mcp.json`. Always include `filesystem`.

Then update `{para-dir}/.claude/settings.local.json` to add `enabledMcpjsonServers` containing the names of all servers you just wrote (so Claude Code approves them without prompting). Create the file if it doesn't exist, or merge into the existing `enabledMcpjsonServers` array if it does:

```json
{
  "enabledMcpjsonServers": ["filesystem", "outlook"]
}
```

---

## Step 10: Confirm

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARA Workspaces ready!

Vault:     {para-dir}
Tasks:     {task-backend}
Email:     {email-backend}
Calendar:  {calendar-backend}

What to do next:
  /para              — see your dashboard
  /para:capture      — capture your first idea
  /para:project new  — create your first project
  /para:review       — run a weekly review anytime
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
