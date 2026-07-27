# Markdown to HTML Slide Workflow

This repository stores Reveal.js slide source files as Markdown under `out/` and converts one Markdown deck at a time into an HTML presentation with `markdown_to_html_converter.py`.

## Current Repository Shape

- `out/*.md` contains the slide source decks. At the time of inspection there are 59 Markdown files.
- `out/*.html` contains generated or hand-created Reveal.js presentations. 52 Markdown files currently have a same-basename `.html` output.
- `out/template.html` is the Reveal.js wrapper used by the converter. It loads Reveal.js from `../node_modules/reveal.js`, so the generated HTML is intended to be opened from inside `out/`.
- `out/assets/` contains images referenced by the Markdown decks.
- `.env` selects the deck to convert with `MD_NAME`, for example `MD_NAME="07062026_christ_light"`.

Markdown files without a same-basename HTML output at inspection time:

- `08092024_earnest_prayer.md` has `earnest_prayer.html` instead.
- `18042026_the_kingdom_of_heaven.md` has no generated HTML yet.
- `3003025_intermediate_state.md` has no generated HTML yet.
- `career talk.md` has `career_talk.html` instead.
- `christ_work_disciples_faith.md` has no generated HTML yet.
- `perseverance_implications.md` has `perserverance_implications.html` instead.
- `slide_template.md` is an authoring template, not a finished deck.

## Main Conversion Script

Use `markdown_to_html_converter.py` for the normal workflow.

What it does:

1. Loads `MD_NAME` from the shell environment or `.env`.
2. Reads `out/{MD_NAME}.md`.
3. Splits the Markdown into sections separated by blank lines.
4. Converts each section into a Reveal.js `<section>`.
5. Inserts the generated sections into `out/template.html` inside `<div class="slides">`.
6. Writes `out/{MD_NAME}.html`.
7. Inserts the deck title into the HTML `<title>` tag.

Required local dependencies:

- Python 3
- `python-dotenv`
- `Pillow`
- `markdown2`, although it is imported but not currently used
- Node dependency `reveal.js`, installed from `package.json`

Install dependencies when needed:

```bash
pip install python-dotenv Pillow markdown2
npm install
```

Convert the deck named in `.env`:

```bash
python3 markdown_to_html_converter.py
```

Convert a specific deck without editing `.env`:

```bash
MD_NAME="07062026_christ_light" python3 markdown_to_html_converter.py
```

The value of `MD_NAME` is the basename only. Do not include `out/` or `.md`.

## Markdown Format Expected by the Converter

The converter uses a small custom Markdown dialect. It does not implement all Markdown behavior.

### Deck Title

Use a single top-level `#` heading as the deck title:

```markdown
# 约翰福音与使徒行传：耶稣基督是世界的光
```

The script uses this text for the HTML `<title>` and does not create a slide for it. Avoid additional `#` headings inside the body, because any section starting with `# ` is treated as a title section and skipped.

### Text-Only Slide

Use `##` for each slide title, followed by bullet or numbered content:

```markdown
## 结论
- First point
- Second point
- **Key term:** explanation
```

The output uses the text-only slide template with background `assets/nov/100114.jpg`.

### Image Slide

Put an image path in backticks as the first line after a `##` heading:

```markdown
## 引入
`assets/jesus-light-of-world.png`
- First point
- Second point
```

The output uses an image slide template with background `assets/scroll.jpg`.

Image path behavior:

- Paths are written relative to the generated HTML file in `out/`, so `assets/example.jpg` means `out/assets/example.jpg`.
- The script checks image dimensions with Pillow. Horizontal images render above the text; vertical images render on the left with text on the right.
- If the image file cannot be found, the script assumes a horizontal layout and still writes the path into the HTML.

### Numbered Lists

Use normal numbered Markdown:

```markdown
1. First point
2. Second point
```

The converter detects numbered items and emits an ordered list with custom CSS numbering.

### Bold Text

Use `**bold**` for emphasis:

```markdown
- **核心信息：** explanation
```

The converter changes this to `<strong>...</strong>`.

### Tables

Markdown tables are supported only in text-only sections:

```markdown
## Comparison
| Header 1 | Header 2 |
|---|---|
| Cell 1 | Cell 2 |
```

The converter detects a pipe table and creates `<table class="reveal-table">`.

### Subheadings Inside Slides

Lines starting with `###` inside slide content are converted into bold list items, not actual nested Reveal.js slides.

```markdown
## Slide title
### Important subheading
- Detail
```

### Unsupported or Fragile Patterns

- Nested bullet indentation is not preserved as a nested list.
- Multiple images on one line are intended by `slide_template.md`, but the current parser removes backticks before splitting the image list. In practice, use one image per slide unless the parser is fixed.
- A section must be separated from the next section by a blank line, because the parser uses double newlines to split sections.
- Raw Markdown paragraphs become list fragments. This works for short teaching points but is not full paragraph rendering.
- `#` body headings are skipped, so use `##` for slide titles.

## Producing a New HTML Slide Deck

1. Create or edit `out/{deck_name}.md`.
2. Put all images under `out/assets/` or a subfolder of `out/assets/`.
3. Reference images from Markdown as `assets/image-name.jpg`.
4. Make sure the first line is a single `# Deck Title`.
5. Use `##` for all slides.
6. Set `MD_NAME`:

```bash
MD_NAME="{deck_name}" python3 markdown_to_html_converter.py
```

7. Open `out/{deck_name}.html` in a browser.

If the browser blocks some local JavaScript fetches, serve the folder with a local HTTP server:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/out/{deck_name}.html
```

## Auxiliary Scripts

### `main.py`

`main.py` is an experimental LLM-based generator. It uses LangGraph and a local Ollama model to generate a complete single-file Reveal.js presentation from a hard-coded Markdown sample, evaluates it, optionally improves it, and writes `presentation_ollama.html`.

It is not part of the current `out/*.md` to `out/*.html` workflow.

Use it only when experimenting with LLM-generated standalone HTML. It requires Ollama running locally and the configured model to be available.

### `extract.py`

`extract.py` extracts image-search keywords and image-generation prompts from a JSON project structure. It reads project settings from `src/params.yaml` and API keys from `config.yml`, then writes enriched JSON to a `data/youtube_projects/.../processed/output.json` path.

It is not part of the current slide conversion workflow. It may help earlier in content preparation when looking for image prompts, but it does not read `out/*.md` and does not generate slide HTML.

## Current Asset Notes

The inspected Markdown files contain 154 backtick image/path references. Most resolve under `out/assets/`. Missing references found during inspection:

- `18042026_the_kingdom_of_heaven.md`: `assets/jesus-kingdom.png`, `assets/ot-expectation.jpg`, `assets/jesus-background.jpg`, `assets/kingdom-vision.jpg`
- `18052025_intro_greatest_stories.md`: `assets/cross and bible.jpg`
- `3003025_intermediate_state.md`: ten `assets/dec/...` image references for the intermediate-state deck
- `slide_template.md`: placeholder image paths

Before converting those decks, add the missing assets or update the image paths.
