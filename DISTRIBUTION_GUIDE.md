# Document Composer Skill - Distribution Guide

## For Skill Distributors (You)

### Method 1: Package as a .skill file (Recommended)
```bash
cd doc-composer-poc
python scripts/package_skill.py doc-composer-skill/

# This creates: doc-composer-skill.skill
```

Share the `.skill` file with other users. It's a self-contained package with everything needed.

### Method 2: Share the Full POC
Share the `doc-composer-poc.zip` file which includes:
- The skill itself
- Sample documents and templates
- Demo scripts
- Complete documentation

## For Skill Recipients (Other Claude Code Users)

### Installation Instructions

#### Option A: Installing Just the Skill

1. **Save the skill to your Claude environment**:
   ```bash
   # Create a user skills directory (if it doesn't exist)
   mkdir -p /mnt/skills/user/
   
   # Unpack the .skill file
   unzip doc-composer-skill.skill -d /mnt/skills/user/
   ```

2. **Verify installation**:
   ```bash
   ls /mnt/skills/user/doc-composer-skill/
   # Should show: SKILL.md, scripts/, references/
   ```

#### Option B: Setting Up the Complete System

1. **Extract the full POC**:
   ```bash
   unzip doc-composer-poc.zip
   cd doc-composer-poc
   ```

2. **Customize for your organization**:
   ```bash
   # Replace the library documents with your own
   rm library/*.docx
   cp /path/to/your/templates/*.docx library/
   
   # Replace the master template
   cp /path/to/your/master-template.docx master-template/
   ```

3. **Install the skill**:
   ```bash
   cp -r doc-composer-skill /mnt/skills/user/
   ```

### Usage Instructions

#### Basic Usage with Claude Code

1. **Create a manifest file** (markdown):
   ```markdown
   # Monthly Report - January 2025
   
   - cover-page
   - executive-summary
   - department-updates
   - financial-summary
   - next-steps
   ```

2. **Ask Claude to generate the report**:
   > "Use the doc-composer skill to create my monthly report using the manifest I just created"

   Claude will:
   - Automatically detect and load the doc-composer skill
   - Read your manifest
   - Compose the document from your library
   - Preserve all formatting

#### Advanced Usage

**Custom Library Location**:
```python
# Tell Claude to use a specific library
"Compose a report using the Q1 manifest with documents from /shared/templates/2025/"
```

**Batch Processing**:
```python
# Process multiple reports
"Generate all monthly reports for Q1 using the manifests in /reports/q1/"
```

**Dynamic Content**:
```python
# Update content before composing
"Update the financial data in the library, then generate the board report"
```

### Customization Guide

#### Setting Up Your Document Library

1. **Naming Convention**:
   - Use descriptive names: `executive-summary.docx`, `financial-overview.docx`
   - Avoid spaces in filenames (use hyphens)
   - Keep to single-page documents for modularity

2. **Master Template Requirements**:
   - Include all corporate styles
   - Set up headers/footers
   - Define page numbering
   - Include any watermarks or backgrounds

3. **Creating Manifests**:
   ```markdown
   # [Report Title]
   
   ## Required Sections
   - document-name-1  # Without .docx extension
   - document-name-2
   - document-name-3
   
   ## Optional Sections (commented out)
   # - optional-section-1
   # - optional-section-2
   ```

### Extending the Skill

#### Adding Custom Functions

1. **Create a new script** in `scripts/`:
   ```python
   # scripts/custom_processor.py
   def process_with_data(manifest, data_source):
       """Add data injection capability."""
       pass
   ```

2. **Update the skill documentation** in `SKILL.md`:
   ```markdown
   ## Custom Features
   - Data injection: `python scripts/custom_processor.py`
   ```

#### Integration with Other Systems

**SharePoint Integration**:
```python
# Fetch documents from SharePoint instead of local library
python scripts/compose_document.py \
  --manifest report.md \
  --library "sharepoint://team/templates/" \
  --output final-report.docx
```

**Database-Driven Manifests**:
```python
# Generate manifest from database
python scripts/generate_manifest.py --query "SELECT * FROM report_sections WHERE report_type='quarterly'"
```

### Troubleshooting

**Common Issues**:

1. **"Skill not found"**:
   - Ensure skill is in `/mnt/skills/user/` or `/mnt/skills/public/`
   - Check permissions: `ls -la /mnt/skills/user/`

2. **"Document not in library"**:
   - Verify document name matches exactly (case-sensitive)
   - Check library path is correct
   - Don't include .docx extension in manifest

3. **"Formatting lost"**:
   - Ensure master template has all required styles
   - Use the merge_docx.py script (preserves formatting better)

### Best Practices

1. **Version Control**:
   - Keep library documents in git
   - Tag stable versions of the skill
   - Document changes in manifests

2. **Testing**:
   ```bash
   # Test with a simple manifest first
   echo "- cover-page" > test.md
   python scripts/compose_document.py --manifest test.md --library library/ --output test.docx
   ```

3. **Performance**:
   - Keep library documents under 1MB each
   - Use simple manifests (< 20 documents)
   - Pre-process complex formatting in library documents

### Support & Updates

- **Documentation**: See `SKILL.md` for complete API reference
- **Examples**: Check `references/workflow.md` for detailed examples
- **Updates**: Pull latest version from [your repository/location]

### Quick Start Checklist

- [ ] Received `.skill` file or `poc.zip`
- [ ] Installed skill in `/mnt/skills/user/`
- [ ] Created/customized document library
- [ ] Set up master template
- [ ] Created first manifest
- [ ] Successfully generated test document
- [ ] Integrated with Claude Code

## Example Claude Code Session

```
User: "I need to create our Q1 board presentation"

Claude: I'll help you create the Q1 board presentation using the doc-composer skill. 
Let me first check what's available...

[Claude reads the skill]
[Claude checks your library]
[Claude creates appropriate manifest if needed]
[Claude runs the composition]

Here's your completed Q1 board presentation with all sections properly formatted 
according to your corporate template: output/Q1-2025-Board-Presentation.docx
```

## Sharing Protocol

When sharing with a colleague:

1. **Package the skill**: `python scripts/package_skill.py doc-composer-skill/`
2. **Include this guide**: Share `DISTRIBUTION_GUIDE.md`
3. **Provide sample library**: Include 2-3 example documents
4. **Share a test manifest**: Include a simple manifest for testing
5. **Offer support**: Be available for initial setup questions

Remember: The skill is designed to be self-contained and work with any document library that follows the naming conventions!