---
name: para:archive
description: Archive a completed or inactive PARA item (project, area, or resource). Moves it to the archives while preserving all content.
argument-hint: <project|area|resource> <name>
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Archive

Archive a completed or inactive item from the PARA system. The item is moved to `04-archives/` with a timestamp and reason, preserving all content for future reference.

## Arguments

$ARGUMENTS — format: `<type> <name>`

Examples:
- `project website-redesign`
- `area old-responsibility`
- `resource outdated-topic`

## Instructions

1. Parse the type (project/area/resource) and name from `$ARGUMENTS`

2. Locate the item:
   - `project` → `{para-dir}/01-projects/{name}/`
   - `area` → `{para-dir}/02-areas/{name}/`
   - `resource` → `{para-dir}/03-resources/{name}/`
   - Use fuzzy matching if exact name not found

3. Read the existing `CLAUDE.md`

4. Ask the user:
   - "Reason for archiving?" (completed / inactive / cancelled / replaced)
   - If project: "What was the final outcome?" (optional)

5. Update `CLAUDE.md` frontmatter with:
   ```yaml
   archived-at: {today}
   archived-reason: "{reason}"
   original-path: "{original relative path}"
   ```
   Also set `status: archived` for projects.

6. Create archive destination: `{para-dir}/04-archives/{YYYY-MM}/{item-name}/`

7. Move all files from the source directory to the archive destination using Bash:
   ```bash
   mv "{source-dir}" "{archive-dir}"
   ```

8. Confirm: "Archived '{name}' to 04-archives/{YYYY-MM}/{name}/"

9. If archiving a project: check if any tasks in the task backend still reference this project and notify the user.
