# i.AI Assessment: Theme Mapping Analysis

This repository contains the solution for the AI Evaluation Engineer Technical Task for i.AI. The task involves generating synthetic consultation responses, extracting themes using Themefinder, creating a second set of theme mappings with controlled randomness, and comparing the two sets of theme mappings.

## Project Structure

```
project/
├── data/                          # Data directory
│   ├── synthetic_responses.json   # Generated consultation responses
│   ├── theme_mapping_1.json       # First set of theme mappings
│   ├── theme_mapping_2.json       # Second set of theme mappings
│   ├── comparison_results.json    # Detailed comparison results
│   ├── visualizations/            # Visualizations of the comparison
│   ├── sample_responses.json      # Sample consultation responses
│   ├── sample_theme_mapping_1.json # Sample first theme mapping
│   ├── sample_theme_mapping_2.json # Sample second theme mapping
│   ├── sample_comparison_results.json # Sample comparison results
│   └── theme_descriptions.md      # Descriptions of theme meanings
├── scripts/                       # Python scripts
│   ├── data_generation.py         # Script to generate synthetic responses
│   ├── theme_extraction.py        # Script to extract themes using Themefinder
│   ├── theme_variation.py         # Script to create a second set of theme mappings
│   ├── theme_comparison.py        # Script to compare the two sets of theme mappings
│   ├── utils.py                   # Utility functions
│   └── test_utils.py              # Tests for utility functions
├── docs/                          # Documentation
│   ├── themefinder_usage.md       # Guide for using Themefinder
│   └── metrics_explanation.md     # Explanation of comparison metrics
├── summary.md                     # Summary paragraph of the comparison
├── plan.md                        # Working plan for the assessment
├── run_pipeline.sh                # Shell script to run the complete pipeline
├── run_pipeline.py                # Python script to run the complete pipeline
└── README.md                      # This file
```

## Requirements

- Python 3.9+
- Required packages:
  - openai
  - numpy
  - matplotlib
  - pandas
  - scikit-learn
  - themefinder (if available)

## Installation

1. Clone the repository
2. Install the required packages:

```bash
pip install openai numpy matplotlib pandas scikit-learn
pip install themefinder  # Optional, fallback implementation provided
```

## Usage

### 1. Generate Synthetic Data

Generate 300 synthetic consultation responses:

```bash
python scripts/data_generation.py --count 300 --output data/synthetic_responses.json
```

### 2. Generate Themes

Extract themes from the synthetic responses using Themefinder (or fallback implementation):

```bash
python scripts/theme_extraction.py --input data/synthetic_responses.json --output data/theme_mapping_1.json
```

To force the fallback implementation even if Themefinder is available:

```bash
python scripts/theme_extraction.py --force-fallback
```

### 3. Create a Second Theme Mapping

Create a second set of theme mappings with controlled randomness:

```bash
python scripts/theme_variation.py --input data/theme_mapping_1.json --output data/theme_mapping_2.json --variation 0.3
```

The `--variation` parameter controls the degree of randomness (0.0 to 1.0).

### 4. Compare Theme Mappings

Compare the two sets of theme mappings and generate a summary:

```bash
python scripts/theme_comparison.py --mapping1 data/theme_mapping_1.json --mapping2 data/theme_mapping_2.json --output data/comparison_results.json --summary summary.md
```

### Running the Complete Pipeline

You can run the complete pipeline using either the shell script or Python script:

#### Using the Shell Script

```bash
./run_pipeline.sh
```

#### Using the Python Script

```bash
python run_pipeline.py --count 300 --variation 0.3
```

Both scripts will:
1. Generate synthetic consultation responses
2. Extract themes using Themefinder (or fallback)
3. Create a second theme mapping with controlled randomness
4. Compare the two theme mappings and generate a summary

## Documentation

Additional documentation is available in the `docs` directory:

- `docs/themefinder_usage.md`: Guide for using the Themefinder API
- `docs/metrics_explanation.md`: Explanation of the metrics used in theme comparison

## Sample Data

Sample data files are provided in the `data` directory:

- `data/sample_responses.json`: Sample consultation responses
- `data/sample_theme_mapping_1.json`: Sample first theme mapping
- `data/sample_theme_mapping_2.json`: Sample second theme mapping
- `data/sample_comparison_results.json`: Sample comparison results
- `data/theme_descriptions.md`: Descriptions of what each theme represents

## AI Assistance

This project was developed with AI assistance. The following AI tools were used:

- Azure OpenAI API (GPT-4o) for generating synthetic consultation responses
- AI assistance for code development and documentation

## Author

AI Evaluation Engineer  
Date: 31/03/2025
