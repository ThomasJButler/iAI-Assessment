#!/usr/bin/env python3
"""
Test Script for Utility Functions

This script tests the utility functions used in the i.AI Assessment.

Author: AI Evaluation Engineer
Date: 31/03/2025
"""

import os
import unittest
import tempfile
import json
from typing import List, Dict, Any

# Import utility functions
from utils import (
    calculate_jaccard_similarity,
    calculate_jaccard_similarities,
    validate_theme_mapping,
    load_json,
    save_json,
    load_text,
    save_text,
    parse_variation_level
)


class TestUtilityFunctions(unittest.TestCase):
    """Test case for utility functions."""

    def test_jaccard_similarity(self):
        """Test Jaccard similarity calculation."""
        # Test with identical sets
        self.assertEqual(calculate_jaccard_similarity({"A", "B", "C"}, {"A", "B", "C"}), 1.0)
        
        # Test with disjoint sets
        self.assertEqual(calculate_jaccard_similarity({"A", "B", "C"}, {"D", "E", "F"}), 0.0)
        
        # Test with overlapping sets
        self.assertEqual(calculate_jaccard_similarity({"A", "B", "C"}, {"A", "B", "D"}), 0.5)
        
        # Test with empty sets
        self.assertEqual(calculate_jaccard_similarity(set(), set()), 1.0)
        self.assertEqual(calculate_jaccard_similarity({"A", "B"}, set()), 0.0)

    def test_jaccard_similarities(self):
        """Test Jaccard similarities calculation for theme mappings."""
        mapping1 = [
            ["Response 1", ["Theme A", "Theme B"]],
            ["Response 2", ["Theme C", "Theme D"]],
            ["Response 3", ["Theme A", "Theme C"]]
        ]
        
        mapping2 = [
            ["Response 1", ["Theme A", "Theme C"]],
            ["Response 2", ["Theme C", "Theme D"]],
            ["Response 3", ["Theme B", "Theme D"]]
        ]
        
        similarities = calculate_jaccard_similarities(mapping1, mapping2)
        
        self.assertEqual(len(similarities), 3)
        self.assertEqual(similarities[0], 1/3)  # Jaccard of {"A", "B"} and {"A", "C"}
        self.assertEqual(similarities[1], 1.0)  # Jaccard of {"C", "D"} and {"C", "D"}
        self.assertEqual(similarities[2], 0.0)  # Jaccard of {"A", "C"} and {"B", "D"}

    def test_validate_theme_mapping(self):
        """Test theme mapping validation."""
        # Valid mapping
        valid_mapping = [
            ["Response 1", ["Theme A", "Theme B"]],
            ["Response 2", ["Theme C"]]
        ]
        self.assertTrue(validate_theme_mapping(valid_mapping))
        
        # Invalid mappings
        invalid_mappings = [
            # Not a list
            "not a list",
            
            # Item not a list
            ["Response 1", ["Theme A"]],
            
            # Item too short
            [["Response 1"]],
            
            # Item too long
            [["Response 1", ["Theme A"], "extra"]],
            
            # First element not a string
            [[123, ["Theme A"]]],
            
            # Second element not a list
            [["Response 1", "not a list"]],
            
            # Theme not a string
            [["Response 1", ["Theme A", 123]]]
        ]
        
        for mapping in invalid_mappings:
            self.assertFalse(validate_theme_mapping(mapping))

    def test_json_operations(self):
        """Test JSON loading and saving."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Test data
            test_data = {
                "string": "value",
                "number": 123,
                "list": [1, 2, 3],
                "nested": {"key": "value"}
            }
            
            # Save and load
            self.assertTrue(save_json(test_data, temp_path))
            loaded_data = load_json(temp_path)
            
            # Verify
            self.assertEqual(loaded_data, test_data)
            
            # Test loading non-existent file
            self.assertIsNone(load_json("non_existent_file.json"))
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_text_operations(self):
        """Test text loading and saving."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Test data
            test_text = "This is a test\nWith multiple lines\nAnd special characters: !@#$%^&*()"
            
            # Save and load
            self.assertTrue(save_text(test_text, temp_path))
            loaded_text = load_text(temp_path)
            
            # Verify
            self.assertEqual(loaded_text, test_text)
            
            # Test loading non-existent file
            self.assertIsNone(load_text("non_existent_file.txt"))
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_parse_variation_level(self):
        """Test variation level parsing."""
        # Valid values
        self.assertEqual(parse_variation_level("0"), 0.0)
        self.assertEqual(parse_variation_level("0.5"), 0.5)
        self.assertEqual(parse_variation_level("1"), 1.0)
        
        # Invalid values
        with self.assertRaises(ValueError):
            parse_variation_level("not a number")
        
        with self.assertRaises(ValueError):
            parse_variation_level("-0.1")
        
        with self.assertRaises(ValueError):
            parse_variation_level("1.1")


if __name__ == "__main__":
    unittest.main()
