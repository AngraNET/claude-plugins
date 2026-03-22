# Claude Plugins — Personal Marketplace

Personal Claude Code plugin marketplace for AngraNET.

## Structure

- **`/plugins`** — Personal plugins
- **`/external_plugins`** — Third-party plugins (reserved)

## Installation

Once registered as a marketplace, install plugins via:

```
/plugin install {plugin-name}@angra-plugins
```

## Plugins

| Plugin | Description |
|---|---|
| [para-workspaces](plugins/para-workspaces) | PARA methodology / Second Brain (Tiago Forte) |

## Plugin Structure

Each plugin follows the Claude Code plugin standard:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json            (optional)
├── skills/              (optional)
├── agents/              (optional)
├── hooks/               (optional)
└── README.md
```
