#!/usr/bin/env python3
"""
Test script to verify the git repository loading functionality
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from tracespec.app import load_requirements_from_repo, resolve_filepath
from tracespec.utils import extract_subsystem

def test_load_requirements():
    """Test loading requirements from the git repository."""
    print("Testing load_requirements_from_repo()...")

    try:
        requirements = load_requirements_from_repo()
        print(f"✓ Loaded {len(requirements)} subsystems: {list(requirements.keys())}")

        total_reqs = sum(len(v) for v in requirements.values())
        print(f"✓ Total requirements: {total_reqs}")

        # Test a specific requirement
        for subsystem, reqs in requirements.items():
            if reqs:
                req = reqs[0]
                print(f"✓ Sample requirement from {subsystem}: {req['requirement_id']}")
                print(f"  Text: {req['requirement_text'][:50]}...")
                break

    except Exception as e:
        print(f"✗ Error loading requirements: {e}")
        return False

    return True

def test_resolve_filepath():
    """Test the resolve_filepath function."""
    print("\nTesting resolve_filepath()...")

    test_cases = [
        "SYSAUTH00001",
        "SYSAPI00001",
        "SYSNAV00001"
    ]

    for req_id in test_cases:
        try:
            filepath = resolve_filepath(req_id)
            subsystem = extract_subsystem(req_id)
            expected_path = f"requirements_repo/requirements/{subsystem.lower()}/{req_id}.json"

            if filepath.exists():
                print(f"✓ {req_id} -> {filepath} (exists)")
            else:
                print(f"? {req_id} -> {filepath} (file not found)")

        except Exception as e:
            print(f"✗ Error resolving {req_id}: {e}")

def test_extract_subsystem():
    """Test the subsystem extraction function."""
    print("\nTesting extract_subsystem()...")

    test_cases = [
        ("SYSAUTH00001", "AUTH"),
        ("SYSAPI00001", "API"),
        ("SYSNAV00002", "NAV"),
        ("SYSMOB00001", "MOB"),
        ("SYSDATA00001", "DATA")
    ]

    for req_id, expected in test_cases:
        result = extract_subsystem(req_id)
        if result == expected:
            print(f"✓ {req_id} -> {result}")
        else:
            print(f"✗ {req_id} -> {result} (expected {expected})")

if __name__ == "__main__":
    print("TraceSpec Git Repository Loading Test")
    print("=" * 50)

    success = True
    success &= test_load_requirements()
    test_resolve_filepath()
    test_extract_subsystem()

    print("\n" + "=" * 50)
    if success:
        print("✓ All tests completed successfully!")
    else:
        print("✗ Some tests failed!")
