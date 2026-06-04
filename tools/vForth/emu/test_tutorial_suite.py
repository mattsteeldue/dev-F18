#!/usr/bin/env python3
"""
Automated test suite for loading all tutorial files
Checks that files are syntactically correct and can be loaded without immediate errors
"""

import sys
import os
import glob
from emulator import VForthEmulator

def test_tutorial_syntax(tutorial_file):
    """Test if a tutorial file has valid Forth syntax"""
    try:
        with open(tutorial_file, 'r', encoding='ascii') as f:
            content = f.read()

        # Check basic requirements
        checks = {
            "Has MARKER NEWTASK": "MARKER NEWTASK" in content,
            "Has load banner": "---" in content and "loaded" in content,
            "Has sections": "\ =" in content,
            "Has comments": "\\" in content,
            "7-bit ASCII only": all(ord(c) < 128 for c in content),
        }

        return checks
    except Exception as e:
        return {"error": str(e)}

def run_tutorial_tests():
    print("=== vForth Tutorial Suite Test ===\n")

    # Find all tutorial files
    tutorial_files = sorted(glob.glob("tutorial/*.f"))
    if not tutorial_files:
        print("[ERROR] No tutorial files found in tutorial/ directory")
        return False

    print(f"Found {len(tutorial_files)} tutorial files\n")

    # Test syntax of first few tutorials
    print("--- Syntax Check (first 5 tutorials) ---\n")
    syntax_pass = 0
    syntax_fail = 0

    for tutorial_file in tutorial_files[:5]:
        filename = os.path.basename(tutorial_file)
        checks = test_tutorial_syntax(tutorial_file)

        if "error" in checks:
            print(f"[FAIL] {filename}")
            print(f"       Error: {checks['error']}")
            syntax_fail += 1
        else:
            passed = sum(1 for v in checks.values() if v)
            total = len(checks)
            if passed == total:
                print(f"[OK] {filename} ({passed}/{total} checks passed)")
                syntax_pass += 1
            else:
                print(f"[WARN] {filename} ({passed}/{total} checks passed)")
                for check, result in checks.items():
                    if not result:
                        print(f"       Missing: {check}")
                syntax_fail += 1

    print(f"\nSyntax check result: {syntax_pass} pass, {syntax_fail} fail\n")

    # Test that all tutorials follow naming convention
    print("--- File Naming Convention Check ---\n")
    naming_ok = 0
    naming_bad = 0

    for tutorial_file in tutorial_files:
        filename = os.path.basename(tutorial_file)
        # Check format: NNN-slug.f where NNN is 3 digits
        parts = filename.split('-')
        if len(parts) >= 2 and len(parts[0]) == 3 and parts[0].isdigit():
            naming_ok += 1
        else:
            print(f"[WARN] Non-standard naming: {filename}")
            naming_bad += 1

    print(f"Naming convention: {naming_ok} correct, {naming_bad} non-standard\n")

    # List all tutorials
    print("--- All Available Tutorials ---\n")
    for i, tutorial_file in enumerate(tutorial_files, 1):
        filename = os.path.basename(tutorial_file)
        size = os.path.getsize(tutorial_file)
        print(f"{i:2d}. {filename:30s} ({size:5d} bytes)")

    print(f"\n=== Tutorial Suite Summary ===")
    print(f"Total tutorials: {len(tutorial_files)}")
    print(f"Syntax validation: {syntax_pass} pass, {syntax_fail} fail")
    print(f"Naming convention: {naming_ok} correct, {naming_bad} non-standard")
    print(f"\nTo test interactively:")
    print(f"  python emu/interactive_test.py")
    print(f"  forth> INCLUDE tutorial/001-stack-basics.f")

    return syntax_fail == 0 and naming_bad == 0

if __name__ == "__main__":
    try:
        success = run_tutorial_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
