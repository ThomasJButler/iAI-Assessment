#!/usr/bin/env python3
"""
Data Generation Script for i.AI Assessment

This script generates synthetic consultation responses using Azure OpenAI API.
It creates 300 diverse responses to the question:
"What changes would you like to see in the education system in your area over the next five years?"

Author: AI Evaluation Engineer
Date: 31/03/2025
"""

import os
import json
import time
import random
import logging
from typing import List, Dict, Any, Optional
import argparse
import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Azure OpenAI API configuration
AZURE_OPENAI_ENDPOINT = "https://iai-azoai-interview.openai.azure.com/"
AZURE_OPENAI_API_KEY = "6FrJnxZWsBwkXOpFtb16DmpS5ULgoodO1m3A0DpDIj6Q9PmhnwKCJQQJ99BCACi0881XJ3w3AAABACOGqhml"
OPENAI_API_VERSION = "2024-08-01-preview"
DEPLOYMENT_NAME = "gpt-4o"

# Constants
CONSULTATION_QUESTION = "What changes would you like to see in the education system in your area over the next five years?"
TOTAL_RESPONSES = 300
OUTPUT_FILE = "data/synthetic_responses.json"
BATCH_SIZE = 25  # Increased batch size for faster generation
MAX_RETRIES = 3  # Reduced max retries for faster completion
INITIAL_RETRY_DELAY = 1  # seconds - minimal initial delay
MAX_RETRY_DELAY = 10  # Maximum delay between retries (seconds) - reduced max delay
BATCH_DELAY = 1  # seconds between batches - minimal delay


class ResponseGenerator:
    """Class to generate synthetic consultation responses using Azure OpenAI API."""

    def __init__(self, endpoint: str, api_key: str, api_version: str, deployment_name: str):
        """
        Initialize the ResponseGenerator with Azure OpenAI credentials.

        Args:
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            api_version: OpenAI API version
            deployment_name: Model deployment name
        """
        self.client = openai.AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.deployment_name = deployment_name
        logger.info("Initialized ResponseGenerator with Azure OpenAI client")

    def generate_batch(self, batch_size: int, perspective: Optional[str] = None,
                      length: Optional[str] = None, focus: Optional[str] = None) -> List[str]:
        """
        Generate a batch of responses with specified characteristics.

        Args:
            batch_size: Number of responses to generate
            perspective: Optional perspective to generate from (e.g., 'parent', 'teacher')
            length: Optional length constraint ('short', 'medium', 'long')
            focus: Optional topic focus (e.g., 'curriculum', 'technology')

        Returns:
            List of generated responses
        """
        # Build the prompt based on parameters
        system_prompt = "You are generating synthetic consultation responses to a public education survey. Generate diverse, realistic responses that reflect a wide range of opinions, backgrounds, and priorities."
        
        user_prompt = f"Generate {batch_size} diverse, realistic responses to the following consultation question:\n\n"
        user_prompt += f'"{CONSULTATION_QUESTION}"\n\n'
        
        if perspective:
            user_prompt += f"Generate responses from the perspective of {perspective}s. "
        
        if length:
            if length == "short":
                user_prompt += "Keep responses brief (1-2 sentences). "
            elif length == "medium":
                user_prompt += "Make responses moderately detailed (3-5 sentences). "
            elif length == "long":
                user_prompt += "Create detailed responses with multiple paragraphs. "
        
        if focus:
            user_prompt += f"Focus responses on aspects related to {focus}. "
        
        user_prompt += "\nEnsure responses are diverse, realistic, and reflect a range of opinions. "
        user_prompt += "Make sure each response is unique and different from the others. "
        user_prompt += "Format the output as a JSON array of strings, with each string being a separate response."

        # Call the API with exponential backoff retry logic
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=1.0,  # Maximum temperature for maximum diversity
                    max_tokens=4000,
                    response_format={"type": "json_object"}
                )
                
                # Extract and parse the responses
                content = response.choices[0].message.content
                try:
                    response_data = json.loads(content)
                    if "responses" in response_data:
                        return response_data["responses"]
                    else:
                        # Try to find an array in the response
                        for key, value in response_data.items():
                            if isinstance(value, list) and all(isinstance(item, str) for item in value):
                                return value
                        
                        # If we can't find a suitable array, log an error
                        logger.error(f"Unexpected response format: {content}")
                        return []
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse JSON response: {content}")
                    return []
                
            except openai.RateLimitError as e:
                # Handle rate limit errors with exponential backoff
                if attempt < MAX_RETRIES - 1:
                    # Calculate exponential backoff delay with jitter
                    delay = min(MAX_RETRY_DELAY, INITIAL_RETRY_DELAY * (2 ** attempt))
                    # Add random jitter (±20%)
                    jitter = random.uniform(0.8, 1.2)
                    delay = delay * jitter
                    
                    logger.warning(f"Rate limit exceeded (attempt {attempt+1}/{MAX_RETRIES}). Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("Max retries exceeded for rate limit. Returning empty list.")
                    return []
            except Exception as e:
                logger.error(f"API call failed (attempt {attempt+1}/{MAX_RETRIES}): {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    # Use shorter delays for other errors
                    delay = INITIAL_RETRY_DELAY * (1.5 ** attempt)
                    logger.info(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("Max retries exceeded. Returning empty list.")
                    return []
        
        return []  # Fallback if all retries fail

    def generate_responses(self, total_count: int) -> List[str]:
        """
        Generate the specified number of diverse responses.

        Args:
            total_count: Total number of responses to generate

        Returns:
            List of generated responses
        """
        all_responses = []
        batches_needed = (total_count + BATCH_SIZE - 1) // BATCH_SIZE
        
        # Define diversity parameters
        perspectives = ['parent', 'teacher', 'student', 'community member', 'education professional']
        lengths = ['short', 'medium', 'long']
        focuses = [
            'curriculum', 'technology', 'teaching methods', 'facilities', 
            'inclusivity', 'assessment', 'extracurricular activities',
            'teacher support', 'parent involvement', 'funding'
        ]
        
        logger.info(f"Generating {total_count} responses in {batches_needed} batches")
        
        for i in range(batches_needed):
            # Determine batch size (might be smaller for the last batch)
            current_batch_size = min(BATCH_SIZE, total_count - len(all_responses))
            
            # Randomly select parameters for diversity
            perspective = random.choice(perspectives) if random.random() > 0.3 else None
            length = random.choice(lengths) if random.random() > 0.3 else None
            focus = random.choice(focuses) if random.random() > 0.3 else None
            
            logger.info(f"Batch {i+1}/{batches_needed}: Generating {current_batch_size} responses " +
                       f"(perspective={perspective}, length={length}, focus={focus})")
            
            # Generate the batch
            batch_responses = self.generate_batch(
                current_batch_size, perspective, length, focus
            )
            
            # Add to our collection
            all_responses.extend(batch_responses)
            
            # Log progress
            logger.info(f"Progress: {len(all_responses)}/{total_count} responses generated")
            
            # Add a delay between batches to avoid rate limiting
            if i < batches_needed - 1:
                delay = BATCH_DELAY + random.uniform(-1, 1)  # Add some jitter
                logger.info(f"Waiting {delay:.1f} seconds before next batch to avoid rate limits...")
                time.sleep(delay)
        
        return all_responses[:total_count]  # Ensure we return exactly the requested number

    def remove_duplicates(self, responses: List[str]) -> List[str]:
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


def save_responses(responses: List[str], output_file: str) -> None:
    """
    Save the generated responses to a JSON file.

    Args:
        responses: List of generated responses
        output_file: Path to the output file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(responses, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(responses)} responses to {output_file}")


def main():
    """Main function to generate and save synthetic responses."""
    parser = argparse.ArgumentParser(description='Generate synthetic consultation responses')
    parser.add_argument('--count', type=int, default=TOTAL_RESPONSES,
                        help=f'Number of responses to generate (default: {TOTAL_RESPONSES})')
    parser.add_argument('--output', type=str, default=OUTPUT_FILE,
                        help=f'Output file path (default: {OUTPUT_FILE})')
    parser.add_argument('--use-sample', action='store_true',
                        help='Use sample data instead of generating new data')
    parser.add_argument('--sample-file', type=str, default="data/sample_responses.json",
                        help='Path to sample responses file (default: data/sample_responses.json)')
    args = parser.parse_args()
    
    logger.info(f"Output file: {args.output}")
    
    # Check if we should use sample data
    if args.use_sample:
        logger.info(f"Using sample data from {args.sample_file}")
        try:
            with open(args.sample_file, 'r', encoding='utf-8') as f:
                responses = json.load(f)
            logger.info(f"Loaded {len(responses)} sample responses")
            
            # Trim to requested count if needed
            if len(responses) > args.count:
                responses = responses[:args.count]
                logger.info(f"Trimmed to {args.count} responses")
        except Exception as e:
            logger.error(f"Failed to load sample data: {str(e)}")
            return
    else:
        logger.info(f"Starting response generation: target={args.count}")
        
        try:
            # Initialize the generator
            generator = ResponseGenerator(
                AZURE_OPENAI_ENDPOINT,
                AZURE_OPENAI_API_KEY,
                OPENAI_API_VERSION,
                DEPLOYMENT_NAME
            )
            
            # Generate responses
            responses = generator.generate_responses(args.count)
        except ImportError:
            logger.error("Failed to import openai module. Please install it with 'pip install openai' or use --use-sample")
            return
        except Exception as e:
            logger.error(f"Failed to generate responses: {str(e)}")
            logger.info("Try using --use-sample to use sample data instead")
            return
    
    # Process responses
    if args.use_sample:
        # For sample data, just ensure we have the right count
        unique_responses = responses[:args.count]
    else:
        # For generated data, remove duplicates and generate more if needed
        unique_responses = generator.remove_duplicates(responses)
        
        # If we lost too many to deduplication, generate more to compensate
        if len(unique_responses) < args.count:
            additional_needed = args.count - len(unique_responses)
            logger.info(f"Generating {additional_needed} additional responses to replace duplicates")
            
            additional_responses = generator.generate_responses(additional_needed)
            additional_unique = generator.remove_duplicates(additional_responses)
            
            unique_responses.extend(additional_unique)
            unique_responses = unique_responses[:args.count]  # Ensure we don't exceed the requested count
    
    # Save the responses
    save_responses(unique_responses, args.output)
    
    logger.info("Response generation complete")


if __name__ == "__main__":
    main()
