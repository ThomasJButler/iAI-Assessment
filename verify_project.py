#!/usr/bin/env python3
"""
Project Verification Script for i.AI Assessment

This script verifies that all required files are present and have the correct structure.

Author: AI Evaluation Engineer
Date: 31/03/2025
"""

import os
import json
import sys
from typing import List, Dict, Any, Tuple

# Required files and directories
REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    "run_pipeline.sh",
    "run_pipeline.py",
    "summary.md",
    "plan.md",
    "scripts/data_generation.py",
    "scripts/theme_extraction.py",
    "scripts/theme_variation.py",
    "scripts/theme_comparison.py",
    "scripts/utils.py",
    "scripts/test_utils.py",
    "docs/themefinder_usage.md",
    "docs/metrics_explanation.md",
    "data/theme_descriptions.md"
]

# Sample data files
SAMPLE_FILES = [
    "data/sample_responses.json",
    "data/sample_theme_mapping_1.json",
    "data/sample_theme_mapping_2.json",
    "data/sample_comparison_results.json"
]

# Directories that should exist
REQUIRED_DIRS = [
    "scripts",
    "data",
    "docs",
    "data/visualizations"
]


def check_file_exists(file_path: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_path: Path to the file

    Returns:
        True if the file exists, False otherwise
    """
    return os.path.isfile(file_path)


def check_dir_exists(dir_path: str) -> bool:
    """
    Check if a directory exists.

    Args:
        dir_path: Path to the directory

    Returns:
        True if the directory exists, False otherwise
    """
    return os.path.isdir(dir_path)


def check_json_structure(file_path: str, expected_type: type) -> Tuple[bool, str]:
    """
    Check if a JSON file has the expected structure.

    Args:
        file_path: Path to the JSON file
        expected_type: Expected type of the JSON data

    Returns:
        Tuple of (success, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, expected_type):
            return False, f"Expected {expected_type.__name__}, got {type(data).__name__}"
        
        if expected_type == list and len(data) > 0:
            # Check if it's a theme mapping
            if isinstance(data[0], list) and len(data[0]) == 2:
                if not isinstance(data[0][0], str):
                    return False, "First element of each item should be a string (response)"
                if not isinstance(data[0][1], list):
                    return False, "Second element of each item should be a list (themes)"
                if len(data[0][1]) > 0 and not all(isinstance(theme, str) for theme in data[0][1]):
                    return False, "Themes should be strings"
        
        return True, "Valid JSON structure"
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except Exception as e:
        return False, f"Error checking JSON structure: {str(e)}"


def verify_project() -> List[str]:
    """
    Verify that all required files and directories are present and have the correct structure.

    Returns:
        List of error messages, empty if all checks pass
    """
    errors = []
    
    # Check required directories
    for dir_path in REQUIRED_DIRS:
        if not check_dir_exists(dir_path):
            errors.append(f"Missing directory: {dir_path}")
    
    # Check required files
    for file_path in REQUIRED_FILES:
        if not check_file_exists(file_path):
            errors.append(f"Missing required file: {file_path}")
    
    # Check sample files
    for file_path in SAMPLE_FILES:
        if not check_file_exists(file_path):
            errors.append(f"Missing sample file: {file_path}")
    
    # Check JSON structure of sample files
    if check_file_exists("data/sample_responses.json"):
        success, message = check_json_structure("data/sample_responses.json", list)
        if not success:
            errors.append(f"Invalid structure in data/sample_responses.json: {message}")
    
    if check_file_exists("data/sample_theme_mapping_1.json"):
        success, message = check_json_structure("data/sample_theme_mapping_1.json", list)
        if not success:
            errors.append(f"Invalid structure in data/sample_theme_mapping_1.json: {message}")
    
    if check_file_exists("data/sample_theme_mapping_2.json"):
        success, message = check_json_structure("data/sample_theme_mapping_2.json", list)
        if not success:
            errors.append(f"Invalid structure in data/sample_theme_mapping_2.json: {message}")
    
    if check_file_exists("data/sample_comparison_results.json"):
        success, message = check_json_structure("data/sample_comparison_results.json", dict)
        if not success:
            errors.append(f"Invalid structure in data/sample_comparison_results.json: {message}")
    
    # Check if scripts are executable
    executable_scripts = [
        "run_pipeline.sh",
        "run_pipeline.py",
        "scripts/data_generation.py",
        "scripts/theme_extraction.py",
        "scripts/theme_variation.py",
        "scripts/theme_comparison.py",
        "scripts/test_utils.py"
    ]
    
    for script in executable_scripts:
        if check_file_exists(script) and not os.access(script, os.X_OK):
            errors.append(f"Script is not executable: {script}")
    
    return errors


def main():
    """Main function to verify the project."""
    print("Verifying i.AI Assessment project...")
    
    errors = verify_project()
    
    if errors:
        print("\nErrors found:")
        for error in errors:
            print(f"  - {error}")
        print(f"\nTotal errors: {len(errors)}")
        sys.exit(1)
    else:
        print("\nAll checks passed! The project is complete and ready for submission.")
        sys.exit(0)


if __name__ == "__main__":
    main()
