# Repository Instructions

## Purpose

This repository is used to create Sunday school teaching material as Markdown
slide decks. The AI must be able to research, draft, revise, and review a
complete `.md` file for a Sunday school lesson.

## Project environment

### Virtual environment

On Windows, always activate the virtual environment before running Python
scripts:

```powershell
powershell -Command "& 'C:\Users\User\projects\envs\.extraction_env\Scripts\Activate.ps1'; [your_command_here]"
```

Instructions for macOS and Linux have not yet been added.

### Dependencies

- Pillow, for image processing.
- markdown2, for Markdown conversion.

### Scripts

- `markdown_to_html_converter.py` converts Markdown to HTML and detects image
  aspect ratios.

## Mandatory subagent

For every task that creates, revises, expands, translates, or reviews Sunday
school material, invoke a subagent with the task name
`sunday_school_writer` at the start of the task. This is required even when the
requested change is small.

Before invoking it, read `agents/sunday_school_writer.md` completely and use
that file as the subagent's instructions. Give the subagent the lesson topic,
intended audience, language, Scripture passage, desired length, destination
file, and any constraints supplied by the user. If any detail is missing,
infer it from the request and reference files when safe.

The primary agent remains responsible for integrating the subagent's work,
checking the final file, and reporting the result. If subagents are unavailable
in the current environment, follow `agents/sunday_school_writer.md` directly
and tell the user that delegation was unavailable.

## Reference material

Before drafting or revising a lesson, inspect relevant Markdown files in
`out/`. Treat them as the repository's house-style examples.

- Use `out/slide_template.md` as the basic syntax reference.
- Prefer recent, topic-adjacent files in `out/` for structure, tone, language,
  theological depth, Scripture-citation style, and expected slide density.
- Reuse the style and conventions, but do not copy substantial passages unless
  the user explicitly asks for reuse.
- Prioritize writing Sunday school material in Chinese. Use another language
  only when the user explicitly requests it.

## Markdown lesson format

- Save the deliverable as a `.md` file, normally under `out/`, unless the user
  specifies another path.
- Begin with one `#` heading for the lesson title.
- Use each `##` heading as a new slide.
- Use `###` headings only for a subtitle or a clear subdivision within a slide.
- Keep slide text concise and presentation-ready. Prefer short bullet points
  over long paragraphs.
- Add image references on their own line using the existing convention:
  `` `assets/example.jpg` ``. Do not invent an asset filename and imply that it
  exists; mark a proposed asset clearly when no matching file is available.
- Every `##` slide must contain exactly one relevant image reference unless the
  user explicitly requests a different layout.
- First inspect `out/assets/` for suitable existing images. If there are not
  enough relevant images, use image generation or search online for appropriate
  images, save the final files under `out/assets/`, and reference those local
  files from the Markdown.
- When sourcing images online, prefer public-domain or clearly reusable images
  and record the creator, source page, and license when available on the final
  `## References` slide. Record AI-generated images as generated assets in the
  references.
- Do not use remote image URLs directly in lesson slides. Every image reference
  must resolve to an existing local file under `out/assets/`.
- Use tables, numbered lists, bold terms, review slides, applications, and
  discussion questions when they improve teaching.
- Cite Scripture close to the claim it supports and keep book/chapter/verse
  notation consistent within the deck.

## Content quality

- Build a coherent teaching flow: title or hook, biblical context, main
  teaching, explanation, application, review, and discussion or reflection.
- Keep the content age-appropriate, pastorally responsible, and usable by a
  Sunday school teacher.
- Distinguish the biblical text from interpretation, historical background,
  denominational teaching, and application.
- Verify quotations, names, dates, catechism references, and Scripture
  references when reliable sources or repository material are available.
- Do not fabricate quotations, citations, sources, or image availability.
- Follow the theological viewpoint and terminology established by the
  topic-adjacent files in `out/` unless the user asks for a different approach.

## Final checks

Before finishing:

1. Compare the draft with at least two relevant Markdown references in `out/`,
   including `out/slide_template.md`.
2. Check heading hierarchy, slide length, asset references, Scripture
   references, language consistency, and Markdown validity.
3. Count the `##` slides and image-bearing slides. Confirm that every `##`
   slide contains one relevant image and that every referenced image exists
   under `out/assets/`.
4. Confirm the requested `.md` file exists at the intended path and contains a
   complete, teachable lesson rather than an outline fragment.
