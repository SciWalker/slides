# Markdown Slide Authoring Guidelines

Use this guide when writing new Markdown slide decks under `out/`. For conversion details, always refer to `docs/markdown_to_html_slide_workflow.md` as the source of truth for how `markdown_to_html_converter.py` parses the file.

## Goal

Write Markdown that is easy to teach from, easy to convert, and unlikely to break the current custom converter.

The best existing decks use this rhythm:

1. Main title
2. Opening or review slide
3. Topic definition or background
4. Several focused teaching-point slides
5. Scripture, catechism, or source support
6. Application or conclusion
7. Discussion questions
8. References, when needed

## File Naming

Use lowercase, underscore-separated filenames when possible:

```text
out/07062026_christ_light.md
out/10112024_church_disciplines.md
out/06042025_second_coming.md
```

Avoid spaces in new filenames. Existing files such as `career talk.md` work as Markdown files, but they make command-line conversion and same-name HTML output less predictable.

Use the same basename for conversion:

```bash
MD_NAME="07062026_christ_light" python3 markdown_to_html_converter.py
```

## Recommended Deck Skeleton

Start future decks from this shape:

```markdown
# Main deck title

## Opening title or review
`assets/image-name.jpg`
- One sentence that frames the lesson
- One sentence that connects to the previous lesson

## Main scripture or key question
- Scripture reference or central question
- Main idea of the lesson

## Definition or background
- Define the main term
- Give the historical or biblical setting
- State why the topic matters

## Teaching point 1
- First claim
- Supporting scripture or reason
- Short explanation

## Teaching point 2
- First claim
- Supporting scripture or reason
- Short explanation

## Application
- What the hearer should believe
- What the hearer should repent of
- What the hearer should practice

## Discussion questions
1. First question
2. Second question
3. Third question

## References
1. Source title or URL
```

## Slide Length

Keep each slide short enough to fit on screen:

- Aim for 3 to 5 bullets per slide.
- Keep each bullet to one main idea.
- Split dense material into multiple `##` slides.
- Long catechism answers and long scripture quotes can work, but they should usually be their own slide.
- Tables should be used only for comparison material, not for ordinary bullet lists.

The generated slides are scrollable, but scrolling during teaching is harder than moving to the next slide.

## Headings

Use exactly one top-level `#` heading at the beginning:

```markdown
# 教会纪律
```

Use `##` for every slide title:

```markdown
## 教会纪律的范围
```

Avoid using `#` inside the body. The converter treats a section starting with `# ` as a deck title and skips it.

Use `###` sparingly inside slide content. The converter turns it into a bold list item, not a real subheading:

```markdown
## 蒙恩之道
### 1. 圣言
- 做成信心
- 坚固信心
```

## Images

Put images under `out/assets/` or a subfolder of it, then reference them without `out/`:

```markdown
## 耶稣再来的简介
`assets/second_coming_christ.jpg`
- 圣经明确预言耶稣要第二次以肉身降临世界
- 与第一次来相比，第二次再来是带着荣耀和审判
```

Guidelines:

- Use one image per slide with the current converter.
- Put the image line immediately after the `##` slide title.
- Keep image filenames stable after generating HTML.
- Prefer descriptive filenames such as `jesus_second_coming.jpg`.
- If using subfolders, keep paths simple, such as `assets/dec/image-name.jpg`.

The current converter tries to detect image orientation:

- Horizontal images appear above the text.
- Vertical images appear on the left, with text on the right.

## Bullet Lists

Use simple dash bullets:

```markdown
## 教会的标记
- 使徒行传 2:42
- 圣道宣讲
- 施行圣礼
- 执行教会纪律
```

Avoid nested bullets for new decks. The converter does not preserve true nested list structure.

If a non-bulleted line appears inside a slide, the converter still turns it into a list fragment. This can be useful for short quotes, but avoid mixing too many paragraph styles in the same slide.

## Numbered Lists

Use numbered lists for sequence, steps, arguments, or discussion questions:

```markdown
## 教会纪律惩戒三步骤
1. 私下里当面跟对方说
2. 带着两个见证人一起再去跟他说
3. 如果对方还是不听，就告诉教会的议会
```

Use numbered lists only when the order matters. For unordered teaching points, use dash bullets.

## Bold Emphasis

Use bold to identify the key term at the front of a bullet:

```markdown
- **第一次来**: 耶稣道成肉身，为了拯救世人
- **第二次来**: 基督在荣耀中来，审判世界
```

This pattern appears often in the existing decks and converts cleanly to HTML.

## Tables

Use tables for direct comparisons:

```markdown
## 耶稣再来的兆头
| 兆头 | 示例经文 |
|---|---|
| 福音传遍天下 | 马太福音 24:14 |
| 假基督出现 | 马太福音 24:4-5 |
```

Guidelines:

- Keep columns short.
- Avoid large paragraphs inside table cells.
- Do not put an image line before a table slide; table conversion is intended for text-only slides.

## Scripture and Catechism Slides

For scripture-heavy or catechism-heavy slides:

- Put the reference in the slide title when it is the main subject.
- Use bullets for the core phrases you want to explain.
- If quoting a long passage, consider breaking it into several slides.
- Follow long doctrinal text with a short explanation or application slide.

Example:

```markdown
## 海德堡要理第83问：「掌管天国钥匙的权柄」是什么意思？
答：掌管天国钥匙的权柄，就是借着「宣讲福音」与「教会惩戒」领人悔改。
```

## Discussion and Application

Most teaching decks should end with practical reflection:

```markdown
## 应用
- 检视自己的信仰动机
- 在学校、职场中活出信仰见证
- 持守真理并信靠基督

## 讨论问题
1. 这段经文如何改变你对这个主题的理解？
2. 哪一个应用最挑战你？
3. 你可以在本周怎样实践？
```

Keep discussion questions concrete and answerable. Three questions is usually enough.

## References

Use a final `## References` slide when the deck relies on outside sources:

```markdown
## References
1. https://example.com/source
2. Book title, chapter number
```

Avoid hiding important teaching content only in references. The deck should stand on its own.

## Quality Checklist Before Converting

Before running the converter:

- The file starts with one `# Main Title`.
- Every slide starts with `##`.
- Slides are separated by one blank line.
- Image paths use `assets/...`, not `out/assets/...`.
- Image files exist under `out/assets/`.
- New filenames do not contain spaces.
- There are no accidental body `#` headings.
- Dense slides have been split.
- Tables are text-only slides.
- Discussion and references slides are included when useful.

Run conversion:

```bash
MD_NAME="deck_name" python3 markdown_to_html_converter.py
```

Then open or serve the generated `out/deck_name.html` and inspect the result visually.
