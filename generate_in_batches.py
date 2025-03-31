#!/usr/bin/env python3
"""
Script to generate responses in smaller batches and combine them.

This script generates synthetic consultation responses in smaller batches
to avoid hitting API rate limits, and then combines them into a single file.

Author: Thomas J Butler
Date: 31/03/2025
"""

import os
import json
import time
import argparse
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("batch_generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_TOTAL_RESPONSES = 300
DEFAULT_BATCH_SIZE = 25  # Larger batch size for faster generation
DEFAULT_WAIT_TIME = 15   # 15 seconds between batches for faster generation
OUTPUT_FILE = "data/synthetic_responses.json"
TEMP_DIR = "data/temp"


def ensure_directories() -> None:
    """Ensure that required directories exist."""
    os.makedirs("data", exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)


def run_command(command: list) -> bool:
    """
    Run a command and log the output.

    Args:
        command: Command to run as a list of strings

    Returns:
        True if the command completed successfully, False otherwise
    """
    logger.info(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True
        )
        logger.info(f"Command completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        return False


def generate_batch(batch_number: int, batch_size: int) -> bool:
    """
    Generate a batch of responses.

    Args:
        batch_number: Batch number (for logging and filename)
        batch_size: Number of responses to generate in this batch

    Returns:
        True if the batch was generated successfully, False otherwise
    """
    output_file = os.path.join(TEMP_DIR, f"batch_{batch_number}.json")
    
    logger.info(f"Generating batch {batch_number} with {batch_size} responses")
    
    return run_command([
        "python3", 
        "scripts/data_generation.py",
        "--count", str(batch_size),
        "--output", output_file
    ])


def remove_duplicates(responses: list) -> list:
    """
    Remove duplicate responses from the list.

    Args:
        responses: List of responses that may contain duplicates

    Returns:
        Deduplicated list of responses
    """
    unique_responses = []
    seen = set()
    
    for response in responses:
        # Normalize the response for comparison (lowercase, strip whitespace)
        normalized = response.lower().strip()
        
        if normalized not in seen:
            seen.add(normalized)
            unique_responses.append(response)
    
    logger.info(f"Removed {len(responses) - len(unique_responses)} duplicate responses")
    return unique_responses


def combine_batches(total_count: int) -> bool:
    """
    Combine all generated batches into a single file.

    Args:
        total_count: Total number of responses to include

    Returns:
        True if the batches were combined successfully, False otherwise
    """
    logger.info(f"Combining batches into {OUTPUT_FILE}")
    
    # Get all batch files
    try:
        batch_files = sorted([
            os.path.join(TEMP_DIR, f) 
            for f in os.listdir(TEMP_DIR) 
            if f.startswith("batch_") and f.endswith(".json")
        ])
    except Exception as e:
        logger.error(f"Failed to list batch files: {str(e)}")
        return False
    
    if not batch_files:
        logger.error("No batch files found to combine")
        return False
    
    # Combine all responses
    all_responses = []
    for batch_file in batch_files:
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                responses = json.load(f)
                logger.info(f"Loaded {len(responses)} responses from {batch_file}")
                all_responses.extend(responses)
        except Exception as e:
            logger.error(f"Failed to load {batch_file}: {str(e)}")
            logger.info("Skipping this batch and continuing...")
            continue
    
    if not all_responses:
        logger.error("No responses loaded from any batch")
        return False
    
    # Remove duplicates
    unique_responses = remove_duplicates(all_responses)
    
    # Check if we have enough responses
    if len(unique_responses) < total_count:
        logger.warning(f"Only have {len(unique_responses)} unique responses, requested {total_count}")
    
    # Trim to requested count if needed
    if len(unique_responses) > total_count:
        logger.info(f"Trimming from {len(unique_responses)} to {total_count} responses")
        unique_responses = unique_responses[:total_count]
    
    # Save combined responses
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(unique_responses, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(unique_responses)} responses to {OUTPUT_FILE}")
        return True
    except Exception as e:
        logger.error(f"Failed to save combined responses: {str(e)}")
        return False


def main() -> None:
    """Main function to parse arguments and run the batch generation."""
    global OUTPUT_FILE
    
    parser = argparse.ArgumentParser(description='Generate responses in batches')
    parser.add_argument('--total', type=int, default=DEFAULT_TOTAL_RESPONSES,
                        help=f'Total number of responses to generate (default: {DEFAULT_TOTAL_RESPONSES})')
    parser.add_argument('--batch-size', type=int, default=DEFAULT_BATCH_SIZE,
                        help=f'Number of responses per batch (default: {DEFAULT_BATCH_SIZE})')
    parser.add_argument('--wait-time', type=int, default=DEFAULT_WAIT_TIME,
                        help=f'Wait time between batches in seconds (default: {DEFAULT_WAIT_TIME})')
    parser.add_argument('--output', type=str, default=OUTPUT_FILE,
                        help=f'Output file path (default: {OUTPUT_FILE})')
    args = parser.parse_args()
    
    # Update output file
    OUTPUT_FILE = args.output
    
    # Ensure directories exist
    ensure_directories()
    
    # Calculate number of batches
    total_responses = args.total
    batch_size = args.batch_size
    wait_time = args.wait_time
    
    batches_needed = (total_responses + batch_size - 1) // batch_size
    
    logger.info(f"Starting batch generation: total={total_responses}, batch_size={batch_size}, wait_time={wait_time}s")
    logger.info(f"Will generate {batches_needed} batches")
    
    # Generate batches
    for i in range(batches_needed):
        # Calculate batch size (might be smaller for the last batch)
        current_batch_size = min(batch_size, total_responses - i * batch_size)
        
        # Generate batch
        success = False
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                if generate_batch(i + 1, current_batch_size):
                    success = True
                    break
                else:
                    logger.warning(f"Failed to generate batch {i + 1}, attempt {attempt + 1}/{max_attempts}")
                    time.sleep(5)  # Short delay before retry
            except KeyboardInterrupt:
                logger.warning("Keyboard interrupt detected, skipping to next batch")
                break
        
        if not success:
            logger.error(f"Failed to generate batch {i + 1} after {max_attempts} attempts")
            logger.info("Continuing with next batch...")
        
        # Wait between batches (except after the last batch)
        if i < batches_needed - 1:
            logger.info(f"Waiting {wait_time} seconds before next batch...")
            try:
                time.sleep(wait_time)
            except KeyboardInterrupt:
                logger.warning("Keyboard interrupt detected during wait, continuing with next batch")
    
    # Combine batches
    if not combine_batches(total_count=total_responses):
        logger.error("Failed to combine batches")
        exit(1)
    
    logger.info("Batch generation complete")


if __name__ == "__main__":
    main()
