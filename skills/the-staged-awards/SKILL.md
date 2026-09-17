---
name: the-staged-awards
description: Generate a playful, affectionate short-form awards ceremony for a software repository using size-aware analysis of its complete file inventory, available Git history, tests, docs, naming patterns, and development quirks.
---

# The Staged Awards

Generate a playful, affectionate short-form awards ceremony for the current software repository, or for a repository path named by the user. The ceremony should feel like a warm developer awards night, not a roast.

## Workflow

1. Read the support files before generating:
   - `templates/awards_template.md` is the required default output structure.
   - `templates/linkedin_awards_template.txt` is the required structure when the user asks for LinkedIn, plain text, or an emoji-led version.
   - `references/ceremony-patterns.md` provides award ideas, useful repo signals, and tone calibration.
2. Resolve this skill's directory, then run `python3 scripts/repository_profile.py <repository-path>`. Use its measurements to classify the repository and populate the ceremony summary. The script measures every Git-tracked path, counts eligible text files and lines, and examines commits reachable from `HEAD` and all locally available refs.
3. Inspect the complete tracked-file inventory, then apply the matching depth:
   - **Small:** at most 100 eligible text files and 20,000 eligible lines. Read every eligible text file.
   - **Medium:** at most 500 eligible text files and 100,000 eligible lines. Map every directory; read repository-level docs, tests, scripts, helpers, configuration, and workflows; inspect representative files from every primary component; and deepen coverage around high-churn and recently changed files.
   - **Large:** anything above either medium threshold. Map every primary package and component; read repository-level docs, configuration, and workflows; sample representative source and tests from every primary component; and prioritize the highest-churn files, important stable files, and changes distributed across the history span.

   Eligible text excludes common dependency, vendor, build, coverage, generated, lock, minified, source-map, binary, symlink, unreadable, and secret-like credential files. Exclude all `.env` files case-insensitively, including concrete files and example, sample, or template variants. Do not expose credentials or sensitive configuration values; inspect other safe configuration key names and purposes only. Do not silently ignore an entire primary component. Record a concise `inspection_coverage` value that states whether all eligible files were read or describes the structured sampling used.
4. Analyze history across the repository's available time span:
   - Review commit subjects distributed from the earliest available commit through the latest, not only the most recent cluster.
   - Use name and churn history across all locally available refs to find repeated changes, quiet stable files, ambitious refactors, recurring fixes, documentation growth, and workflow support.
   - Treat `commit_count`, `first_commit_date`, and `latest_commit_date` as totals for locally available history. If `shallow_repository=yes`, explicitly label the history as incomplete. Local analysis cannot count unfetched or unavailable remote commits.
   - For a repository with no commits, use `0` and `N/A` for both dates, then base awards on the visible file structure.
5. Generate fresh opening and closing remarks for this run:
   - Ground both sections in the repository's actual character, themes, history, or award choices rather than reusing stock ceremony prose.
   - Keep them warm, concise, and distinct from each other. The opening should welcome the repository to the ceremony; the closing should reflect on what the awards recognized and give it a fitting send-off.
   - Use time-neutral language. Do not say "tonight," "this morning," "today," or otherwise assume when the skill is being run unless the user explicitly asks for time-specific wording.
6. Generate 4-6 awards using the selected template. For LinkedIn mode, prefer 4 concise awards so the ceremony remains easy to post and read.
7. Keep raw inspection notes out of the ceremony unless the user asks for them, but always include the completed ceremony summary.
8. Do a tone pass and soften any line that could read as contempt, scolding, mockery, or a personal jab.

## Award Format

Each award should include:

- Award title
- Winner, such as a file, directory, commit message, script, test, docs page, config file, or recurring pattern
- Brief explanation grounded in the repository
- One brief presenter-style sentence as normal prose, without a label such as `Presenter commentary:`

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

- Default to valid Markdown using `templates/awards_template.md`.
- For LinkedIn, plain-text, or emoji-led output, use `templates/linkedin_awards_template.txt` and:
  - Use emoji and blank lines for structure instead of Markdown headings, emphasis, inline code, links, rules, or list markers.
  - Keep repository paths and commit messages as ordinary unwrapped text.
  - Write the footer URL in full so LinkedIn can recognize it as a link.
  - Aim to keep the complete post at or below 2,500 characters. Tighten the explanations before removing required sections.
- Do not output JSON.
- Do not wrap the ceremony in a code fence.
- Do not include implementation commentary.
- Prefer specific observations over generic software jokes.
- In the ceremony summary, always report repository size, tracked and eligible file totals, eligible line total, inspection coverage, total available commits, and the first and latest available commit dates.
- Replace every template placeholder, including `{{opening_remarks}}` and `{{closing_remarks}}`; do not copy remarks from a previous ceremony.
