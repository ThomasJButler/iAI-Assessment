
#!/usr/bin/env python3
"""
Pipeline Runner for i.AI Assessment

This script runs the complete pipeline for the i.AI Assessment:
1. Generate synthetic consultation responses
2. Extract themes using Themefinder (or fallback)
3. Create a second theme mapping with controlled randomness
4. Compare the two theme mappings and generate a summary

Author: AI Evaluation Engineer
Date: 31/03/2025
"""

import os
import argparse
import subprocess
import logging
import time
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_RESPONSE_COUNT = 300
DEFAULT_VARIATION_LEVEL = 0.3
DATA_DIR = "data"
SCRIPTS_DIR = "scripts"
VISUALIZATIONS_DIR = os.path.join(DATA_DIR, "visualizations")


def ensure_directories() -> None:
    """Ensure that required directories exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)


def run_command(command: List[str], description: str) -> Optional[str]:
    """
    Run a command and log the output.

    Args:
        command: Command to run as a list of strings
        description: Description of the command for logging

    Returns:
        Command output if successful, None otherwise
    """
    logger.info(f"Running: {' '.join(command)}")
    logger.info(f"Step: {description}")
    
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True
        )
        logger.info(f"Command completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        return None


def run_pipeline(response_count: int, variation_level: float) -> bool:
    """
    Run the complete pipeline.

    Args:
        response_count: Number of synthetic responses to generate
        variation_level: Level of variation for the second theme mapping

    Returns:
        True if the pipeline completed successfully, False otherwise
    """
    # Ensure directories exist
    ensure_directories()
    
    # Print header
    logger.info("=" * 40)
    logger.info("i.AI Assessment Pipeline")
    logger.info("=" * 40)
    logger.info(f"Running complete pipeline with:")
    logger.info(f"- Response count: {response_count}")
    logger.info(f"- Variation level: {variation_level}")
    logger.info("=" * 40)
    
    # Step 1: Generate synthetic data
    logger.info("Step 1: Generating synthetic consultation responses...")
    if run_command([
        "python3", 
        os.path.join(SCRIPTS_DIR, "data_generation.py"),
        "--count", str(response_count),
        "--output", os.path.join(DATA_DIR, "synthetic_responses.json")
    ], "Generate synthetic data") is None:
        return False
    logger.info("✓ Synthetic data generation complete")
    
    # Step 2: Extract themes
    logger.info("Step 2: Extracting themes using Themefinder (or fallback)...")
    if run_command([
        "python3",
        os.path.join(SCRIPTS_DIR, "theme_extraction.py"),
        "--input", os.path.join(DATA_DIR, "synthetic_responses.json"),
        "--output", os.path.join(DATA_DIR, "theme_mapping_1.json")
    ], "Extract themes") is None:
        return False
    logger.info("✓ Theme extraction complete")
    
    # Step 3: Create second theme mapping
    logger.info(f"Step 3: Creating second theme mapping with variation level {variation_level}...")
    if run_command([
        "python3",
        os.path.join(SCRIPTS_DIR, "theme_variation.py"),
        "--input", os.path.join(DATA_DIR, "theme_mapping_1.json"),
        "--output", os.path.join(DATA_DIR, "theme_mapping_2.json"),
        "--variation", str(variation_level)
    ], "Create second theme mapping") is None:
        return False
    logger.info("✓ Second theme mapping created")
    
    # Step 4: Compare theme mappings
    logger.info("Step 4: Comparing theme mappings and generating summary...")
    if run_command([
        "python3",
        os.path.join(SCRIPTS_DIR, "theme_comparison.py"),
        "--mapping1", os.path.join(DATA_DIR, "theme_mapping_1.json"),
        "--mapping2", os.path.join(DATA_DIR, "theme_mapping_2.json"),
        "--output", os.path.join(DATA_DIR, "comparison_results.json"),
        "--summary", "summary.md",
        "--visualizations", VISUALIZATIONS_DIR
    ], "Compare theme mappings") is None:
        return False
    logger.info("✓ Theme comparison complete")
    
    # Print completion message
    logger.info("=" * 40)
    logger.info("Pipeline completed successfully!")
    logger.info("=" * 40)
    logger.info("Outputs:")
    logger.info(f"- Synthetic responses: {os.path.join(DATA_DIR, 'synthetic_responses.json')}")
    logger.info(f"- Theme mapping 1: {os.path.join(DATA_DIR, 'theme_mapping_1.json')}")
    logger.info(f"- Theme mapping 2: {os.path.join(DATA_DIR, 'theme_mapping_2.json')}")
    logger.info(f"- Comparison results: {os.path.join(DATA_DIR, 'comparison_results.json')}")
    logger.info(f"- Summary: summary.md")
    logger.info(f"- Visualizations: {VISUALIZATIONS_DIR}")
    logger.info("=" * 40)
    
    return True


def main() -> None:
    """Main function to parse arguments and run the pipeline."""
    parser = argparse.ArgumentParser(description='Run the complete i.AI Assessment pipeline')
    parser.add_argument('--count', type=int, default=DEFAULT_RESPONSE_COUNT,
                        help=f'Number of synthetic responses to generate (default: {DEFAULT_RESPONSE_COUNT})')
    parser.add_argument('--variation', type=float, default=DEFAULT_VARIATION_LEVEL,
                        help=f'Variation level for the second theme mapping (default: {DEFAULT_VARIATION_LEVEL})')
    args = parser.parse_args()
    
    # Record start time
    start_time = time.time()
    
    # Run the pipeline
    success = run_pipeline(args.count, args.variation)
    
    # Record end time and calculate duration
    end_time = time.time()
    duration = end_time - start_time
    
    if success:
        logger.info(f"Pipeline completed in {duration:.2f} seconds")
    else:
        logger.error(f"Pipeline failed after {duration:.2f} seconds")
        exit(1)


if __name__ == "__main__":
    main()
