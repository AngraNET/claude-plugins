---
name: para:capture
description: Quickly capture an idea, note, article, highlight, or anything that resonates into the PARA inbox for later processing. This is the CAPTURE step of the CODE framework (Capture → Organize → Distill → Express). Use when the user wants to get something out of their head quickly without categorizing it yet.
argument-hint: <text to capture, or leave empty for interactive>
allowed-tools: [Write, Bash]
---

# PARA Quick Capture — The "C" in CODE

Capture is the first step of the Second Brain methodology. Your job is to make this **as fast and frictionless as possible.**

> "Your brain is for having ideas, not storing them." — Tiago Forte

## The Resonance Principle

Don't ask the user to justify what they're capturing. The guiding principle is: **save anything that resonates on an intuitive or emotional level.** This is not an analytical decision — it's a signal. Trust it.

What's worth capturing:
- Ideas that spark something
- Highlights from articles, books, podcasts
- Decisions made in meetings
- Things you want to remember or look up later
- Anything that feels surprising, useful, or personally meaningful

## User input: $ARGUMENTS

## Instructions

1. Read `para-dir` from `~/.claude/para-workspaces.local.md` (default: `~/para`)

2. If `$ARGUMENTS` is provided, use it directly.
   If empty, ask simply: "What do you want to capture?"
   Do not ask for a category or bucket — that's what `/para:inbox` is for.

3. Optionally ask: "Any source? (article URL, book title, meeting name — skip if none)"

4. Generate a filename: `{YYYY-MM-DD}-{HHmmss}-{slug}.md`
   where slug = first 4–5 meaningful words, hyphenated, lowercase

5. Write the file to `{para-dir}/0-inbox/`:

```markdown
---
type: inbox
captured-at: {ISO 8601 timestamp}
source: {cli | url | book | meeting | other}
source-ref: {URL, book title, or meeting name if provided}
tags: []
---

{capture text}
```

6. Confirm briefly: "Captured. ✓"
   If inbox now has >5 items: add "({N} items in inbox — run `/para:inbox` to process)"

## What to tell the user about routing

If the user asks where it went or how it gets organized: explain that this goes to the inbox first. The inbox is processed separately with `/para:inbox`, which applies the PARA routing decision tree:
> Project → Area → Resource → (don't save)

The intentional delay between capture and organization is by design — it keeps capture fast and organization thoughtful.
