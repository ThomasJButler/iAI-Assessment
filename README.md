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

### Option 1: Direct Installation

1. Clone the repository
2. Install the required packages:

```bash
pip3 install openai numpy matplotlib pandas scikit-learn
pip3 install themefinder  # Optional, fallback implementation provided
```

### Option 2: Virtual Environment

1. Clone the repository
2. Create and activate a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install -r requirements.txt
```

3. To deactivate the virtual environment when done:

```bash
deactivate
```

4. To activate it again later:

```bash
source venv/bin/activate
```

### Option 3: Conda Environment (Recommended)

1. Clone the repository
2. Create and activate a conda environment:

#### Method A: Using environment.yml (Simplest)

```bash
# Create conda environment from the environment.yml file
conda env create -f environment.yml

# Activate the environment
conda activate iai-assessment
```

#### Method B: Manual Setup

```bash
# Create a new conda environment with Python 3.9
conda create -n iai-assessment python=3.9

# Activate the environment
conda activate iai-assessment

# Install core dependencies using conda
conda install -c conda-forge numpy pandas matplotlib scikit-learn

# Install remaining dependencies using pip
pip install openai pytest black flake8 mypy

# Try to install themefinder (may not be available)
pip install themefinder
```

3. To deactivate the conda environment when done:

```bash
conda deactivate
```

4. To activate it again later:

```bash
conda activate iai-assessment
```

## Usage

### 1. Generate Synthetic Data

Generate 300 synthetic consultation responses:

```bash
python3 scripts/data_generation.py --count 300 --output data/synthetic_responses.json
```

#### Handling API Rate Limits

If you encounter rate limit errors with the OpenAI API, you can use the batch generation script:

```bash
python3 generate_in_batches.py
```

This script generates responses in small batches with delays between batches to avoid rate limits. See [BATCH_GENERATION_README.md](BATCH_GENERATION_README.md) for details.

### 2. Generate Themes

Extract themes from the synthetic responses using Themefinder (or fallback implementation):

```bash
python3 scripts/theme_extraction.py --input data/synthetic_responses.json --output data/theme_mapping_1.json
```

To force the fallback implementation even if Themefinder is available:

```bash
python3 scripts/theme_extraction.py --force-fallback
```

### 3. Create a Second Theme Mapping

Create a second set of theme mappings with controlled randomness:

```bash
python3 scripts/theme_variation.py --input data/theme_mapping_1.json --output data/theme_mapping_2.json --variation 0.3
```

The `--variation` parameter controls the degree of randomness (0.0 to 1.0).

### 4. Compare Theme Mappings

Compare the two sets of theme mappings and generate a summary:

```bash
python3 scripts/theme_comparison.py --mapping1 data/theme_mapping_1.json --mapping2 data/theme_mapping_2.json --output data/comparison_results.json --summary summary.md
```

### Running the Complete Pipeline

You can run the complete pipeline using either the shell script or Python script:

#### Using the Shell Script

```bash
./run_pipeline.sh
```

#### Using the Python Script

```bash
python3 run_pipeline.py --count 300 --variation 0.3
```

Both scripts will:
1. Generate synthetic consultation responses (using sample data by default to avoid OpenAI API issues)
2. Extract themes using Themefinder (or fallback)
3. Create a second theme mapping with controlled randomness
4. Compare the two theme mappings and generate a summary

**Note**: The pipeline is configured to use sample data by default to avoid OpenAI API rate limits and dependency issues. If you want to generate new data, you'll need to modify the scripts to remove the `--use-sample` flag and ensure the openai package is installed.

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

- Azure OpenAI API (GPT-4o) for generating synthetic consultation responses.
- AI assistance for code development and documentation, ChatGPT 4.0 (custom prompting GPT), Perplexity MCP, Claude 3.7, Cline for Agentic AI capabilities inside VS code.

## Author

Thomas James Butler 
Date: 31/03/2025
