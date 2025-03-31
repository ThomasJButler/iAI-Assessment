#!/usr/bin/env python3
"""
Utility Functions for i.AI Assessment

This script provides common utility functions used across the assessment tasks.

Author: AI Evaluation Engineer
Date: 31/03/2025
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Union

# Configure logging
def setup_logging(log_file: str = "assessment.log") -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        log_file: Path to the log file

    Returns:
        Configured logger
    """
    logger = logging.getLogger("assessment")
    
    if not logger.handlers:  # Only add handlers if they don't exist
        logger.setLevel(logging.INFO)
        
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# File operations
def ensure_directory(directory_path: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)

def load_json(file_path: str) -> Any:
    """
    Load data from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Loaded data, or None if loading fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger = logging.getLogger("assessment")
        logger.error(f"Error loading JSON from {file_path}: {str(e)}")
        return None

def save_json(data: Any, file_path: str, indent: int = 2) -> bool:
    """
    Save data to a JSON file.

    Args:
        data: Data to save
        file_path: Path to the output file
        indent: Indentation level for JSON formatting

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        ensure_directory(os.path.dirname(file_path))
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        logger = logging.getLogger("assessment")
        logger.error(f"Error saving JSON to {file_path}: {str(e)}")
        return False

def load_text(file_path: str) -> Optional[str]:
    """
    Load text from a file.

    Args:
        file_path: Path to the text file

    Returns:
        Loaded text, or None if loading fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    except Exception as e:
        logger = logging.getLogger("assessment")
        logger.error(f"Error loading text from {file_path}: {str(e)}")
        return None

def save_text(text: str, file_path: str) -> bool:
    """
    Save text to a file.

    Args:
        text: Text to save
        file_path: Path to the output file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        ensure_directory(os.path.dirname(file_path))
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        logger = logging.getLogger("assessment")
        logger.error(f"Error saving text to {file_path}: {str(e)}")
        return False

# Data validation
def validate_theme_mapping(mapping: List[List]) -> bool:
    """
    Validate the structure of a theme mapping.

    Args:
        mapping: Theme mapping to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(mapping, list):
        return False
    
    for item in mapping:
        # Each item should be a list with 2 elements: [response, themes]
        if not isinstance(item, list) or len(item) != 2:
            return False
        
        # First element should be a string (response)
        if not isinstance(item[0], str):
            return False
        
        # Second element should be a list of strings (themes)
        if not isinstance(item[1], list) or not all(isinstance(theme, str) for theme in item[1]):
            return False
    
    return True

# Metrics calculation
def calculate_jaccard_similarity(set1: set, set2: set) -> float:
    """
    Calculate Jaccard similarity between two sets.

    Args:
        set1: First set
        set2: Second set

    Returns:
        Jaccard similarity (0.0 to 1.0)
    """
    if not set1 and not set2:
        return 1.0  # Both empty sets are considered identical
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union

def calculate_jaccard_similarities(mapping1: List[List], mapping2: List[List]) -> List[float]:
    """
    Calculate Jaccard similarities for each pair of theme sets in the mappings.

    Args:
        mapping1: First theme mapping
        mapping2: Second theme mapping

    Returns:
        List of Jaccard similarities
    """
    similarities = []
    
    for i in range(min(len(mapping1), len(mapping2))):
        _, themes1 = mapping1[i]
        _, themes2 = mapping2[i]
        
        set1 = set(themes1)
        set2 = set(themes2)
        
        similarity = calculate_jaccard_similarity(set1, set2)
        similarities.append(similarity)
    
    return similarities

# Command line helpers
def parse_variation_level(value: str) -> float:
    """
    Parse and validate a variation level from a string.

    Args:
        value: String representation of the variation level

    Returns:
        Validated variation level (0.0 to 1.0)

    Raises:
        ValueError: If the value is not a valid variation level
    """
    try:
        level = float(value)
        if level < 0.0 or level > 1.0:
            raise ValueError(f"Variation level must be between 0.0 and 1.0, got {level}")
        return level
    except ValueError:
        raise ValueError(f"Invalid variation level: {value}")

import time
from datetime import datetime

# AI usage documentation
def document_ai_usage(task: str, usage_details: Dict[str, Any], output_file: str = "ai_usage.json") -> None:
    """
    Document the use of AI assistance in the assessment.

    Args:
        task: Name of the task
        usage_details: Details of AI usage
        output_file: Path to the output file
    """
    # Load existing documentation if it exists
    existing_data = load_json(output_file) or {}
    
    # Add or update the task entry
    existing_data[task] = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **usage_details
    }
    
    # Save the updated documentation
    save_json(existing_data, output_file)

# Main function for testing
if __name__ == "__main__":
    # Set up logging
    logger = setup_logging()
    logger.info("Utility functions loaded successfully")
    
    # Test JSON operations
    test_data = {"test": "data", "nested": {"value": 123}}
    save_json(test_data, "test_output.json")
    loaded_data = load_json("test_output.json")
    
    if loaded_data == test_data:
        logger.info("JSON operations working correctly")
    else:
        logger.error("JSON operations failed")
    
    # Clean up test file
    if os.path.exists("test_output.json"):
        os.remove("test_output.json")
