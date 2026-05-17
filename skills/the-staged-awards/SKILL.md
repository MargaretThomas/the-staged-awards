---
name: the-staged-awards
description: Generate a playful, affectionate mini awards ceremony for a software repository by analyzing git history, commit messages, file structure, tests, docs, naming patterns, and development quirks.
---

# The Staged Awards

Generate a playful, affectionate mini awards ceremony for the current software repository, or for a repository path named by the user. The ceremony should feel like a warm developer awards night, not a roast.

## Workflow

1. Read the support files before generating:
   - `templates/awards_template.md` is the required output structure unless the user asks for a shorter format.
   - `references/ceremony-patterns.md` provides award ideas, useful repo signals, and tone calibration.
2. Inspect the repository context:
   - Identify the repository name and current branch.
   - Review recent git history and commit messages.
   - Review tracked files, top-level directories, docs, tests, scripts, helpers, and config files.
   - Look for repeated changes, high-churn areas, quiet stable files, unusually named helpers, careful tests, ambitious refactors, recurring fix patterns, documentation growth, and workflow support.
3. Prefer lightweight shell inspection commands such as:
   - `git rev-parse --show-toplevel`
   - `git branch --show-current`
   - `git log --oneline --decorate -30`
   - `git log --name-only --pretty=format: -- .`
   - `git ls-files`
   - `git status --short`
4. Generate 4-6 awards in Markdown using the template fields and sections.
5. Keep raw inspection notes out of the ceremony unless the user asks for them.
6. Do a tone pass and soften any line that could read as contempt, scolding, mockery, or a personal jab.

## Award Format

Each award should include:

- Award title
- Winner, such as a file, directory, commit message, script, test, docs page, config file, or recurring pattern
- Short explanation grounded in the repository
- Brief presenter-style commentary

## Tone Rules

- Warm first, funny second.
- Specific before clever.
- Celebrate effort, taste, care, resilience, and usefulness.
- Tease situations and code archaeology lightly; do not tease competence.
- Avoid shaming contributors, hostile sarcasm, elitist humor, and harsh criticism.
- Avoid framing code as incompetent, chaotic, suspicious, over-engineered, guilty, obsessive, or being interrogated.
- Avoid jokes built around side-eyes, judgment, cross-examination, magnifying glasses, grudging acceptance, or "how does this even work?" unless the user explicitly asks for a sharper roast tone.
- Avoid jokes that imply the repo, tests, docs, workflows, or algorithms are annoying, excessive, fussy, or barely held together.
- Do not name individual contributors unless the user explicitly asks.
- Do not ridicule security, accessibility, incident, or production-risk work.
- If the repo has limited history, say so briefly and base awards on visible file structure and docs instead.

## Humor Calibration

Use these transformations when a joke starts to sound like a roast:

- "too many constants" -> "a supporting cast of constants keeping choices explicit"
- "cross-examined" -> "carefully considered"
- "stare at it hard enough" -> "look closely enough to understand its shape"
“barely holding together” → “holding together more than it lets on”
“suspicious utility” → “unexpectedly useful in a lot of situations”
- "side-eyes from the toolchain" -> "help from the toolchain"
- "how is this still working?" -> "steady under more responsibility than expected"

Good jokes should leave the maintainer feeling seen, not called out.

## Self-Check Before Output

Before returning the ceremony, silently check:

- Would this feel kind if read by the person who wrote the code?
- Does each award praise a concrete contribution, not just point at a quirk?
- Are the punchlines aimed at the drama of software work rather than at the author's judgment?
- Did at least half the awards recognize care, clarity, reliability, documentation, testing, or release work?
- Are any metaphors too harsh for fragile work such as bugs, fixes, tests, releases, accessibility, security, or production support?

## Output Rules

- Output valid Markdown only.
- Do not output JSON.
- Do not wrap the ceremony in a code fence.
- Do not include implementation commentary.
- Prefer specific observations over generic software jokes.
