---
name: para:distill
description: Apply Progressive Summarization to a note or resource — the DISTILL step of CODE. Highlights key passages, adds a summary, and makes the note useful for your future self. Use when the user wants to distill a note, article highlight, or resource into something quickly scannable.
argument-hint: <file-path or resource-name>
allowed-tools: [Read, Write, Glob, Grep]
---

# PARA Distill — The "D" in CODE

Distillation transforms raw captured notes into knowledge your future self can use instantly.

> "Design notes for your future self — you're sending packets of knowledge through time." — Tiago Forte

## The Progressive Summarization Technique

Distillation happens in layers, like a map you can zoom to any detail level:

| Layer | What you do |
|---|---|
| **Layer 1** | Save only the best excerpts from the source (already done at capture) |
| **Layer 2** | Bold the most important phrases within those excerpts |
| **Layer 3** | Highlight the most essential bolded phrases |
| **Layer 4** | Write an executive summary at the top |
| **Layer 5** | (Rarely needed) — Remix into your own words entirely |

**Key rule:** Don't try to distill everything at once. "Add value to a note every time you touch it." A note you return to frequently will naturally move through the layers over time.

## Arguments: $ARGUMENTS

(file path, resource name, or project name)

## Instructions

1. Find the target file:
   - If a path is given, read it directly
   - If a resource/project name, find its `CLAUDE.md`
   - If no argument, list recent inbox items and let user pick

2. Read the file content

3. Ask: "What layer would you like to apply?"
   - **[2] Bold key phrases** — mark the most important passages
   - **[3] Highlight essentials** — pick the best of the bolded phrases
   - **[4] Add executive summary** — write a 2–3 sentence summary at the top
   - **[Auto] Assess and apply** — look at the current state and apply the next logical layer

4. Apply the chosen layer:

   **Layer 2 — Bold key phrases:**
   Read the content. Identify the 20–30% of passages that are most insightful, surprising, or actionable. Wrap them in `**bold**`. Present the bolded version and ask: "Does this look right? Anything to add or remove?"

   **Layer 3 — Highlight essentials:**
   From the bolded passages, identify the 10–15% that are the absolute core. Wrap those in `==highlighted==` (Obsidian/Markdown highlight syntax). These are what you'd read if you had 30 seconds.

   **Layer 4 — Executive summary:**
   Write a 2–3 sentence summary at the very top of the file, under a `## Summary` heading. It should answer: "What is this note about and why does it matter to me?"

5. Update `last-accessed` in the frontmatter to today

6. Confirm: "Distillation applied. Note is now at Layer {N}."

## Tips to share with the user

- "You don't need to distill everything — only notes you return to multiple times will naturally reach Layer 3 or 4."
- "The goal isn't perfect notes. It's notes useful enough to act on when you need them."
- "If a note feels hard to distill, it might not be worth keeping — consider deleting it."
