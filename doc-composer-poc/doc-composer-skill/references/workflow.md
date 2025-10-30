# Document Composition Workflow Reference

## Advanced Workflows

### Conditional Document Inclusion

For dynamic document composition based on conditions:

```python
def conditional_compose(manifest_path, conditions):
    """Include documents based on conditions."""
    base_docs = parse_manifest(manifest_path)
    final_docs = []
    
    for doc in base_docs:
        # Check conditions
        if doc.startswith("financial-") and not conditions.get("include_financials"):
            continue
        if doc.startswith("risk-") and not conditions.get("include_risks"):
            continue
        final_docs.append(doc)
    
    return final_docs
```

### Multi-Library Support

To pull documents from multiple libraries:

```python
def multi_library_locate(doc_name, libraries):
    """Search multiple libraries for a document."""
    for library in libraries:
        doc_path = Path(library) / f"{doc_name}.docx"
        if doc_path.exists():
            return doc_path
    return None
```

### Template Variables

For documents with placeholder variables:

```python
def replace_variables(doc_path, variables):
    """Replace {{variable}} placeholders in document."""
    doc = Document(doc_path)
    
    for paragraph in doc.paragraphs:
        for key, value in variables.items():
            if f"{{{{{key}}}}}" in paragraph.text:
                paragraph.text = paragraph.text.replace(
                    f"{{{{{key}}}}}",
                    str(value)
                )
    
    return doc
```

## Format Preservation Strategies

### Preserving Section-Specific Headers

When documents need different headers/footers:

```python
# Add section break to maintain separate headers
def add_with_section_break(master, source_doc):
    # Add section break
    section = master.add_section(WD_SECTION.NEW_PAGE)
    
    # Copy header from source
    for paragraph in source_doc.sections[0].header.paragraphs:
        new_para = section.header.add_paragraph(paragraph.text)
        # Copy formatting...
```

### Maintaining Styles Hierarchy

```python
def sync_styles(master, source):
    """Ensure source styles exist in master."""
    for style in source.styles:
        if style.name not in [s.name for s in master.styles]:
            # Create matching style in master
            try:
                new_style = master.styles.add_style(
                    style.name,
                    style.type
                )
                # Copy style properties...
            except:
                pass  # Style might already exist
```

### Complex Table Formatting

```python
def copy_table_advanced(source_table, master_doc):
    """Copy table with full formatting preservation."""
    new_table = master_doc.add_table(
        rows=0,  # Start empty
        cols=len(source_table.columns)
    )
    
    # Copy column widths
    for idx, column in enumerate(source_table.columns):
        new_table.columns[idx].width = column.width
    
    # Copy rows with formatting
    for source_row in source_table.rows:
        new_row = new_table.add_row()
        new_row.height = source_row.height
        
        for idx, cell in enumerate(source_row.cells):
            new_cell = new_row.cells[idx]
            # Copy cell properties
            new_cell.width = cell.width
            # Copy content with formatting...
```

## Error Recovery

### Rollback on Failure

```python
import shutil

def safe_compose(master, docs, output):
    """Compose with rollback on failure."""
    # Create backup
    backup = f"{master}.backup"
    shutil.copy2(master, backup)
    
    try:
        # Attempt composition
        compose_document(master, docs, output)
    except Exception as e:
        # Restore from backup
        shutil.copy2(backup, master)
        raise e
    finally:
        # Clean up backup
        if Path(backup).exists():
            Path(backup).unlink()
```

### Partial Composition

When some documents fail:

```python
def resilient_compose(doc_list, library):
    """Continue composition even if some docs fail."""
    successful = []
    failed = []
    
    for doc in doc_list:
        try:
            validate_document(doc, library)
            successful.append(doc)
        except Exception as e:
            failed.append((doc, str(e)))
            print(f"Warning: Skipping {doc}: {e}")
    
    if failed:
        print(f"\nFailed documents: {len(failed)}")
        for doc, error in failed:
            print(f"  - {doc}: {error}")
    
    return successful
```

## Performance Optimization

### Batch Processing

```python
def batch_compose(manifests, library, master, output_dir):
    """Process multiple manifests efficiently."""
    from concurrent.futures import ProcessPoolExecutor
    
    def compose_one(manifest):
        output = Path(output_dir) / f"{manifest.stem}-output.docx"
        return compose_document(manifest, library, master, output)
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(compose_one, manifests)
    
    return list(results)
```

### Caching Parsed Documents

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def load_cached_document(path):
    """Cache loaded documents to avoid re-parsing."""
    return Document(path)
```

## Integration Points

### Claude Code Usage

When called from Claude Code:
```python
# Claude Code can call with specific parameters
result = compose_document(
    manifest="reports/q4-2024.md",
    library="/shared/templates/",
    master="masters/corporate.docx",
    output="output/Q4-Report-2024.docx"
)

# Then provide the result to user
print(f"Report generated: {result}")
```

### Manifest Generation

Claude can generate manifests programmatically:
```python
def generate_manifest(sections, output_path):
    """Generate manifest from section list."""
    with open(output_path, 'w') as f:
        f.write(f"# Generated Report Manifest\n\n")
        f.write("## Sections\n")
        for section in sections:
            f.write(f"- {section}\n")
```

### Validation Checks

```python
def validate_composition(output_path):
    """Validate the composed document."""
    doc = Document(output_path)
    
    checks = {
        "has_content": len(doc.paragraphs) > 0,
        "has_multiple_pages": len(doc.sections) > 1,
        "file_size_reasonable": Path(output_path).stat().st_size > 10000,
        "can_be_opened": True  # If we got here, it opened
    }
    
    return all(checks.values()), checks
```
