---
name: para:search
description: Search across all PARA items, and optionally calendar events, emails, and tasks for a query. Use when the user is looking for something and doesn't know exactly where it is.
argument-hint: <query> [--source all|local|calendar|email|tasks]
allowed-tools: [Glob, Grep, Bash]
---

# PARA Search

Search across the entire PARA system for a query.

## Arguments

$ARGUMENTS — format: `<query> [--source <source>]`

Default source: `all`

## Instructions

1. Parse query and source flag from `$ARGUMENTS`
2. Read `para-dir` from settings (default: `~/para`)

3. **Local search** (always run unless `--source` excludes it):

   a. Search frontmatter fields (title, goal, tags, area):
   ```bash
   grep -r -l --include="*.md" -i "{query}" "{para-dir}"
   ```

   b. Search body content:
   ```bash
   grep -r -n --include="*.md" -i "{query}" "{para-dir}"
   ```

   c. Categorize results by bucket (projects / areas / resources / archives / inbox)

4. **Calendar search** (if `--source all` or `--source calendar` and MCP available):
   - Search calendar events with query in title or description

5. **Email search** (if `--source all` or `--source email` and MCP available):
   - Search Gmail for the query

6. **Tasks search** (if `--source all` or `--source tasks` and MCP available):
   - Search task lists for the query

7. **Present results** ranked by relevance:

```
Search results for: "{query}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 PROJECTS (N matches)
  1. Website Redesign — title match
     ~/para/01-projects/website-redesign/CLAUDE.md

  2. SEO Improvement — body match (line 42)
     ~/para/01-projects/seo-improvement/CLAUDE.md
     → "...{query} should be addressed in the meta tags..."

📚 RESOURCES (N matches)
  3. CSS Grid Reference — tag match
     ~/para/03-resources/css-grid-reference/CLAUDE.md

📅 CALENDAR (N matches)
  4. "{query} Review Meeting" — 2026-03-25 10:00

✉ EMAIL (N matches)
  5. Thread: "Re: {query} proposal" — 3 days ago

✅ TASKS (N matches)
  6. "Research {query} options" — Website Redesign project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: N results across all sources
```

If no results found, say so clearly and suggest broader search terms.
