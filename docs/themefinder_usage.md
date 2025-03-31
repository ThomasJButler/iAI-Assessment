# Themefinder Usage Guide

This document provides guidance on how to use the Themefinder API for theme extraction from consultation responses.

## Installation

Install the Themefinder package from PyPI:

```bash
pip install themefinder
```

## Basic Usage

```python
import themefinder

# Initialize the ThemeFinder
finder = themefinder.ThemeFinder()

# Extract themes from a single response
response = "I'd like to see more focus on practical skills in the curriculum."
themes = finder.extract_themes(response)
print(themes)  # Example output: ['Theme F', 'Theme E']

# Process multiple responses
responses = [
    "I'd like to see more focus on practical skills in the curriculum.",
    "The education system should prioritize smaller class sizes."
]
results = finder.process_responses(responses)
```

## Configuration Options

Themefinder can be configured with various options:

```python
# Configure with custom options
finder = themefinder.ThemeFinder(
    min_themes_per_response=1,
    max_themes_per_response=5,
    theme_prefix="Theme ",
    similarity_threshold=0.75
)
```

## Processing Large Datasets

For large datasets, use batch processing to manage memory and API rate limits:

```python
import json

# Load responses from a JSON file
with open("responses.json", "r") as f:
    responses = json.load(f)

# Process in batches
batch_size = 50
results = []

for i in range(0, len(responses), batch_size):
    batch = responses[i:i+batch_size]
    batch_results = finder.process_responses(batch)
    results.extend(batch_results)
    print(f"Processed {i+len(batch)}/{len(responses)} responses")

# Save results
with open("theme_mapping.json", "w") as f:
    json.dump(results, f, indent=2)
```

## Error Handling

Implement robust error handling to manage API failures:

```python
try:
    themes = finder.extract_themes(response)
except themefinder.ThemeFinderError as e:
    print(f"Theme extraction failed: {e}")
    # Implement fallback strategy
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log error and continue
```

## Fallback Implementation

If Themefinder is unavailable or fails, you can use the fallback implementation provided in `theme_extraction.py`:

```python
from theme_extraction import ThemeExtractor

# Initialize the extractor
extractor = ThemeExtractor()

# Use the fallback implementation
results = extractor.extract_themes_fallback(responses)
```

## Output Format

Themefinder returns theme mappings in the following format:

```json
[
  [
    "Response text here",
    ["Theme A", "Theme F", "Theme I"]
  ],
  [
    "Another response text",
    ["Theme B", "Theme E"]
  ]
]
```

## Performance Considerations

- Themefinder processes approximately 10 responses per second
- For large datasets (>1000 responses), consider parallel processing
- Cache results to avoid redundant API calls for identical responses

## Support

For issues with Themefinder, contact the i.AI support team or refer to the official documentation.
