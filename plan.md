# i.AI Assessment Working Plan

## Project Overview

This document outlines the working plan for the AI Evaluation Engineer Technical Task for i.AI. The task involves analysing and evaluating synthetic consultation data using Themefinder, a topic modelling tool that identifies key themes and maps responses to these themes.

## Task Summary

The assessment consists of four main tasks:

1. **Generate Synthetic Data**: Create 300 plausible responses to a public consultation question about education system changes
2. **Generate Themes**: Use Themefinder to extract themes from the synthetic responses
3. **Create a Second Theme Mapping**: Develop a variant of the original theme mapping with controlled randomness
4. **Compare Theme Mappings**: Analyse and quantify the variation between the two sets of theme mappings

## Detailed Approach

### 1. Generate Synthetic Data

**Objective**: Create 300 diverse, realistic responses to the question: "What changes would you like to see in the education system in your area over the next five years?"

**Methodology**:
- Utilise Azure OpenAI API (GPT-4o) to generate responses
- Implement a structured approach to ensure diversity in:
  - Response length (short, medium, long)
  - Topic focus (curriculum, resources, teaching methods, etc.)
  - Perspective (parents, teachers, students, community members)
  - Complexity and specificity of suggestions

**Implementation Steps**:
1. Set up Azure OpenAI client using provided credentials
2. Design prompt engineering strategy to elicit diverse responses
3. Implement batched generation to manage API rate limits
4. Apply post-processing to ensure quality and remove duplicates
5. Save responses in JSON format for reproducibility

**Output**:
- `synthetic_responses.json`: JSON file containing all 300 responses
- `data_generation.py`: Python script used to generate the data

### 2. Generate Themes with Themefinder

**Objective**: Extract themes from the synthetic responses using Themefinder or implement a fallback solution if needed.

**Methodology**:
- Install and configure Themefinder from PyPI
- Process the synthetic responses through Themefinder
- If Themefinder fails, implement a fallback solution using NLP techniques

**Primary Implementation (Themefinder)**:
1. Install Themefinder package
2. Configure Themefinder with appropriate parameters
3. Process synthetic responses through Themefinder
4. Extract and format theme mappings

**Fallback Implementation (if needed)**:
1. Implement text preprocessing (tokenization, stopword removal, lemmatization)
2. Apply topic modelling techniques (e.g., LDA, NMF)
3. Extract key themes based on topic modelling results
4. Assign themes to responses using similarity measures
5. Format output to match Themefinder's expected structure

**Output**:
- `theme_mapping_1.json`: JSON file containing the first set of theme mappings
- `theme_extraction.py`: Python script for theme extraction

### 3. Create a Second Theme Mapping

**Objective**: Generate a second set of theme mappings that differs from the first in a controlled, quantifiable manner.

**Methodology**:
- Develop an algorithm that introduces controlled randomness to the original theme mappings
- Implement a configurable parameter to adjust the degree of variation

**Implementation Steps**:
1. Load the original theme mappings
2. Define a randomisation function with the following operations:
   - Add new themes to responses (with configurable probability)
   - Remove existing themes from responses (with configurable probability)
   - Replace themes with different ones (with configurable probability)
3. Apply the randomisation function to create the second mapping
4. Ensure the randomisation level is configurable via a single parameter
5. Save the second mapping in the same format as the first

**Output**:
- `theme_mapping_2.json`: JSON file containing the second set of theme mappings
- `theme_variation.py`: Python script for creating the second mapping

### 4. Compare Theme Mappings

**Objective**: Analyse and quantify the variation between the two sets of theme mappings, producing a summary for both technical and non-technical stakeholders.

**Methodology**:
- Implement multiple quantitative metrics to measure the differences
- Create visualisations to illustrate the variations
- Write a clear summary paragraph explaining the findings

**Metrics Implementation**:
1. **Jaccard Similarity Index**:
   - Calculate theme overlap for each response
   - Aggregate to get overall similarity score
   
2. **Theme Distribution Analysis**:
   - Compare frequency of each theme across both mappings
   - Measure statistical significance of differences
   
3. **Response-Level Agreement**:
   - Calculate percentage of responses with identical theme mappings
   - Analyse patterns in disagreements

4. **Weighted Cohen's Kappa**:
   - Measure inter-rater reliability between the two mappings
   - Account for chance agreement

**Visualisation**:
- Create bar charts comparing theme frequencies
- Generate heatmaps showing theme co-occurrence patterns
- Plot distribution of Jaccard similarity scores

**Summary Development**:
- Craft a concise paragraph explaining the variation
- Include key metrics in accessible language
- Ensure clarity for both technical and non-technical readers

**Output**:
- `theme_comparison.py`: Python script for analysis
- `comparison_results.json`: Detailed metrics and results
- `summary.md`: Summary paragraph and key findings

## Implementation Details

### Code Structure

```
project/
├── data/
│   ├── synthetic_responses.json
│   ├── theme_mapping_1.json
│   ├── theme_mapping_2.json
│   └── comparison_results.json
├── scripts/
│   ├── data_generation.py
│   ├── theme_extraction.py
│   ├── theme_variation.py
│   ├── theme_comparison.py
│   └── utils.py
├── summary.md
└── README.md
```

### Coding Standards

- **Language**: Python 3.9+
- **Style**: PEP 8 compliant
- **Documentation**: Comprehensive docstrings (Google style)
- **Type Hints**: Used throughout for better code clarity
- **Error Handling**: Robust exception handling with informative messages
- **Logging**: Detailed logging for reproducibility
- **Testing**: Unit tests for core functions

### Dependencies

- **Azure OpenAI**: For generating synthetic responses
- **Themefinder**: For theme extraction (primary method)
- **NLTK/spaCy**: For text processing (fallback method)
- **scikit-learn**: For topic modelling (fallback method)
- **pandas**: For data manipulation
- **matplotlib/seaborn**: For visualisations
- **numpy**: For numerical operations

## Task Execution Timeline

1. **Task 1** (Generate Synthetic Data):
   - Set up environment and dependencies
   - Implement data generation script
   - Generate and validate synthetic responses

2. **Task 2** (Generate Themes):
   - Install and configure Themefinder
   - Process responses through Themefinder
   - Implement fallback solution if needed
   - Generate first theme mapping

3. **Task 3** (Create Second Mapping):
   - Develop randomisation algorithm
   - Implement configurable variation parameter
   - Generate second theme mapping
   - Validate mapping format

4. **Task 4** (Compare Mappings):
   - Implement comparison metrics
   - Create visualisations
   - Write summary paragraph
   - Compile final results

## Deliverables

1. **Dataset**:
   - Synthetic responses (JSON)
   - Two theme mappings (JSON)

2. **Code**:
   - Python scripts for each task
   - Utility functions and helpers

3. **Summary**:
   - Analysis of theme variation
   - Quantitative metrics
   - Visualisations

## AI Assistance Documentation

Throughout this project, AI assistance will be used in the following ways:

1. **Prompt Engineering**: Designing effective prompts for generating diverse synthetic responses
2. **Code Development**: Assistance with implementing complex algorithms
3. **Error Debugging**: Help with troubleshooting issues
4. **Documentation**: Assistance with creating clear documentation

All AI-assisted components will be clearly documented in the code comments and final submission.

---

This plan provides a structured approach to completing the i.AI Assessment task, ensuring reproducibility, clarity, and adherence to best practices in AI evaluation engineering.
