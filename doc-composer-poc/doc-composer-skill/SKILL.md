---
name: doc-composer
description: Composes Word documents from a library of single-page documents using a manifest file. Merges documents while preserving all formatting, styles, headers, and footers from both the master template and individual documents.
---

# Document Composer

## Overview
Composes professional Word documents by merging single-page document templates from a library according to a manifest file, while preserving all formatting. Features intelligent fuzzy matching for flexible document name resolution.

## Key Features
- **Fuzzy Name Matching**: Intelligently matches manifest entries to library files
- **Case Insensitive**: `Executive Summary` matches `executive-summary.docx`
- **Flexible Separators**: Spaces, hyphens, underscores are interchangeable
- **Typo Tolerance**: Finds closest matches with 60%+ similarity
- **Format Preservation**: Maintains all styles, headers, footers from source documents

## Workflow

### 1. Parse Manifest
Read the markdown manifest file to get the list of documents to include:
```python
import re

def parse_manifest(manifest_path):
    """Extract document list from markdown manifest."""
    with open(manifest_path, 'r') as f:
        content = f.read()
    
    # Extract items from bullet points
    pattern = r'^\s*[-*]\s+(.+)$'
    documents = re.findall(pattern, content, re.MULTILINE)
    return [doc.strip() for doc in documents]
```

### 2. Locate Library Documents (With Fuzzy Matching)
Find each document in the library using intelligent matching:

**Matching Process:**
1. **Normalize names**: Convert to lowercase, standardize separators
2. **Exact match first**: Check for exact match after normalization
3. **Fuzzy match fallback**: Find closest match if no exact match exists

**Examples that match:**
- `"executive summary"` → `Executive-Summary.docx`
- `"missing security headers"` → `Missing-Security-Header.docx`
- `"risk_assessment"` → `Risk-Assessment.docx`
- `"Q1 report"` → `q1-report.docx`

```python
def locate_documents(doc_names, library_path='./library'):
    """Find documents using fuzzy matching."""
    # The enhanced compose_document.py handles:
    # - Case insensitive matching
    # - Space/hyphen/underscore normalization
    # - Fuzzy matching with confidence scores
    # - User confirmation for fuzzy matches
```

### 3. Merge Documents
Use the merge script to combine documents:
```bash
python scripts/merge_docx.py \
    --master master-template/corporate-template.docx \
    --documents cover-page.docx executive-summary.docx \
    --output output/final-report.docx
```

### 4. Key Considerations

#### Format Preservation
- Headers/footers from master template apply to all pages
- Section-specific headers can be preserved using section breaks
- Styles from master template cascade to all content
- Page numbering continues throughout document

#### Error Handling
- Validate manifest before processing
- Check all documents exist before merging
- Provide clear error messages for missing documents
- Create backup of master template before modification

## Scripts

### compose_document.py
Main orchestration script that:
1. Parses manifest
2. Validates document availability
3. Calls merge process
4. Reports success/failure

### merge_docx.py
Document merging script that:
1. Opens master template
2. Appends each document maintaining formatting
3. Handles section breaks appropriately
4. Saves final composed document

## Example Usage

```bash
# Simple composition
python scripts/compose_document.py \
    --manifest manifests/quarterly-report.md \
    --library library/ \
    --master master-template/corporate-template.docx \
    --output output/Q4-2024-report.docx

# With custom library path
python scripts/compose_document.py \
    --manifest manifests/board-presentation.md \
    --library /shared/templates/board/ \
    --master master-template/board-template.docx \
    --output output/board-deck.docx
```

## Manifest Format

Manifests are simple markdown files listing documents. The enhanced composer supports flexible naming:

### Natural Language Format (Recommended)
```markdown
# Report Title

## Sections to Include
- Executive Summary
- Financial Overview  
- missing security headers
- Risk Assessment
- Strategic Initiatives

## Notes
Names are matched intelligently - case/separators don't matter!
```

### Exact Match Format (Legacy)
```markdown
# Report Title

## Sections to Include
- Executive-Summary
- Financial-Overview
- Missing-Security-Header
- Risk-Assessment
- Strategic-Initiatives
```

**Matching Features:**
- **Case insensitive**: `executive summary` = `Executive-Summary`
- **Separator flexible**: Spaces, hyphens, underscores work
- **Typo tolerant**: 60%+ similarity threshold
- **User confirmation**: Asks before using fuzzy matches

Only bullet points (- or *) are parsed for document names.
