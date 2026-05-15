# The Staged Awards

Tiny awards ceremonies for software repositories.
Part morale boost, part code archaeology, part developer theatre.

The Staged Awards analyzes a repository’s structure, commit history, naming patterns, documentation, and development quirks to generate a playful mini awards ceremony in Markdown.

Because every repo deserves at least one dramatic standing ovation.

---

## Codex Plugin Structure

This repository is packaged as a Codex plugin with one bundled skill:

```text
.codex-plugin/plugin.json
skills/the-staged-awards/SKILL.md
skills/the-staged-awards/references/ceremony-patterns.md
skills/the-staged-awards/templates/awards_template.md
```

The plugin manifest points Codex at `./skills/`, and the skill can be run against any repository Codex can inspect.

---

## What It Does

The Staged Awards can generate things like:

* 🏆 Most Chaotic Commit Message
* 🏆 Quiet MVP File
* 🏆 Main Character Directory
* 🏆 “How Is This Still Working?” Award
* 🏆 Best Supporting Script
* 🏆 Biggest Glow-Up
* 🏆 The Courage Under Production Pressure Award

The goal is to celebrate the strange humanity inside software projects.

---

## Example Output

```md
# The Staged Awards

## 🏆 Quiet MVP Award
`src/utils/dateHelpers.ts`

Never complained.
Never asked for attention.
Still carrying half the application on its back.

---

## 🏆 Most Chaotic Commit Message
"final final actual fix 2"

A timeless classic.
```

---

## Why This Exists

Most tooling focuses on performance, quality, correctness, or delivery speed.

The Staged Awards focuses on:

* developer culture
* team morale
* storytelling
* humour
* reflection
* tiny moments of recognition

Sometimes the repo deserves applause too.

---

## Philosophy

The Staged Awards should feel:

* playful, not cruel
* observant, not invasive
* developer-aware, not corporate
* lightweight, not enterprise-heavy

Good software has fingerprints.
This project celebrates them.

---

## License

MIT

---

## Closing Remarks

Every repository contains:

* decisions
* experiments
* panic
* craftsmanship
* shortcuts
* care
* survival

The Staged Awards simply brings the curtain up for a few minutes.
