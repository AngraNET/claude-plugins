# PARA Workspaces

A Claude Code plugin implementing Tiago Forte's [PARA methodology](https://fortelabs.com/blog/para/) — a universal system for organizing your life into **Projects**, **Areas**, **Resources**, and **Archives**.

## Features

- Full PARA vault management (projects, areas, resources, archives, inbox)
- Quick capture to inbox
- Structured weekly and monthly reviews
- Google Calendar integration — view events in project context
- Gmail integration — read and compose emails tied to projects
- Task management — Google Tasks or Todoist, linked to PARA projects
- Cross-source search across everything
- Health checker for overdue deadlines and stale projects
- Session start dashboard showing your current priorities

## Installation

```bash
/plugin install para-workspaces
```

Or install from a local path:

```bash
/plugin install /path/to/para-workspaces
```

## Quick Start

1. **Initialize**: `/para:setup` — walks you through configuration
2. **Dashboard**: `/para` — see your current status
3. **Capture**: `/para:capture <idea>` — get it out of your head
4. **New project**: `/para:project new <name>`

## Skills (Slash Commands)

| Command | Description |
|---|---|
| `/para` | Dashboard overview |
| `/para:setup` | First-time setup and configuration |
| `/para:capture <text>` | Quick capture to inbox |
| `/para:project <subcommand>` | Manage projects |
| `/para:area <subcommand>` | Manage areas of responsibility |
| `/para:resource <subcommand>` | Manage reference resources |
| `/para:archive <type> <name>` | Archive a PARA item |
| `/para:inbox` | Process inbox captures |
| `/para:review weekly\|monthly` | Structured review |
| `/para:tasks <subcommand>` | Task management |
| `/para:calendar <subcommand>` | Calendar integration |
| `/para:email <subcommand>` | Email integration |
| `/para:search <query>` | Search everything |

## Integrations

### Google Calendar / Gmail / Google Tasks

Requires a Google OAuth2 refresh token. Set these environment variables:

```bash
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REFRESH_TOKEN="your-refresh-token"
```

To get a refresh token:
1. Create a project at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable the Calendar, Gmail, and Tasks APIs
3. Create OAuth2 credentials (Desktop app)
4. Complete the OAuth flow to get a refresh token

### Todoist (alternative to Google Tasks)

```bash
export TODOIST_API_TOKEN="your-api-token"
```

Get your token at: todoist.com/app/settings/integrations/developer

### Notion (optional)

```bash
export NOTION_API_TOKEN="your-integration-token"
```

## PARA Directory Structure

```
~/para/              (configurable)
├── 0-inbox/         Raw captures awaiting processing
├── 1-projects/      Active projects with specific outcomes
├── 2-areas/         Ongoing responsibilities
├── 3-resources/     Reference material by topic
├── 4-archives/      Completed/inactive items
└── reviews/         Weekly and monthly review logs
```

## Data Model

All PARA data is stored as human-readable Markdown with YAML frontmatter. Files are portable, git-friendly, and work with any Markdown editor (Obsidian, Logseq, Typora, VS Code).

## License

MIT
