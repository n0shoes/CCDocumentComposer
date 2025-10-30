#!/usr/bin/env python3
"""
Initialize a new skill with proper structure.
"""

import argparse
import os
from pathlib import Path
from datetime import datetime

def create_skill_structure(skill_name, output_path):
    """Create the skill directory structure and template files."""
    
    skill_dir = Path(output_path) / skill_name
    
    # Create directories
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)
    
    # Create SKILL.md template
    skill_md = skill_dir / "SKILL.md"
    skill_content = f"""---
name: {skill_name}
description: TODO: Add a comprehensive description of what this skill does and when to use it. Be specific and include key terms.
---

# {skill_name.replace('-', ' ').title()}

## Overview
TODO: Provide a brief overview of the skill's purpose and capabilities.

## Workflow

### Step 1: TODO
Describe the first step in the workflow.

### Step 2: TODO
Describe the second step in the workflow.

## Scripts
TODO: Document any scripts in the scripts/ directory.

## References
TODO: Document any reference files in the references/ directory.

## Examples
TODO: Provide usage examples.

```bash
# Example command
python scripts/example.py --input file.txt --output result.txt
```

## Notes
TODO: Add any additional notes or considerations.
"""
    
    with open(skill_md, 'w') as f:
        f.write(skill_content)
    
    # Create example script
    example_script = skill_dir / "scripts" / "example.py"
    script_content = f'''#!/usr/bin/env python3
"""
Example script for {skill_name} skill.
TODO: Replace with actual implementation.
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description="Example script for {skill_name}")
    parser.add_argument("--input", required=True, help="Input file")
    parser.add_argument("--output", required=True, help="Output file")
    
    args = parser.parse_args()
    
    print(f"Processing {{args.input}} -> {{args.output}}")
    # TODO: Implement actual functionality

if __name__ == "__main__":
    main()
'''
    
    with open(example_script, 'w') as f:
        f.write(script_content)
    os.chmod(example_script, 0o755)
    
    # Create example reference
    example_ref = skill_dir / "references" / "example-reference.md"
    ref_content = f"""# Example Reference for {skill_name}

TODO: Replace with actual reference documentation.

## Section 1
Documentation content here.

## Section 2
More documentation content.
"""
    
    with open(example_ref, 'w') as f:
        f.write(ref_content)
    
    # Create placeholder asset
    example_asset = skill_dir / "assets" / "README.txt"
    asset_content = f"""Assets Directory for {skill_name}

Place any files that should be used in outputs here:
- Templates
- Images
- Icons
- Sample files
- Etc.

These files are not loaded into context but are used by the skill.
"""
    
    with open(example_asset, 'w') as f:
        f.write(asset_content)
    
    print(f"✅ Skill '{skill_name}' initialized at: {skill_dir}")
    print("\nCreated structure:")
    print(f"  {skill_name}/")
    print(f"    ├── SKILL.md")
    print(f"    ├── scripts/")
    print(f"    │   └── example.py")
    print(f"    ├── references/")
    print(f"    │   └── example-reference.md")
    print(f"    └── assets/")
    print(f"        └── README.txt")
    print("\nNext steps:")
    print("  1. Edit SKILL.md with your skill instructions")
    print("  2. Add/modify scripts in scripts/")
    print("  3. Add reference docs in references/")
    print("  4. Add assets in assets/")
    print(f"  5. Package with: python scripts/package_skill.py {skill_dir}")

def main():
    parser = argparse.ArgumentParser(description="Initialize a new skill")
    parser.add_argument("skill_name", help="Name of the skill (use-hyphens)")
    parser.add_argument("--path", default=".", help="Output directory (default: current)")
    
    args = parser.parse_args()
    
    # Validate skill name
    if not args.skill_name.replace('-', '').replace('_', '').isalnum():
        print("Error: Skill name should contain only letters, numbers, hyphens, and underscores")
        return 1
    
    create_skill_structure(args.skill_name, args.path)
    return 0

if __name__ == "__main__":
    exit(main())
