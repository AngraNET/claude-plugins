---
name: para:review
description: Run a structured PARA review — weekly (tactical, ~30 min), monthly (strategic), or annual (life alignment). Based on Tiago Forte's official review processes from Building a Second Brain.
argument-hint: [weekly | monthly | annual]
allowed-tools: [Read, Write, Glob, Bash]
---

# PARA Review

Run a structured review of your Second Brain system.

| Type | Frequency | Purpose | Time |
|---|---|---|---|
| Weekly | Weekly | Tactical clarity, situational awareness | ~30 min |
| Monthly | Monthly | Strategic course correction | ~60–90 min |
| Annual | Yearly | Life alignment, vision reset | ~2–3 hours |

## Arguments: $ARGUMENTS

Determine review type from argument (`weekly`, `monthly`, or `annual`).
Default: `weekly`

## Instructions

Read settings to get `para-dir`, then launch the appropriate agent:

- **weekly** → launch `para-weekly-reviewer` agent
- **monthly** → launch `para-monthly-reviewer` agent
- **annual** → launch `para-annual-reviewer` agent

Pass the agent:
- Today's date
- The PARA directory path
- Paths to `reviews/life-goals.md` and `reviews/personal-vision.md`

After the agent completes, confirm:
"Review complete. Log saved to `{para-dir}/reviews/{date}-{type}-review.md`"

---

## The Review Philosophy

From Tiago Forte:

> "What allows the Weekly Review to be mostly tactical is that the Monthly Review is mostly strategic; what allows the Weekly Review to be fast and responsive is that the Monthly Review is slower and more time-consuming."

These three reviews form a nested system:
- **Weekly** keeps you grounded in what's happening now
- **Monthly** course-corrects your direction
- **Annual** questions the destination itself
