# liteparse

A Python project demonstrating [LiteParse](https://pypi.org/project/liteparse/) — a lightweight library for parsing PDFs and images into structured text, with optional OCR support via Tesseract.

## Features

- Parse PDFs into plain text or markdown, preserving page structure
- OCR support for scanned documents and handwritten images
- Multi-language OCR via Tesseract
- CLI tool (`lit`) for quick parsing from the terminal
- Save parsed output to `.txt` or `.md` files

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) (package manager)
- [liteparse](https://pypi.org/project/liteparse/) >= 2.0.4
- [Tesseract](https://github.com/tesseract-ocr/tesseract) *(optional, for OCR)*
- [ImageMagick](https://imagemagick.org/) *(optional, for screenshot/image conversion)*

## Quick Start

Clone and set up the project:

```bash
git clone https://github.com/sudarshan-koirala/liteparse.git
cd liteparse
uv sync  # Install project and all dependencies
```

That's it! `uv sync` reads `pyproject.toml` and `uv.lock` and sets everything up.

---

## Installation

### For this project (clone + setup)

```bash
git clone https://github.com/sudarshan-koirala/liteparse.git
cd liteparse
uv sync
```

### To add liteparse to another project

With uv:
```bash
uv add liteparse
```

With pip:
```bash
pip install liteparse
```

### Tesseract (for OCR support)

```bash
brew install tesseract
brew install tesseract-lang   # adds all extra languages
```

Set the tessdata path for the current session:

```bash
export TESSDATA_PREFIX="/opt/homebrew/share/tessdata"
```

To make it permanent:

```bash
echo 'export TESSDATA_PREFIX="/opt/homebrew/share/tessdata"' >> ~/.zshrc
source ~/.zshrc
```

### ImageMagick (for image/screenshot processing)

```bash
brew install imagemagick
```

---

## Usage

### Basic PDF parsing

```python
from liteparse import LiteParse

parser = LiteParse()
result = parser.parse("data/attention-is-all-you-need.pdf")

print(result.text)
```

### With OCR enabled

Useful for scanned PDFs or handwritten images:

```python
from liteparse import LiteParse

parser = LiteParse(
    ocr_enabled=True,
    tessdata_path="/opt/homebrew/share/tessdata",
    # ocr_language="eng",  # defaults to English
)

result = parser.parse("data/handwritten.jpg")
print(result[0])
```

### Save parsed output to a file

```python
import os
from liteparse import LiteParse

pdf_path = "data/attention-is-all-you-need.pdf"

parser = LiteParse()
result = parser.parse(pdf_path)

output_dir = os.path.join(os.getcwd(), "output_parsed")
os.makedirs(output_dir, exist_ok=True)

output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".md"
output_path = os.path.join(output_dir, output_filename)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(result.text)

print(f"Saved to {output_path}")
```

---

## Claude Code Integration

The liteparse skill can be added to Claude Code for seamless integration with various AI agents. To add the liteparse skill to Claude Code, use:

```bash
npx skills add run-llama/llamaparse-agent-skills --skill liteparse -a claude-code
```

This enables Claude Code to leverage liteparse capabilities for parsing documents within your AI workflows.

---

## CLI Usage

LiteParse ships with a `lit` CLI. Use `uv run lit` to invoke it without activating the virtual environment.

### Parse a local file

```bash
uv run lit parse data/attention-is-all-you-need.pdf
```

### Parse and save to a file

```bash
uv run lit parse data/attention-is-all-you-need.pdf -o output_parsed/attention.md
```

### Download and parse a PDF in one step

```bash
curl -sL -o attention.pdf https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf \
  && uv run lit parse attention.pdf -o attalluneed.txt
```

> **Note:** Piping directly from `curl` into `lit parse -` is not currently supported and will produce an unsupported file format error.

---

## Project Structure

```
liteparse/
├── data/
│   ├── attention-is-all-you-need.pdf   # sample PDF
│   └── handwritten.jpg                 # sample image for OCR
├── output_parsed/
│   └── attention-is-all-you-need.md    # example parsed output
├── screenshots/
│   ├── page_001.png
│   └── page_002.png
├── liteparse-yt.ipynb                  # demo notebook
├── hello.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Notes

- `result.text` returns the full document as a single string.
- `result[n]` accesses the parsed content of page `n` (0-indexed).
- When running in a Jupyter notebook, use `os.getcwd()` instead of `__file__` to get the working directory — `__file__` is not defined in notebook environments.
