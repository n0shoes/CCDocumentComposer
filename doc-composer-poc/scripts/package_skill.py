#!/usr/bin/env python3
"""
Package a skill into a distributable .skill file.
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path
import yaml
import re

def validate_skill(skill_dir):
    """Validate skill structure and requirements."""
    errors = []
    warnings = []
    
    skill_path = Path(skill_dir)
    
    # Check if directory exists
    if not skill_path.exists():
        errors.append(f"Skill directory not found: {skill_dir}")
        return errors, warnings
    
    # Check for SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md file is required")
        return errors, warnings
    
    # Parse and validate SKILL.md
    with open(skill_md, 'r') as f:
        content = f.read()
    
    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("SKILL.md must have YAML frontmatter")
        return errors, warnings
    
    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML frontmatter: {e}")
        return errors, warnings
    
    # Validate required fields
    if 'name' not in frontmatter:
        errors.append("Frontmatter must include 'name' field")
    elif not frontmatter['name']:
        errors.append("'name' field cannot be empty")
    
    if 'description' not in frontmatter:
        errors.append("Frontmatter must include 'description' field")
    elif not frontmatter['description']:
        errors.append("'description' field cannot be empty")
    elif 'TODO' in frontmatter['description']:
        warnings.append("Description contains TODO - please complete it")
    elif len(frontmatter['description']) < 50:
        warnings.append("Description seems too short - be more specific")
    
    # Check for extraneous fields
    allowed_fields = {'name', 'description', 'license'}
    extra_fields = set(frontmatter.keys()) - allowed_fields
    if extra_fields:
        warnings.append(f"Unexpected frontmatter fields: {', '.join(extra_fields)}")
    
    # Check body content
    body = content[len(frontmatter_match.group(0)):]
    if 'TODO' in body:
        warnings.append("SKILL.md body contains TODO items")
    
    # Check directory structure
    for subdir in ['scripts', 'references', 'assets']:
        subpath = skill_path / subdir
        if subpath.exists() and subpath.is_dir():
            # Check if directory has content
            if not any(subpath.iterdir()):
                warnings.append(f"{subdir}/ directory is empty - consider removing it")
    
    # Check for unnecessary files
    unnecessary_files = ['README.md', 'INSTALLATION.md', 'CHANGELOG.md', '.git', '.gitignore']
    for file in unnecessary_files:
        if (skill_path / file).exists():
            warnings.append(f"Found {file} - skills should not include auxiliary documentation")
    
    return errors, warnings

def package_skill(skill_dir, output_dir=None):
    """Package the skill into a .skill file."""
    
    skill_path = Path(skill_dir)
    skill_name = skill_path.name
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()
    
    skill_file = output_path / f"{skill_name}.skill"
    
    # Create zip file
    print(f"Packaging skill: {skill_name}")
    
    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add all files in the skill directory
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # Get relative path
                rel_path = file_path.relative_to(skill_path.parent)
                # Add to zip
                zf.write(file_path, rel_path)
                print(f"  Added: {rel_path}")
    
    # Get file size
    size = skill_file.stat().st_size
    size_kb = size / 1024
    
    print(f"\n✅ Skill packaged successfully!")
    print(f"   File: {skill_file}")
    print(f"   Size: {size_kb:.1f} KB")
    
    return skill_file

def main():
    parser = argparse.ArgumentParser(
        description="Package a skill into a distributable .skill file"
    )
    parser.add_argument(
        "skill_dir",
        help="Path to the skill directory to package"
    )
    parser.add_argument(
        "output_dir",
        nargs='?',
        help="Output directory for .skill file (default: current directory)"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip validation checks"
    )
    
    args = parser.parse_args()
    
    # Validate the skill
    if not args.skip_validation:
        print("Validating skill...")
        errors, warnings = validate_skill(args.skill_dir)
        
        if errors:
            print("\n❌ Validation failed with errors:")
            for error in errors:
                print(f"   ERROR: {error}")
            
            if warnings:
                print("\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"   WARNING: {warning}")
            
            print("\nFix the errors and try again, or use --skip-validation to force packaging")
            return 1
        
        if warnings:
            print("\n⚠️  Validation passed with warnings:")
            for warning in warnings:
                print(f"   WARNING: {warning}")
            
            response = input("\nContinue packaging? (y/n): ")
            if response.lower() != 'y':
                print("Packaging cancelled")
                return 0
        else:
            print("✅ Validation passed!\n")
    
    # Package the skill
    try:
        skill_file = package_skill(args.skill_dir, args.output_dir)
        
        print("\n📦 Your skill is ready for distribution!")
        print("   Users can install it by:")
        print(f"   1. Saving {skill_file.name} to their skills directory")
        print("   2. Unzipping it to access the skill")
        print("   3. Claude Code will automatically detect and use it")
        
    except Exception as e:
        print(f"\n❌ Error packaging skill: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
