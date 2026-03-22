---
name: para:resource
description: Create, view, list, or add notes to PARA Resources — reference material organized by topic. Resources are things you might want to reference later but that have no active outcome attached.
argument-hint: [new <topic> | view <topic> | list | add-note <topic> <text>]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Resource Management

Manage reference resources in the PARA system. Resources are organized by topic and contain notes, links, and reference material you want to keep but don't need to act on now.

## Arguments

$ARGUMENTS

## Subcommands

### `new <topic>`

1. Ask:
   - **Description**: What is this resource about?
   - **Tags**: Any relevant tags?
   - **Source URL**: Is there a primary source or reference URL? (optional)

2. Create directory: `{para-dir}/3-resources/{slugified-topic}/`

3. Write `_index.md`:

```markdown
---
type: resource
title: "{topic}"
description: "{description}"
created: {today}
last-accessed: {today}
source-url: "{url}"
tags: []
---

# {topic}

## Overview

{Description of this resource topic}

## Notes

## Links & References

## Key Takeaways

```

---

### `view <topic>`

1. Find and read the resource `_index.md` (fuzzy match on topic name)
2. Update `last-accessed` to today
3. Display full content

---

### `add-note <topic> <text>`

1. Find the resource directory for `<topic>`
2. Append a dated note entry to the `## Notes` section:

```markdown
### {date}

{text}

```

3. Update `last-accessed`
4. Confirm: "Note added to {topic}"

---

### `list`

1. Read all resources from `3-resources/`
2. Display organized by tags if available:

```
Topic                    Tags                    Last Accessed
───────────────────────────────────────────────────────────────
CSS Grid Reference       frontend, css           2026-03-10
GTD Methodology          productivity, systems   2026-02-28
Sourdough Recipes        cooking, food           2026-01-15
```
