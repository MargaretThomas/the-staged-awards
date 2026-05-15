---
name: the-staged-awards
description: Generate a playful, affectionate mini awards ceremony for a software repository by analyzing git history, commit messages, file structure, tests, docs, naming patterns, and development quirks.
---

# The Staged Awards

Generate a playful but respectful mini awards ceremony for the current software repository, or for a repository path named by the user.

## Workflow

1. Inspect the repository context before writing the ceremony:
   - Identify the repository name and current branch.
   - Review recent git history and commit messages.
   - Review tracked files, top-level directories, docs, tests, scripts, helpers, and config files.
   - Look for repeated changes, high-churn areas, quiet stable files, unusually named helpers, lonely tests, ambitious refactors, and recurring fix patterns.
2. Prefer lightweight shell inspection commands such as:
   - `git rev-parse --show-toplevel`
   - `git branch --show-current`
   - `git log --oneline --decorate -30`
   - `git log --name-only --pretty=format: -- .`
   - `git ls-files`
   - `git status --short`
3. Do not expose raw analysis notes unless the user asks. Use the inspection only to make the awards specific and grounded.
4. Generate 5-10 awards in Markdown.
5. Keep the tone affectionate, witty, developer-aware, lightly theatrical, and emotionally intelligent.

## Award Format

Each award should include:

- Award title
- Winner, such as a file, directory, commit message, script, test, docs page, config file, or recurring pattern
- Short explanation grounded in the repository
- Brief presenter-style commentary

Use the bundled template at `templates/awards_template.md` when a fuller ceremony structure would help. Read `references/ceremony-patterns.md` for extra award ideas and tone constraints when needed.

## Tone Rules

- Celebrate the repository as a human-made artifact.
- Make the humor playful, not cruel.
- Avoid shaming contributors, hostile sarcasm, elitist humor, and harsh criticism.
- Do not name individual contributors unless the user explicitly asks.
- Do not ridicule security, accessibility, incident, or production-risk work.
- If the repo has limited history, say so briefly and base awards on visible file structure and docs instead.

## Output Rules

- Output valid Markdown only.
- Do not output JSON.
- Do not wrap the ceremony in a code fence.
- Do not include implementation commentary.
- Prefer specific observations over generic software jokes.
