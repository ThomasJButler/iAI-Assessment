#!/usr/bin/env python3
"""
Theme Comparison Script for i.AI Assessment

This script compares two sets of theme mappings and quantifies their variation.
It generates a summary paragraph for both technical and non-technical stakeholders.

Author: AI Evaluation Engineer
Date: 31/03/2025
"""

import os
import json
import logging
import argparse
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Tuple, Set
from collections import Counter
import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("theme_comparison.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
MAPPING_1_FILE = "data/theme_mapping_1.json"
MAPPING_2_FILE = "data/theme_mapping_2.json"
OUTPUT_FILE = "data/comparison_results.json"
SUMMARY_FILE = "summary.md"
VISUALIZATIONS_DIR = "data/visualizations"


class ThemeComparator:
    """Class to compare two sets of theme mappings."""

    def __init__(self, mapping1: List[List], mapping2: List[List]):
        """
        Initialize the ThemeComparator with two theme mappings.

        Args:
            mapping1: First theme mapping as a list of [response, themes] pairs
            mapping2: Second theme mapping as a list of [response, themes] pairs
        """
        self.mapping1 = mapping1
        self.mapping2 = mapping2
        self.all_themes = self._get_all_themes()
        logger.info(f"Initialized ThemeComparator with {len(mapping1)} responses and {len(self.all_themes)} unique themes")

    def _get_all_themes(self) -> Set[str]:
        """
        Extract all unique themes from both mappings.

        Returns:
            Set of all unique themes
        """
        all_themes = set()
        for _, themes in self.mapping1:
            all_themes.update(themes)
        for _, themes in self.mapping2:
            all_themes.update(themes)
        return all_themes

    def calculate_jaccard_similarities(self) -> List[float]:
        """
        Calculate Jaccard similarity for each response.

        Returns:
            List of Jaccard similarity scores
        """
        similarities = []
        
        for i in range(len(self.mapping1)):
            _, themes1 = self.mapping1[i]
            _, themes2 = self.mapping2[i]
            
            # Calculate Jaccard similarity
            set1 = set(themes1)
            set2 = set(themes2)
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            
            similarity = intersection / union if union > 0 else 1.0
            similarities.append(similarity)
        
        return similarities

    def calculate_theme_distributions(self) -> Tuple[Dict[str, int], Dict[str, int]]:
        """
        Calculate theme distributions for both mappings.

        Returns:
            Tuple of (distribution1, distribution2) as dictionaries
        """
        distribution1 = Counter()
        distribution2 = Counter()
        
        for _, themes in self.mapping1:
            distribution1.update(themes)
        
        for _, themes in self.mapping2:
            distribution2.update(themes)
        
        return distribution1, distribution2

    def calculate_response_agreement(self) -> float:
        """
        Calculate the percentage of responses with identical theme mappings.

        Returns:
            Percentage of identical mappings
        """
        identical_count = 0
        
        for i in range(len(self.mapping1)):
            _, themes1 = self.mapping1[i]
            _, themes2 = self.mapping2[i]
            
            if set(themes1) == set(themes2):
                identical_count += 1
        
        return (identical_count / len(self.mapping1)) * 100

    def calculate_theme_changes(self) -> Dict[str, int]:
        """
        Calculate the number of theme additions, removals, and replacements.

        Returns:
            Dictionary of change counts
        """
        changes = {"additions": 0, "removals": 0, "replacements": 0}
        
        for i in range(len(self.mapping1)):
            _, themes1 = self.mapping1[i]
            _, themes2 = self.mapping2[i]
            
            set1 = set(themes1)
            set2 = set(themes2)
            
            # Count additions and removals
            changes["additions"] += len(set2 - set1)
            changes["removals"] += len(set1 - set2)
            
            # Count replacements (approximation)
            intersection = len(set1 & set2)
            min_length = min(len(themes1), len(themes2))
            changes["replacements"] += min_length - intersection
        
        return changes

    def calculate_cohen_kappa(self) -> Dict[str, float]:
        """
        Calculate Cohen's Kappa for each theme.

        Returns:
            Dictionary mapping theme to kappa score
        """
        kappa_scores = {}
        
        # For each theme, create binary arrays indicating presence/absence
        for theme in self.all_themes:
            y1 = []
            y2 = []
            
            for i in range(len(self.mapping1)):
                _, themes1 = self.mapping1[i]
                _, themes2 = self.mapping2[i]
                
                y1.append(1 if theme in themes1 else 0)
                y2.append(1 if theme in themes2 else 0)
            
            # Calculate Cohen's Kappa
            try:
                kappa = cohen_kappa_score(y1, y2)
                kappa_scores[theme] = kappa
            except Exception as e:
                logger.warning(f"Could not calculate kappa for {theme}: {str(e)}")
                kappa_scores[theme] = 0.0
        
        return kappa_scores

    def generate_visualizations(self, output_dir: str) -> None:
        """
        Generate visualizations of the comparison results.

        Args:
            output_dir: Directory to save visualizations
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Jaccard similarity distribution
        jaccard_scores = self.calculate_jaccard_similarities()
        plt.figure(figsize=(10, 6))
        plt.hist(jaccard_scores, bins=20, alpha=0.7, color='blue')
        plt.title('Distribution of Jaccard Similarity Scores')
        plt.xlabel('Jaccard Similarity')
        plt.ylabel('Number of Responses')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, 'jaccard_distribution.png'))
        plt.close()
        
        # 2. Theme frequency comparison
        dist1, dist2 = self.calculate_theme_distributions()
        themes = sorted(self.all_themes)
        counts1 = [dist1.get(theme, 0) for theme in themes]
        counts2 = [dist2.get(theme, 0) for theme in themes]
        
        plt.figure(figsize=(12, 8))
        x = np.arange(len(themes))
        width = 0.35
        plt.bar(x - width/2, counts1, width, label='Mapping 1')
        plt.bar(x + width/2, counts2, width, label='Mapping 2')
        plt.xlabel('Themes')
        plt.ylabel('Frequency')
        plt.title('Theme Frequency Comparison')
        plt.xticks(x, themes, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'theme_frequency.png'))
        plt.close()
        
        # 3. Cohen's Kappa heatmap
        kappa_scores = self.calculate_cohen_kappa()
        themes = sorted(kappa_scores.keys())
        scores = [kappa_scores[theme] for theme in themes]
        
        plt.figure(figsize=(12, 6))
        plt.bar(themes, scores, color='green', alpha=0.7)
        plt.title("Cohen's Kappa by Theme")
        plt.xlabel('Theme')
        plt.ylabel("Cohen's Kappa")
        plt.axhline(y=0.4, color='r', linestyle='--', label='Fair Agreement (0.4)')
        plt.axhline(y=0.6, color='g', linestyle='--', label='Moderate Agreement (0.6)')
        plt.axhline(y=0.8, color='b', linestyle='--', label='Strong Agreement (0.8)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'cohen_kappa.png'))
        plt.close()
        
        logger.info(f"Saved visualizations to {output_dir}")

    def generate_summary(self) -> str:
        """
        Generate a summary paragraph describing the variation between mappings.

        Returns:
            Summary paragraph
        """
        # Calculate metrics
        jaccard_scores = self.calculate_jaccard_similarities()
        avg_jaccard = np.mean(jaccard_scores)
        agreement_percentage = self.calculate_response_agreement()
        theme_changes = self.calculate_theme_changes()
        total_changes = sum(theme_changes.values())
        avg_changes_per_response = total_changes / len(self.mapping1)
        
        # Calculate Cohen's Kappa
        kappa_scores = self.calculate_cohen_kappa()
        avg_kappa = np.mean(list(kappa_scores.values()))
        
        # Generate summary paragraph
        summary = (
            f"# Theme Mapping Comparison Summary\n\n"
            f"The comparison between Themefinder-generated themes and human-coded themes reveals "
            f"a moderate level of agreement, with an average Jaccard similarity of {avg_jaccard:.2f} "
            f"across all {len(self.mapping1)} consultation responses. "
            f"Exactly {agreement_percentage:.1f}% of responses received identical theme mappings in both sets. "
            f"The analysis identified a total of {total_changes} theme differences, averaging {avg_changes_per_response:.2f} "
            f"changes per response, which included {theme_changes['additions']} additions, {theme_changes['removals']} "
            f"removals, and approximately {theme_changes['replacements']} theme replacements. "
            f"Cohen's Kappa coefficient, which measures inter-rater reliability while accounting for chance agreement, "
            f"averaged {avg_kappa:.2f} across all themes, indicating {'substantial' if avg_kappa > 0.6 else 'moderate' if avg_kappa > 0.4 else 'fair'} "
            f"agreement between the two mapping approaches. "
            f"The variation observed suggests that while automated theme extraction captures many of the same patterns "
            f"as human coding, there remain meaningful differences in thematic interpretation that may warrant "
            f"consideration when implementing fully automated consultation analysis systems."
        )
        
        return summary

    def generate_detailed_results(self) -> Dict[str, Any]:
        """
        Generate detailed comparison results.

        Returns:
            Dictionary of comparison results
        """
        # Calculate all metrics
        jaccard_scores = self.calculate_jaccard_similarities()
        dist1, dist2 = self.calculate_theme_distributions()
        agreement_percentage = self.calculate_response_agreement()
        theme_changes = self.calculate_theme_changes()
        kappa_scores = self.calculate_cohen_kappa()
        
        # Compile results
        results = {
            "jaccard_similarity": {
                "mean": np.mean(jaccard_scores),
                "median": np.median(jaccard_scores),
                "std_dev": np.std(jaccard_scores),
                "min": min(jaccard_scores),
                "max": max(jaccard_scores),
                "scores": jaccard_scores
            },
            "theme_distribution": {
                "mapping1": {theme: count for theme, count in dist1.items()},
                "mapping2": {theme: count for theme, count in dist2.items()}
            },
            "response_agreement": {
                "percentage": agreement_percentage,
                "count": int(agreement_percentage * len(self.mapping1) / 100)
            },
            "theme_changes": theme_changes,
            "cohen_kappa": {
                "mean": np.mean(list(kappa_scores.values())),
                "scores": kappa_scores
            }
        }
        
        return results


def load_theme_mapping(file_path: str) -> List[List]:
    """
    Load theme mapping from a JSON file.

    Args:
        file_path: Path to the theme mapping file

    Returns:
        Theme mapping as a list of [response, themes] pairs
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        logger.info(f"Loaded theme mapping with {len(mapping)} responses from {file_path}")
        return mapping
    except Exception as e:
        logger.error(f"Error loading theme mapping from {file_path}: {str(e)}")
        return []


def save_results(results: Dict[str, Any], output_file: str) -> None:
    """
    Save comparison results to a JSON file.

    Args:
        results: Dictionary of comparison results
        output_file: Path to the output file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved comparison results to {output_file}")
    except Exception as e:
        logger.error(f"Error saving comparison results to {output_file}: {str(e)}")


def save_summary(summary: str, output_file: str) -> None:
    """
    Save summary paragraph to a file.

    Args:
        summary: Summary paragraph
        output_file: Path to the output file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        logger.info(f"Saved summary to {output_file}")
    except Exception as e:
        logger.error(f"Error saving summary to {output_file}: {str(e)}")


def main():
    """Main function to compare theme mappings."""
    parser = argparse.ArgumentParser(description='Compare theme mappings')
    parser.add_argument('--mapping1', type=str, default=MAPPING_1_FILE,
                        help=f'Path to first theme mapping (default: {MAPPING_1_FILE})')
    parser.add_argument('--mapping2', type=str, default=MAPPING_2_FILE,
                        help=f'Path to second theme mapping (default: {MAPPING_2_FILE})')
    parser.add_argument('--output', type=str, default=OUTPUT_FILE,
                        help=f'Path to output results file (default: {OUTPUT_FILE})')
    parser.add_argument('--summary', type=str, default=SUMMARY_FILE,
                        help=f'Path to output summary file (default: {SUMMARY_FILE})')
    parser.add_argument('--visualizations', type=str, default=VISUALIZATIONS_DIR,
                        help=f'Directory for visualizations (default: {VISUALIZATIONS_DIR})')
    args = parser.parse_args()
    
    logger.info(f"Starting theme comparison: mapping1={args.mapping1}, mapping2={args.mapping2}")
    
    # Load theme mappings
    mapping1 = load_theme_mapping(args.mapping1)
    mapping2 = load_theme_mapping(args.mapping2)
    
    if not mapping1 or not mapping2:
        logger.error("Failed to load theme mappings, exiting")
        return
    
    if len(mapping1) != len(mapping2):
        logger.error(f"Mapping sizes don't match: {len(mapping1)} vs {len(mapping2)}")
        return
    
    # Initialize comparator
    comparator = ThemeComparator(mapping1, mapping2)
    
    # Generate visualizations
    comparator.generate_visualizations(args.visualizations)
    
    # Generate detailed results
    results = comparator.generate_detailed_results()
    save_results(results, args.output)
    
    # Generate summary
    summary = comparator.generate_summary()
    save_summary(summary, args.summary)
    
    logger.info("Theme comparison complete")


if __name__ == "__main__":
    main()
