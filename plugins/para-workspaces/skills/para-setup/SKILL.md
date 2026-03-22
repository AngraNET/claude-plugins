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
- Create: `{para-dir}/4-archives/Archive-{YYYY-MM-DD}/`
- Ask: "Move all files from {path} into this archive? This is reversible — nothing gets deleted. (y/n)"
- If confirmed, run:
  ```bash
  cp -r "{source-path}/." "{para-dir}/4-archives/Archive-{YYYY-MM-DD}/"
  ```
- Confirm: "Your existing files are archived. You're starting fresh."

---

## Step 3: Scaffold Directory Structure

Create:
```
{para-dir}/
├── 0-inbox/
│   └── someday-maybe/
├── 1-projects/
├── 2-areas/
├── 3-resources/
├── 4-archives/
└── reviews/
```

Also create `{para-dir}/reviews/life-goals.md`:

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

And `{para-dir}/reviews/personal-vision.md`:

```markdown
---
type: personal-vision
last-updated: {today}
---

# Personal Narrative Vision

*Describe your ideal typical day one year from now. Cover your main life areas, what you've achieved, how you spend your time. This is reviewed monthly and rewritten annually.*

```

---

## Step 4: Task Backend

Ask: "Which task backend do you want to use?"
- [1] Google Tasks (shared OAuth with Calendar/Gmail)
- [2] Todoist (separate API token)
- [3] None for now

---

## Step 5: Integration Credentials

For Google (Calendar + Gmail + Tasks):
- Explain: "You need a Google OAuth refresh token. Set up a Google Cloud project, enable Calendar/Gmail/Tasks APIs, create OAuth2 credentials (Desktop app), and complete the OAuth flow."
- Ask for: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`
- Suggest adding to `~/.bashrc` or `~/.zshrc`

For Todoist:
- Ask for: `TODOIST_API_TOKEN` (from todoist.com/app/settings/integrations/developer)

For Notion (optional):
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
task-backend: {google-tasks|todoist|none}
show-dashboard-on-start: {true|false}
inbox-reminder: true
log-sessions: false
review-day: sunday
notion-enabled: {true|false}
---

# PARA Workspaces Configuration
```

---

## Step 8: Confirm

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARA Workspaces ready!

Vault:    {para-dir}
Tasks:    {backend}
Calendar: {enabled|not configured}
Email:    {enabled|not configured}

What to do next:
  /para              — see your dashboard
  /para:capture      — capture your first idea
  /para:project new  — create your first project
  /para:review       — run a weekly review anytime
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
