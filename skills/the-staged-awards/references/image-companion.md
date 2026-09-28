# Image Companion

Create one celebratory image for every awards ceremony unless the user explicitly opts out. The image should feel like a portrait of the repository, not a generic programming thumbnail.

## Select a Style

Run `python3 scripts/select_image_style.py` once per ceremony, without `--seed`. Use the returned style for that run. Do not choose a preferred style manually or rerun merely to obtain a different result.

The selector chooses uniformly from:

- Theatrical paper-cut diorama
- Retro pixel-art ceremony
- Isometric 3D miniature
- Vintage screen-print poster
- Technical blueprint or cyanotype

Record the returned `style_name` in the image handoff.

## Derive Repository Motifs

Choose two to four visual motifs supported by the repository inspection. Prefer its real product domain, primary components, tests, documentation, release machinery, or award winners. Make the combination specific enough that someone familiar with the project can recognise it.

Do not expose source code, credentials, personal data, private URLs, or secret-like configuration. Do not invent a logo, interface, feature, architecture, or production claim. Use an existing tracked logo only when it is safe to inspect and can be supplied to the image tool as an explicit reference.

## Generate the Artwork

Use the built-in `image_gen` tool in its default generation mode. Create a 4:3 landscape composition and ask for:

```text
Use case: stylized-concept
Asset type: 4:3 landscape companion artwork for a software-repository awards ceremony
Primary request: Celebrate the inspected repository through a warm developer awards-night scene.
Scene/backdrop: A stage, trophy, spotlight, or curtain-call moment integrated with the verified repository motifs.
Subject: The repository motifs selected from inspection.
Style/medium: <style_prompt from select_image_style.py>
Composition/framing: 4:3 landscape; strong central silhouette; keep the lower third calm and uncluttered for a title overlay; preserve important content within the central 85 percent.
Lighting/mood: Warm, celebratory, affectionate, playful rather than corporate.
Text: No text in the generated artwork; typography is added deterministically afterward.
Constraints: Use only repository-supported motifs; original imagery; suitable at LinkedIn feed size.
Avoid: logos that were not supplied as references, readable code, UI screenshots, watermarks, harsh roast imagery, generic walls of code, and extra text.
```

If the built-in image tool is unavailable or fails, do not silently omit the image and do not switch to an API or CLI that requires credentials. Return the completed ceremony, explain the image blocker briefly, and offer the credential-requiring fallback only if the applicable image-generation guidance permits it.

## Finish and Save

Copy the selected generated artwork from its generated-images location into a temporary or workspace path, then run:

```text
python3 scripts/compose_awards_image.py <generated-artwork> <target-png> --repository-name <exact-repository-name>
```

The composer crops without distortion to exactly 1200 x 900, adds the exact repository name and `THE STAGED AWARDS`, and refuses to overwrite an existing file. It requires `ffmpeg`. If the intended filename exists, use `-v2`, `-v3`, and so on. If `ffmpeg` is unavailable, preserve the generated artwork, report that exact-size finishing is blocked, and do not claim it is 1200 x 900 or has a verified title overlay.

Save the finished project asset under `awards/images/<repository-slug>-staged-awards-<YYYY-MM-DD>.png` in the target repository. Inspect the finished PNG with the available image-viewing tool. Verify the exact repository name, readable contrast, relevant motifs, no stray generated text, and a natural crop. Iterate once with a focused correction if needed.

## Write Alt Text

Write concise alt text from the inspected final image, not just from the prompt. Mention:

- the selected visual style;
- the repository name shown in the title;
- the principal repository-specific motifs;
- the celebratory stage, trophy, spotlight, or curtain-call element.

Do not begin with “Image of” and do not include details that are not visibly present.

## Deliver by Format

For Markdown, replace the image placeholders in `templates/awards_template.md`. Use a path relative to the generated Markdown file when the ceremony is saved, otherwise use the project-relative asset path.

For LinkedIn, keep the post itself clean and copy-pasteable using `templates/linkedin_awards_template.txt`. Present the image file path, selected style, and alt text as a clearly separate handoff after the post; they do not count toward the post's 2,500-character target. Also render the generated image inline when the interface supports it.

For both formats, report the final saved path and selected style. Never claim the image is ready when only an uncomposed background exists.
