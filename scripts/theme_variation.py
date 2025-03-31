#!/usr/bin/env python3
"""
Theme Variation Script for i.AI Assessment

This script creates a second set of theme mappings that randomly differs from the first.
The degree of randomisation is configurable.

Author: AI Evaluation Engineer
Date: 31/03/2025
"""

import os
import json
import logging
import argparse
import random
from typing import List, Dict, Any, Tuple, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("theme_variation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
INPUT_FILE = "data/theme_mapping_1.json"
OUTPUT_FILE = "data/theme_mapping_2.json"
DEFAULT_VARIATION_LEVEL = 0.3  # Default level of variation (0.0 to 1.0)


class ThemeVariationGenerator:
    """Class to generate variations of theme mappings."""

    def __init__(self, variation_level: float = DEFAULT_VARIATION_LEVEL):
        """
        Initialize the ThemeVariationGenerator.

        Args:
            variation_level: Level of variation to apply (0.0 to 1.0)
        """
        self.variation_level = max(0.0, min(1.0, variation_level))  # Clamp between 0 and 1
        logger.info(f"Initialized ThemeVariationGenerator with variation level: {self.variation_level}")

    def get_all_themes(self, theme_mapping: List[List]) -> Set[str]:
        """
        Extract all unique themes from the theme mapping.

        Args:
            theme_mapping: List of [response, themes] pairs

        Returns:
            Set of all unique themes
        """
        all_themes = set()
        for _, themes in theme_mapping:
            all_themes.update(themes)
        return all_themes

    def create_variation(self, theme_mapping: List[List]) -> List[List]:
        """
        Create a variation of the theme mapping with controlled randomness.

        Args:
            theme_mapping: Original theme mapping as a list of [response, themes] pairs

        Returns:
            Varied theme mapping as a list of [response, themes] pairs
        """
        logger.info(f"Creating theme mapping variation with level {self.variation_level}")
        
        # Extract all unique themes
        all_themes = list(self.get_all_themes(theme_mapping))
        logger.info(f"Found {len(all_themes)} unique themes in the original mapping")
        
        # Create a new mapping with variations
        varied_mapping = []
        
        for response, themes in theme_mapping:
            # Start with the original themes
            new_themes = themes.copy()
            
            # Apply variations based on the variation level
            self._apply_theme_removal(new_themes)
            self._apply_theme_addition(new_themes, all_themes)
            self._apply_theme_replacement(new_themes, all_themes)
            
            # Add to the varied mapping
            varied_mapping.append([response, new_themes])
        
        logger.info(f"Created varied theme mapping for {len(varied_mapping)} responses")
        return varied_mapping

    def _apply_theme_removal(self, themes: List[str]) -> None:
        """
        Randomly remove themes based on the variation level.

        Args:
            themes: List of themes to modify (in-place)
        """
        if not themes:
            return
        
        # Calculate how many themes to potentially remove
        # We don't want to remove all themes, so limit to len(themes) - 1
        max_removals = max(0, len(themes) - 1)
        
        # For each theme, there's a chance to remove it based on variation level
        themes_to_remove = []
        for theme in themes:
            if random.random() < self.variation_level and len(themes) - len(themes_to_remove) > 1:
                themes_to_remove.append(theme)
        
        # Remove the selected themes
        for theme in themes_to_remove:
            themes.remove(theme)

    def _apply_theme_addition(self, themes: List[str], all_themes: List[str]) -> None:
        """
        Randomly add new themes based on the variation level.

        Args:
            themes: List of themes to modify (in-place)
            all_themes: List of all available themes
        """
        # Calculate how many themes to potentially add
        # We want to keep a reasonable number of themes per response
        max_additions = max(0, 5 - len(themes))  # Limit to 5 themes total
        
        # For each potential addition, there's a chance to add it based on variation level
        for _ in range(max_additions):
            if random.random() < self.variation_level:
                # Select a theme that's not already in the list
                available_themes = [t for t in all_themes if t not in themes]
                if available_themes:
                    new_theme = random.choice(available_themes)
                    themes.append(new_theme)

    def _apply_theme_replacement(self, themes: List[str], all_themes: List[str]) -> None:
        """
        Randomly replace themes based on the variation level.

        Args:
            themes: List of themes to modify (in-place)
            all_themes: List of all available themes
        """
        if not themes:
            return
        
        # For each theme, there's a chance to replace it based on variation level
        for i, theme in enumerate(themes):
            if random.random() < self.variation_level:
                # Select a theme that's not already in the list
                available_themes = [t for t in all_themes if t not in themes]
                if available_themes:
                    new_theme = random.choice(available_themes)
                    themes[i] = new_theme


def load_theme_mapping(input_file: str) -> List[List]:
    """
    Load theme mapping from a JSON file.

    Args:
        input_file: Path to the input file

    Returns:
        Theme mapping as a list of [response, themes] pairs
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            theme_mapping = json.load(f)
        
        logger.info(f"Loaded theme mapping for {len(theme_mapping)} responses from {input_file}")
        return theme_mapping
    except Exception as e:
        logger.error(f"Error loading theme mapping from {input_file}: {str(e)}")
        return []


def save_theme_mapping(theme_mapping: List[List], output_file: str) -> None:
    """
    Save the theme mapping to a JSON file.

    Args:
        theme_mapping: Theme mapping as a list of [response, themes] pairs
        output_file: Path to the output file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(theme_mapping, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved varied theme mapping for {len(theme_mapping)} responses to {output_file}")
    except Exception as e:
        logger.error(f"Error saving varied theme mapping to {output_file}: {str(e)}")


def analyze_variation(original_mapping: List[List], varied_mapping: List[List]) -> Dict[str, float]:
    """
    Analyze and log the variation between the original and varied theme mappings.

    Args:
        original_mapping: Original theme mapping
        varied_mapping: Varied theme mapping

    Returns:
        Dictionary of variation metrics
    """
    # Initialize counters
    total_responses = len(original_mapping)
    identical_responses = 0
    total_jaccard = 0.0
    theme_changes = {"additions": 0, "removals": 0, "replacements": 0}
    
    # Compare each response
    for i in range(total_responses):
        original_response, original_themes = original_mapping[i]
        varied_response, varied_themes = varied_mapping[i]
        
        # Check if the response is the same
        assert original_response == varied_response, "Response mismatch in mappings"
        
        # Check if the themes are identical
        if set(original_themes) == set(varied_themes):
            identical_responses += 1
        
        # Calculate Jaccard similarity
        intersection = len(set(original_themes) & set(varied_themes))
        union = len(set(original_themes) | set(varied_themes))
        jaccard = intersection / union if union > 0 else 1.0
        total_jaccard += jaccard
        
        # Count theme changes
        theme_changes["additions"] += len(set(varied_themes) - set(original_themes))
        theme_changes["removals"] += len(set(original_themes) - set(varied_themes))
        
        # Count replacements (this is an approximation)
        min_length = min(len(original_themes), len(varied_themes))
        potential_replacements = min_length - intersection
        theme_changes["replacements"] += potential_replacements
    
    # Calculate metrics
    metrics = {
        "identical_percentage": (identical_responses / total_responses) * 100,
        "average_jaccard": total_jaccard / total_responses,
        "average_additions": theme_changes["additions"] / total_responses,
        "average_removals": theme_changes["removals"] / total_responses,
        "average_replacements": theme_changes["replacements"] / total_responses,
        "total_changes": sum(theme_changes.values())
    }
    
    # Log the results
    logger.info(f"Variation analysis:")
    logger.info(f"  Identical responses: {identical_responses}/{total_responses} ({metrics['identical_percentage']:.1f}%)")
    logger.info(f"  Average Jaccard similarity: {metrics['average_jaccard']:.3f}")
    logger.info(f"  Average theme additions per response: {metrics['average_additions']:.2f}")
    logger.info(f"  Average theme removals per response: {metrics['average_removals']:.2f}")
    logger.info(f"  Average theme replacements per response: {metrics['average_replacements']:.2f}")
    logger.info(f"  Total theme changes: {metrics['total_changes']}")
    
    return metrics


def main():
    """Main function to create a varied theme mapping."""
    parser = argparse.ArgumentParser(description='Create a varied theme mapping')
    parser.add_argument('--input', type=str, default=INPUT_FILE,
                        help=f'Input file path (default: {INPUT_FILE})')
    parser.add_argument('--output', type=str, default=OUTPUT_FILE,
                        help=f'Output file path (default: {OUTPUT_FILE})')
    parser.add_argument('--variation', type=float, default=DEFAULT_VARIATION_LEVEL,
                        help=f'Variation level from 0.0 to 1.0 (default: {DEFAULT_VARIATION_LEVEL})')
    args = parser.parse_args()
    
    logger.info(f"Starting theme variation: input={args.input}, output={args.output}, variation={args.variation}")
    
    # Load the original theme mapping
    original_mapping = load_theme_mapping(args.input)
    if not original_mapping:
        logger.error("No theme mapping loaded, exiting")
        return
    
    # Create the variation
    generator = ThemeVariationGenerator(args.variation)
    varied_mapping = generator.create_variation(original_mapping)
    
    # Analyze the variation
    analyze_variation(original_mapping, varied_mapping)
    
    # Save the varied mapping
    save_theme_mapping(varied_mapping, args.output)
    
    logger.info("Theme variation complete")


if __name__ == "__main__":
    main()
