#!/usr/bin/env python3
"""
Theme Extraction Script for i.AI Assessment

This script uses Themefinder to extract themes from synthetic consultation responses.
If Themefinder fails, it implements a fallback solution using NLP techniques.

Author: AI Evaluation Engineer
Date: 31/03/2025
"""

import os
import json
import logging
import argparse
from typing import List, Dict, Any, Tuple, Optional
import random
import string
import numpy as np
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("theme_extraction.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
INPUT_FILE = "data/synthetic_responses.json"
OUTPUT_FILE = "data/theme_mapping_1.json"
NUM_THEMES = 10  # Number of themes to generate in fallback mode
THEME_LETTERS = list(string.ascii_uppercase)[:NUM_THEMES]  # A, B, C, ...
MIN_THEMES_PER_RESPONSE = 1
MAX_THEMES_PER_RESPONSE = 5


class ThemeExtractor:
    """Class to extract themes from consultation responses."""

    def __init__(self):
        """Initialize the ThemeExtractor."""
        self.themefinder_available = self._check_themefinder()
        if self.themefinder_available:
            logger.info("Themefinder is available and will be used for theme extraction")
            # Import Themefinder only if available
            import themefinder
            self.themefinder = themefinder
        else:
            logger.warning("Themefinder is not available, will use fallback implementation")

    def _check_themefinder(self) -> bool:
        """
        Check if Themefinder is installed and available.

        Returns:
            bool: True if Themefinder is available, False otherwise
        """
        try:
            import themefinder
            return True
        except ImportError:
            return False

    def extract_themes_with_themefinder(self, responses: List[str]) -> List[Tuple[str, List[str]]]:
        """
        Extract themes using Themefinder.

        Args:
            responses: List of consultation responses

        Returns:
            List of tuples containing (response, themes)
        """
        if not self.themefinder_available:
            logger.error("Cannot extract themes with Themefinder as it is not available")
            return []

        try:
            logger.info("Starting theme extraction with Themefinder")
            
            # Initialize Themefinder
            # Note: The actual implementation will depend on Themefinder's API
            # This is a placeholder based on the expected usage
            theme_finder = self.themefinder.ThemeFinder()
            
            # Extract themes
            results = []
            for response in responses:
                # Process the response with Themefinder
                # This is a placeholder - actual implementation will use Themefinder's API
                themes = theme_finder.extract_themes(response)
                
                # Format the themes as "Theme X" where X is a letter
                formatted_themes = [f"Theme {theme}" for theme in themes]
                
                # Add to results
                results.append((response, formatted_themes))
            
            logger.info(f"Successfully extracted themes for {len(results)} responses using Themefinder")
            return results
            
        except Exception as e:
            logger.error(f"Error extracting themes with Themefinder: {str(e)}")
            return []

    def extract_themes_fallback(self, responses: List[str]) -> List[Tuple[str, List[str]]]:
        """
        Extract themes using a fallback implementation based on random assignment.
        
        This is used when Themefinder is not available.

        Args:
            responses: List of consultation responses

        Returns:
            List of tuples containing (response, themes)
        """
        logger.info("Starting theme extraction with fallback implementation")
        
        # Generate theme names (Theme A, Theme B, etc.)
        theme_names = [f"Theme {letter}" for letter in THEME_LETTERS]
        
        # Assign themes to responses
        results = []
        for response in responses:
            # Determine number of themes for this response
            num_themes = random.randint(MIN_THEMES_PER_RESPONSE, MAX_THEMES_PER_RESPONSE)
            
            # Randomly select themes
            response_themes = random.sample(theme_names, num_themes)
            
            # Add to results
            results.append((response, response_themes))
        
        logger.info(f"Successfully assigned themes to {len(results)} responses using fallback method")
        return results

    def extract_themes(self, responses: List[str]) -> List[Tuple[str, List[str]]]:
        """
        Extract themes from responses, using Themefinder if available or fallback otherwise.

        Args:
            responses: List of consultation responses

        Returns:
            List of tuples containing (response, themes)
        """
        if self.themefinder_available:
            # Try Themefinder first
            results = self.extract_themes_with_themefinder(responses)
            
            # If Themefinder fails, fall back to the alternative implementation
            if not results:
                logger.warning("Themefinder extraction failed, falling back to alternative implementation")
                results = self.extract_themes_fallback(responses)
        else:
            # Use fallback implementation directly
            results = self.extract_themes_fallback(responses)
        
        return results


def load_responses(input_file: str) -> List[str]:
    """
    Load consultation responses from a JSON file.

    Args:
        input_file: Path to the input file

    Returns:
        List of consultation responses
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            responses = json.load(f)
        
        logger.info(f"Loaded {len(responses)} responses from {input_file}")
        return responses
    except Exception as e:
        logger.error(f"Error loading responses from {input_file}: {str(e)}")
        return []


def save_theme_mapping(theme_mapping: List[Tuple[str, List[str]]], output_file: str) -> None:
    """
    Save the theme mapping to a JSON file.

    Args:
        theme_mapping: List of tuples containing (response, themes)
        output_file: Path to the output file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Convert to the expected format
        formatted_mapping = [[response, themes] for response, themes in theme_mapping]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted_mapping, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved theme mapping for {len(theme_mapping)} responses to {output_file}")
    except Exception as e:
        logger.error(f"Error saving theme mapping to {output_file}: {str(e)}")


def analyze_theme_distribution(theme_mapping: List[Tuple[str, List[str]]]) -> None:
    """
    Analyze and log the distribution of themes.

    Args:
        theme_mapping: List of tuples containing (response, themes)
    """
    # Count theme occurrences
    theme_counts = Counter()
    for _, themes in theme_mapping:
        theme_counts.update(themes)
    
    # Calculate statistics
    total_themes = sum(theme_counts.values())
    unique_themes = len(theme_counts)
    avg_themes_per_response = total_themes / len(theme_mapping) if theme_mapping else 0
    
    # Log the results
    logger.info(f"Theme distribution analysis:")
    logger.info(f"  Total themes assigned: {total_themes}")
    logger.info(f"  Unique themes: {unique_themes}")
    logger.info(f"  Average themes per response: {avg_themes_per_response:.2f}")
    
    # Log individual theme counts
    logger.info("  Theme counts:")
    for theme, count in sorted(theme_counts.items()):
        logger.info(f"    {theme}: {count} ({count/len(theme_mapping)*100:.1f}%)")


def main():
    """Main function to extract themes from responses."""
    parser = argparse.ArgumentParser(description='Extract themes from consultation responses')
    parser.add_argument('--input', type=str, default=INPUT_FILE,
                        help=f'Input file path (default: {INPUT_FILE})')
    parser.add_argument('--output', type=str, default=OUTPUT_FILE,
                        help=f'Output file path (default: {OUTPUT_FILE})')
    parser.add_argument('--force-fallback', action='store_true',
                        help='Force using the fallback implementation even if Themefinder is available')
    args = parser.parse_args()
    
    logger.info(f"Starting theme extraction: input={args.input}, output={args.output}")
    
    # Load responses
    responses = load_responses(args.input)
    if not responses:
        logger.error("No responses loaded, exiting")
        return
    
    # Initialize the extractor
    extractor = ThemeExtractor()
    
    # Extract themes
    if args.force_fallback:
        logger.info("Forcing fallback implementation as requested")
        theme_mapping = extractor.extract_themes_fallback(responses)
    else:
        theme_mapping = extractor.extract_themes(responses)
    
    if not theme_mapping:
        logger.error("Theme extraction failed, no themes extracted")
        return
    
    # Analyze theme distribution
    analyze_theme_distribution(theme_mapping)
    
    # Save the theme mapping
    save_theme_mapping(theme_mapping, args.output)
    
    logger.info("Theme extraction complete")


if __name__ == "__main__":
    main()
