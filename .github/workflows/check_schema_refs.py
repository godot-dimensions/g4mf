#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JSON Schema reference checker for G4MF specification.
Validates that all $ref properties in JSON schemas point to existing schema files.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def find_schema_files(root_path: Path) -> List[Path]:
    """Find all JSON schema files in the given directory."""
    schema_files = []
    for path in root_path.rglob("*.schema.json"):
        schema_files.append(path)
    return schema_files


def extract_refs(obj: Any, current_path: Optional[List[str]] = None) -> List[Tuple[str, str]]:
    """
    Recursively extract all $ref values from a JSON schema object.
    Returns list of (ref_value, json_path) tuples.
    """
    if current_path is None:
        current_path = []
    refs = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = current_path + [key]
            if key == "$ref":
                # Skip external schema references (URLs)
                if isinstance(value, str) and not value.startswith(("http://", "https://")):
                    path_str = ".".join(new_path)
                    refs.append((value, path_str))
            else:
                refs.extend(extract_refs(value, new_path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_path = current_path + [f"[{i}]"]
            refs.extend(extract_refs(item, new_path))
    return refs


def check_ref(ref: str, source_file: Path, root_path: Path) -> Tuple[bool, str]:
    """
    Check if a $ref is valid.
    Returns (is_valid, error_message) tuple.
    """
    # Split ref into file path and JSON pointer (if any)
    if "#" in ref:
        file_part, pointer = ref.split("#", 1)
    else:
        file_part, pointer = ref, None
    # Skip empty file parts (references to same file)
    if not file_part:
        return True, ""
    # Resolve relative path from source file's directory
    source_dir = source_file.parent
    target_file = (source_dir / file_part).resolve()
    # Check if target file exists
    if not target_file.exists():
        return False, f"Referenced schema does not exist: {file_part}"
    # Check if it's actually in the schema directory
    try:
        target_file.relative_to(root_path / "specification" / "schema")
    except ValueError:
        return False, f"Referenced file is outside schema directory: {file_part}"
    # Optional: We could validate the JSON pointer exists in the target schema,
    # but that's more complex and may not be necessary for basic validation
    return True, ""


def main():
    if len(sys.argv) < 2:
        print("Usage: check_schema_refs.py <file1.schema.json> [file2.schema.json ...]")
        print("   or: check_schema_refs.py --all")
        sys.exit(1)
    # Determine root path (repository root)
    script_path = Path(__file__).resolve()
    root_path = script_path.parent.parent.parent
    schema_dir = root_path / "specification" / "schema"
    # Get list of files to check
    if sys.argv[1] == "--all":
        files_to_check = find_schema_files(schema_dir)
    else:
        files_to_check = [Path(f).resolve() for f in sys.argv[1:]]
    # Track errors
    errors = []
    files_checked = 0
    refs_checked = 0
    for schema_file in files_to_check:
        if not schema_file.exists():
            errors.append(f"File does not exist: {schema_file}")
            continue
        files_checked += 1
        try:
            with open(schema_file, "r", encoding="utf-8") as f:
                schema_data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in {schema_file.relative_to(root_path)}: {e}")
            continue
        except Exception as e:
            errors.append(f"Could not read {schema_file.relative_to(root_path)}: {e}")
            continue
        # Extract and check all $ref values
        refs = extract_refs(schema_data)
        for ref_value, json_path in refs:
            refs_checked += 1
            is_valid, error_msg = check_ref(ref_value, schema_file, root_path)
            if not is_valid:
                try:
                    rel_path = schema_file.relative_to(root_path)
                except ValueError:
                    rel_path = schema_file
                errors.append(f"{rel_path}: {error_msg}")
                errors.append(f"  At: {json_path}")
                errors.append(f"  $ref: {ref_value}")
    # Print results
    if errors:
        print(f"❌ Found {len(errors)//3} broken schema reference(s) in {files_checked} file(s):")
        print()
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        print(f"✅ All {refs_checked} schema reference(s) in {files_checked} schema file(s) are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
