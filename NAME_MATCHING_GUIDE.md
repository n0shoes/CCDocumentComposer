# Document Name Matching Guide

## Current Implementation (Basic)
The current `compose_document.py` requires **exact name matching** between manifest entries and library files.

### Example:
```markdown
# Manifest entry
- Missing-Security-Header

# Must match exactly:
library/Missing-Security-Header.docx ✓
library/missing-security-header.docx ✗ (case mismatch)
library/Missing_Security_Header.docx ✗ (underscore vs hyphen)
```

## Enhanced Version (With Fuzzy Matching)
The enhanced `compose_document_enhanced.py` provides flexible matching:

### Normalization Rules:
1. **Case insensitive**: `Missing-Security-Header` = `missing-security-header`
2. **Flexible separators**: Spaces, hyphens, underscores are interchangeable
3. **Leading dashes ignored**: `- missing security` = `missing security`
4. **Special characters removed**: `risk-assessment!` = `risk-assessment`

### Examples That Would Match:

| Manifest Entry | Library File | Match? |
|---|---|---|
| `- missing security headers` | `Missing-Security-Header.docx` | ✅ Yes |
| `executive summary` | `Executive-Summary.docx` | ✅ Yes |
| `risk_assessment` | `Risk-Assessment.docx` | ✅ Yes |
| `financial overview` | `Financial_Overview.docx` | ✅ Yes |
| `Q1 Report` | `q1-report.docx` | ✅ Yes |

### Fuzzy Matching (60% Similarity)
If no exact match (after normalization), tries fuzzy matching:

```
Manifest: "secuirty headers"  (typo)
Library:  "Security-Headers.docx"
Result:   ≈ Fuzzy match found (85% confidence)
```

## How Claude Would Handle This

When using the skill, Claude would:

1. **Try exact matching first** (current implementation)
2. **If no matches found**, Claude could:
   - Suggest similar files from the library
   - Offer to correct the manifest
   - Use the enhanced script for fuzzy matching

### Example Claude Interaction:

```
User: "Generate report using this manifest:
- executive summary
- missing security headers
- financial data"

Claude: I notice your manifest uses casual names. Let me check your library...

Found in library:
✓ Executive-Summary.docx → matches "executive summary"
≈ Missing-Security-Header.docx → likely matches "missing security headers"
✗ No match for "financial data"

Available similar files:
- Financial-Overview.docx
- Financial-Report-Q1.docx

Would you like me to:
1. Use fuzzy matching to proceed
2. Update your manifest with exact names
3. Show you all available library documents
```

## Best Practices

### For Exact Matching (Current):
```markdown
# Use exact filenames without .docx
- Executive-Summary
- Missing-Security-Header
- Financial-Overview
```

### For Flexible Matching (Enhanced):
```markdown
# More natural, readable format
- Executive Summary
- Missing Security Headers
- Financial Overview
```

### For Claude Code Usage:
Claude can intelligently handle both by:
1. Detecting which version of the script is available
2. Suggesting corrections when matches aren't found
3. Showing available options from the library
4. Using fuzzy matching when appropriate

## Switching to Enhanced Version

To use the enhanced matching in your skill:

```bash
# Replace the original script
cp compose_document_enhanced.py doc-composer-skill/scripts/compose_document.py

# Or keep both and let Claude choose
cp compose_document_enhanced.py doc-composer-skill/scripts/compose_document_fuzzy.py
```

Then Claude can:
- Use strict matching for production documents
- Use fuzzy matching for draft/development work
- Let users choose their preference

## Configuration Options

The enhanced version supports:
- `--no-interactive`: Auto-accept fuzzy matches (for automation)
- Confidence threshold: Currently 60%, can be adjusted
- Match reporting: Shows confidence scores for transparency