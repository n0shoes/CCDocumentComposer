#!/usr/bin/env python3
"""
Claude Code Integration Demo
Shows how Claude Code would use the document composer skill.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

def simulate_claude_code_request(user_request):
    """
    Simulates how Claude Code would process a user request.
    In real usage, Claude would read the skill and execute accordingly.
    """
    print("=" * 60)
    print("CLAUDE CODE SIMULATION")
    print("=" * 60)
    print(f"\n📝 User Request: \"{user_request}\"\n")
    
    # Step 1: Claude reads the skill
    print("1️⃣  Claude reads the doc-composer skill...")
    skill_path = Path("doc-composer-skill/SKILL.md")
    if skill_path.exists():
        print(f"   ✓ Skill loaded from {skill_path}")
    else:
        print("   ✗ Skill not found")
        return
    
    # Step 2: Claude identifies the task
    print("\n2️⃣  Claude analyzes the request...")
    print("   - Task: Generate quarterly report")
    print("   - Manifest: quarterly-report.md")
    print("   - Output: Q4-2024 report")
    
    # Step 3: Claude executes the composition
    print("\n3️⃣  Claude executes the document composition...")
    
    cmd = [
        sys.executable,
        "doc-composer-skill/scripts/compose_document.py",
        "--manifest", "manifests/quarterly-report.md",
        "--library", "library/",
        "--master", "master-template/corporate-template.docx",
        "--output", "output/Q4-2024-report.docx"
    ]
    
    print(f"   Command: {' '.join(cmd)}")
    print()
    
    # Execute the composition
    result = os.system(' '.join(cmd))
    
    if result == 0:
        print("\n✅ Document successfully composed!")
        
        # Step 4: Claude provides the result
        print("\n4️⃣  Claude's response to user:")
        print("-" * 40)
        print("I've successfully generated your Q4 2024 quarterly report.")
        print("The report includes the following sections:")
        print("  • Cover Page")
        print("  • Executive Summary")
        print("  • Financial Overview")
        print("  • Market Analysis")
        print("  • Risk Assessment")
        print("  • Strategic Initiatives")
        print("  • Conclusion")
        print()
        print("📄 Report saved to: output/Q4-2024-report.docx")
        print("The document maintains all corporate formatting from your")
        print("master template and preserves the formatting of each section.")
    else:
        print("\n❌ Document composition failed")

def demonstrate_variations():
    """Show different ways Claude Code could use the composer."""
    print("\n" + "=" * 60)
    print("ADDITIONAL USE CASES")
    print("=" * 60)
    
    examples = [
        {
            "scenario": "Board Meeting Materials",
            "request": "Create board presentation using the January board manifest",
            "manifest": "board-presentation.md",
            "output": "Board-Presentation-Jan-2025.docx"
        },
        {
            "scenario": "Custom Report",
            "request": "Generate a report with just financials and risks",
            "action": "Claude would create a custom manifest with only those sections"
        },
        {
            "scenario": "Batch Processing",
            "request": "Generate all quarterly reports for 2024",
            "action": "Claude would iterate through Q1, Q2, Q3, Q4 manifests"
        },
        {
            "scenario": "Dynamic Content",
            "request": "Update the financial data then generate the report",
            "action": "Claude would first update library/financial-overview.docx, then compose"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['scenario']}")
        print(f"   Request: \"{example['request']}\"")
        if "manifest" in example:
            print(f"   Manifest: {example['manifest']}")
            print(f"   Output: {example['output']}")
        else:
            print(f"   Action: {example['action']}")

def show_skill_benefits():
    """Highlight the benefits of using skills with Claude Code."""
    print("\n" + "=" * 60)
    print("BENEFITS OF SKILLS APPROACH")
    print("=" * 60)
    
    benefits = [
        ("Reusability", "The doc-composer skill can be used for any document composition task"),
        ("Consistency", "Every Claude instance uses the same proven workflow"),
        ("Efficiency", "No need to recreate complex logic each time"),
        ("Reliability", "Tested scripts ensure consistent results"),
        ("Extensibility", "Easy to add new features or document types"),
        ("Knowledge Transfer", "Skills capture best practices and domain expertise")
    ]
    
    for benefit, description in benefits:
        print(f"\n✨ {benefit}")
        print(f"   {description}")

def generate_sample_documents():
    """Generate sample documents if they don't exist."""
    if not Path("library/cover-page.docx").exists():
        print("\n" + "=" * 60)
        print("GENERATING SAMPLE DOCUMENTS")
        print("=" * 60)
        print("\nCreating sample Word documents for demonstration...")
        result = os.system(f"{sys.executable} generate_samples.py")
        if result == 0:
            print("\n✅ Sample documents created successfully!")
        else:
            print("\n⚠️  Could not create sample documents")
            print("Please run: python generate_samples.py")
            return False
    return True

def main():
    """Main demonstration flow."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " DOCUMENT COMPOSER POC - CLAUDE CODE INTEGRATION DEMO ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Check if we need to generate samples
    if not generate_sample_documents():
        return
    
    # Simulate Claude Code processing a request
    user_request = "Generate the Q4 2024 quarterly report using the quarterly-report manifest"
    simulate_claude_code_request(user_request)
    
    # Show additional use cases
    demonstrate_variations()
    
    # Highlight benefits
    show_skill_benefits()
    
    print("\n" + "=" * 60)
    print("READY FOR LEADERSHIP DEMONSTRATION")
    print("=" * 60)
    print("\n📊 This POC demonstrates:")
    print("  1. How Claude Code reads and uses skills")
    print("  2. Document composition from modular libraries")
    print("  3. Format preservation across documents")
    print("  4. Extensibility to various use cases")
    print("  5. Production-ready architecture")
    print("\n🚀 Next steps:")
    print("  • Package the skill: python scripts/package_skill.py doc-composer-skill/")
    print("  • Deploy to Claude Code environment")
    print("  • Extend with additional document types")
    print("  • Integrate with existing document management systems")
    print()

if __name__ == "__main__":
    main()
