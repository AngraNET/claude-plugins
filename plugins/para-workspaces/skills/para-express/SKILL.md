---
name: para:express
description: Create tangible output from your Second Brain — the EXPRESS step of CODE. Helps assemble Intermediate Packets, find relevant notes for a deliverable, or turn captured knowledge into a real work product. Use when the user wants to create something using their PARA notes.
argument-hint: <project-name or deliverable description>
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

# PARA Express — The "E" in CODE

Expression is the whole point of your Second Brain. All the capturing, organizing, and distilling exists to create real output.

> "Information only becomes knowledge — something personal, embodied, grounded — when we put it to use." — Tiago Forte

## The Intermediate Packets Strategy

Don't try to complete an entire project at once. Break it into **Intermediate Packets** — discrete, reusable units of work.

Types of Intermediate Packets:
- Meeting notes with decisions captured
- Research findings summarized
- Brainstorm outputs
- Slide decks or outlines
- Action item lists
- Drafted sections of a document

> "Instead of rolling a giant boulder uphill all at once, complete just one Intermediate Packet per work session." — Tiago Forte

Benefits:
- Work in any available time window (15 min or 3 hours)
- Gather continuous feedback
- Maintain motivation through frequent wins
- Packets are reusable across future projects

## Arguments: $ARGUMENTS

(project name, or description of what you want to create)

## Instructions

### Mode 1: Find relevant notes for a deliverable

If user wants to create something (article, presentation, proposal, report):

1. Ask: "What are you trying to create? Describe the deliverable."
2. Ask: "Which project is this for?" (or "standalone")
3. Search across PARA for relevant notes:
   - Grep `{para-dir}` for key terms from the deliverable description
   - Check the project's `_index.md` notes section
   - Check related resource topics
4. Present the most relevant notes/excerpts:

```
Found {N} relevant notes for: "{deliverable}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
From Project "Website Redesign":
  • Capture 2026-03-10: "homepage hero copy ideas"
  • Capture 2026-03-15: "competitor analysis notes"

From Resource "Copywriting":
  • Layer 4 summary: "Headlines should focus on benefit, not feature..."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

5. Ask: "Should I assemble these into a starting draft?"
6. If yes: create a new file in the project directory as an Intermediate Packet:
   `{para-dir}/01-projects/{project}/packets/{YYYY-MM-DD}-{slug}.md`

### Mode 2: Track Intermediate Packets for a project

If user wants to see or manage their work packets for a project:

1. List all files in `{para-dir}/01-projects/{project}/packets/`
2. Show creation date, title, and a one-line summary of each
3. Ask: "Create a new packet, or open an existing one?"

### Mode 3: Version-forward publishing

Remind the user of the "version-forward" principle:
> "There is no such thing as a finished product. Everything carries implicit version 1.0 status. Share and perfect iteratively."

If user seems to be waiting until something is "done" before sharing, ask: "What's the smallest version of this you could share or act on today?"

## Packet template

```markdown
---
type: intermediate-packet
project: "{project}"
created: {today}
status: draft
deliverable: "{what this contributes to}"
---

# {Packet Title}

## Source Notes Used
{list of notes/captures this draws from}

## Content

{the actual work product}
```
