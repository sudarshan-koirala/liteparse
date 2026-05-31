# Claude Code Setup for LiteParse

This project uses [LiteParse](https://www.npmjs.com/package/@llamaindex/liteparse) — a lightweight document parser for PDFs, images, Office documents, and more.

## Installation

### Install LiteParse Globally

```bash
npm i -g @llamaindex/liteparse
```

Verify installation:
```bash
lit --version
```

### System Dependencies

#### macOS
```bash
brew install imagemagick          # For image processing
brew install --cask libreoffice   # For Office documents (DOCX, PPTX, XLSX)
```

#### Ubuntu/Debian
```bash
apt-get install imagemagick libreoffice
```

---

## Quick Start

### Parse a PDF to Text
```bash
lit parse data/attention-is-all-you-need.pdf
```

### Parse to JSON (structured output)
```bash
lit parse data/attention-is-all-you-need.pdf --format json -o output.json
```

### Parse with OCR (for scanned PDFs/images)
```bash
lit parse data/handwritten.jpg --ocr-language eng
```

### Save to markdown
```bash
lit parse data/attention-is-all-you-need.pdf -o output_parsed/parsed-output.md
```

---

## Common Commands

| Command | Description |
|---------|-------------|
| `lit parse <file>` | Extract text from document |
| `lit parse <file> --format json` | Output as structured JSON |
| `lit parse <file> --no-ocr` | Parse without OCR (faster for text PDFs) |
| `lit parse <file> --target-pages "1-5"` | Parse specific page range |
| `lit batch-parse ./input ./output` | Batch process a directory |
| `lit screenshot <file> -o ./screenshots` | Generate page screenshots |

---

## Using in Python/Node.js

### Python (with LiteParse from PyPI)
```python
from liteparse import LiteParse

parser = LiteParse()
result = parser.parse("data/attention-is-all-you-need.pdf")
print(result.text)  # Full document text
print(result[0])    # First page
```

### Node.js (with @llamaindex/liteparse)
```javascript
import { LiteParse } from "@llamaindex/liteparse";

const parser = new LiteParse();
const result = await parser.parse("data/attention-is-all-you-need.pdf");
console.log(result.text);
```

---

## Supported Formats

| Category | Formats |
|----------|---------|
| **PDF** | `.pdf` |
| **Word** | `.doc`, `.docx`, `.docm`, `.odt`, `.rtf` |
| **PowerPoint** | `.ppt`, `.pptx`, `.pptm`, `.odp` |
| **Spreadsheets** | `.xls`, `.xlsx`, `.xlsm`, `.ods`, `.csv`, `.tsv` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg` |

---

## Claude Code Integration

When using Claude Code with this project:

1. **File parsing**: Ask Claude Code to parse documents using the `lit` CLI
2. **Batch processing**: Use `lit batch-parse` for multiple files
3. **Screenshots**: Generate visual previews with `lit screenshot`
4. **Programmatic**: Use the Python `liteparse` library or Node.js SDK

### Example: Ask Claude Code

> "Parse the PDF at data/attention-is-all-you-need.pdf and save the output to output_parsed/result.md"

Claude Code will:
1. Run: `lit parse data/attention-is-all-you-need.pdf -o output_parsed/result.md`
2. Verify the output file was created
3. Show you the parsed content

---

## Advanced: LiteParse Configuration

Create `liteparse.config.json` for repeated use:

```json
{
  "ocrLanguage": "en",
  "ocrEnabled": true,
  "dpi": 150,
  "outputFormat": "json",
  "preciseBoundingBox": true
}
```

Use it:
```bash
lit parse document.pdf --config liteparse.config.json
```

---

## Troubleshooting

### `lit` command not found
```bash
npm i -g @llamaindex/liteparse
npm list -g @llamaindex/liteparse  # Verify installation
```

### LibreOffice needed for Office documents
```bash
# macOS
brew install --cask libreoffice

# Ubuntu/Debian
apt-get install libreoffice
```

### OCR not working
- Ensure ImageMagick is installed
- Try disabling OCR: `lit parse file.pdf --no-ocr`
- Check OCR language: `lit parse file.pdf --ocr-language fra` (for French, etc.)

---

## Project Structure

```
liteparse/
├── data/                                    # Sample documents
│   ├── attention-is-all-you-need.pdf       # Original PDF
│   ├── attention-is-all-you-need.json      # Metadata JSON
│   ├── attention-is-all-you-need-liteparse.json  # Full parsed output
│   ├── handwritten.jpg                     # Sample image for OCR
│   └── handwritten_clean.png               # Processed image
├── output_parsed/                           # Example parsed output
│   └── attention-is-all-you-need.md        # Parsed markdown
├── screenshots/                             # Page screenshots
├── liteparse-yt.ipynb                      # Demo notebook
├── pyproject.toml                          # Python project config
├── CLAUDE.md                               # This file
└── README.md                               # Project documentation
```

---

## Next Steps

1. ✅ Install: `npm i -g @llamaindex/liteparse`
2. ✅ Verify: `lit --version`
3. ✅ Test: `lit parse data/attention-is-all-you-need.pdf`
4. Ask Claude Code to parse documents as needed!
