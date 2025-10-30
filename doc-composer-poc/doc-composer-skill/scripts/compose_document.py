#!/usr/bin/env python3
"""
Document Composer - Main orchestration script
Composes Word documents from a library based on a manifest file.
"""

import os
import sys
import argparse
import re
from pathlib import Path
import subprocess

def parse_manifest(manifest_path):
    """Parse markdown manifest to extract document list."""
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Manifest file not found: {manifest_path}")
        sys.exit(1)
    
    # Extract items from bullet points (- or *)
    pattern = r'^\s*[-*]\s+(.+)$'
    documents = re.findall(pattern, content, re.MULTILINE)
    
    if not documents:
        print(f"Error: No documents found in manifest. Use - or * for bullet points.")
        sys.exit(1)
    
    return [doc.strip() for doc in documents]

def normalize_name(name):
    """Normalize a name for matching."""
    # Remove leading dash if present
    name = name.lstrip('-').strip()
    # Convert to lowercase
    name = name.lower()
    # Replace spaces, underscores, and hyphens with a single separator
    name = re.sub(r'[\s\-_]+', '-', name)
    # Remove special characters
    name = re.sub(r'[^\w\-]', '', name)
    return name

def find_best_match(target_name, library_path):
    """
    Find the best matching document in the library.
    Returns (exact_match, fuzzy_match, confidence_score)
    """
    from difflib import get_close_matches
    
    library = Path(library_path)
    target_normalized = normalize_name(target_name)
    
    # Get all .docx files in library
    available_docs = {}
    for doc_file in library.glob("*.docx"):
        # Store both original and normalized names
        original_name = doc_file.stem
        normalized = normalize_name(original_name)
        available_docs[normalized] = doc_file
    
    # First try exact match (after normalization)
    if target_normalized in available_docs:
        return available_docs[target_normalized], "exact", 1.0
    
    # Try fuzzy matching
    matches = get_close_matches(
        target_normalized, 
        available_docs.keys(), 
        n=1, 
        cutoff=0.6  # 60% similarity threshold
    )
    
    if matches:
        best_match = matches[0]
        # Calculate a simple similarity score
        score = sum(a == b for a, b in zip(target_normalized, best_match)) / max(len(target_normalized), len(best_match))
        return available_docs[best_match], "fuzzy", score
    
    return None, None, 0

def validate_documents(doc_names, library_path):
    """Validate documents exist with fuzzy matching support."""
    library = Path(library_path)
    if not library.exists():
        print(f"Error: Library directory not found: {library_path}")
        sys.exit(1)
    
    valid_docs = []
    fuzzy_matches = []
    missing_docs = []
    
    print("\nMatching documents from manifest to library...")
    for name in doc_names:
        doc_file, match_type, score = find_best_match(name, library_path)
        
        if doc_file:
            if match_type == "exact":
                print(f"  ✓ Found exact match: '{name}' → {doc_file.name}")
                valid_docs.append(str(doc_file))
            else:
                print(f"  ≈ Found fuzzy match ({score:.0%}): '{name}' → {doc_file.name}")
                fuzzy_matches.append((name, doc_file, score))
                valid_docs.append(str(doc_file))
        else:
            print(f"  ✗ No match found: '{name}'")
            missing_docs.append(name)
    
    # If there are fuzzy matches, optionally confirm with user
    if fuzzy_matches:
        print("\n⚠️  Fuzzy matches found. Please confirm:")
        for original, matched_file, score in fuzzy_matches:
            print(f"   '{original}' → '{matched_file.name}' (confidence: {score:.0%})")
        
        response = input("\nAccept these matches? (y/n): ")
        if response.lower() != 'y':
            print("\nFuzzy matches rejected. Available documents in library:")
            for doc in library.glob("*.docx"):
                print(f"  - {doc.stem}")
            sys.exit(0)
    
    # Handle missing documents
    if missing_docs:
        print(f"\n⚠️  Warning: {len(missing_docs)} documents not found in library")
        
        if not valid_docs:
            print("\nError: No valid documents found. Available documents:")
            for doc in library.glob("*.docx"):
                print(f"  - {doc.stem}")
            sys.exit(1)
        
        response = input("Continue with available documents? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    return valid_docs

def compose_document(manifest, library, master, output):
    """Main composition workflow."""
    print(f"\n=== Document Composer ===")
    print(f"Manifest: {manifest}")
    print(f"Library: {library}")
    print(f"Master: {master}")
    print(f"Output: {output}")
    print("=" * 25)
    
    # Step 1: Parse manifest
    print("\n1. Parsing manifest...")
    doc_names = parse_manifest(manifest)
    print(f"   Found {len(doc_names)} documents to compose:")
    for doc in doc_names:
        print(f"   - {doc}")
    
    # Step 2: Validate documents exist
    print("\n2. Validating documents...")
    doc_paths = validate_documents(doc_names, library)
    print(f"   Validated {len(doc_paths)} documents")
    
    # Step 3: Check master template exists
    print("\n3. Checking master template...")
    if not Path(master).exists():
        print(f"Error: Master template not found: {master}")
        sys.exit(1)
    print("   Master template found")
    
    # Step 4: Create output directory if needed
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Step 5: Call merge script
    print("\n4. Merging documents...")
    merge_script = Path(__file__).parent / "merge_docx.py"
    
    cmd = [
        sys.executable,
        str(merge_script),
        "--master", master,
        "--documents"] + doc_paths + [
        "--output", output
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("   Merge successful!")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error during merge: {e}")
        if e.stderr:
            print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: merge_docx.py script not found at {merge_script}")
        sys.exit(1)
    
    # Step 6: Verify output
    print("\n5. Verifying output...")
    if output_path.exists():
        size = output_path.stat().st_size
        print(f"   Success! Document created: {output}")
        print(f"   File size: {size:,} bytes")
    else:
        print(f"Error: Output file was not created")
        sys.exit(1)
    
    print("\n=== Composition Complete ===\n")
    return str(output_path)

def main():
    parser = argparse.ArgumentParser(
        description="Compose Word documents from library based on manifest"
    )
    parser.add_argument(
        "--manifest", required=True,
        help="Path to markdown manifest file"
    )
    parser.add_argument(
        "--library", default="./library",
        help="Path to document library directory (default: ./library)"
    )
    parser.add_argument(
        "--master", required=True,
        help="Path to master template document"
    )
    parser.add_argument(
        "--output", required=True,
        help="Path for output document"
    )
    
    args = parser.parse_args()
    
    compose_document(
        args.manifest,
        args.library,
        args.master,
        args.output
    )

if __name__ == "__main__":
    main()
