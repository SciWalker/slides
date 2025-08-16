# Project Environment Setup

## Virtual Environment

### Windows
Always activate the virtual environment before running Python scripts:

```bash
powershell -Command "& 'C:\Users\User\projects\envs\.extraction_env\Scripts\Activate.ps1'; [your_command_here]"
```

### macOS/Linux
(To be added later)

## Dependencies
- Pillow (for image processing)
- markdown2 (for markdown conversion)

## Scripts
- `markdown_to_html_converter.py` - Converts markdown to HTML with image aspect ratio detection