# Theme Comparison Metrics Explanation

This document explains the metrics used to compare theme mappings in the i.AI Assessment.

## Jaccard Similarity

Jaccard similarity measures the overlap between two sets by dividing the size of the intersection by the size of the union.

### Formula
```
J(A, B) = |A ∩ B| / |A ∪ B|
```

Where:
- A and B are sets of themes
- |A ∩ B| is the number of themes common to both sets
- |A ∪ B| is the total number of unique themes in both sets

### Interpretation
- **Range**: 0.0 to 1.0
- **0.0**: No overlap between theme sets (completely different)
- **1.0**: Perfect overlap (identical theme sets)
- **Example**: If response 1 has themes [A, B, C] and response 2 has themes [A, B, D], the Jaccard similarity is 2/4 = 0.5

### Usage in Theme Comparison
We calculate Jaccard similarity for each response's theme sets across the two mappings, then aggregate these scores to get overall similarity metrics:
- Mean Jaccard similarity
- Median Jaccard similarity
- Standard deviation
- Minimum and maximum values

## Response Agreement

Response agreement measures the percentage of responses that received identical theme mappings in both sets.

### Formula
```
Agreement = (Number of responses with identical theme sets / Total number of responses) * 100
```

### Interpretation
- **Range**: 0% to 100%
- **0%**: No responses have identical theme mappings
- **100%**: All responses have identical theme mappings
- **Example**: If 30 out of 300 responses have identical theme mappings, the agreement is 10%

## Theme Changes

Theme changes quantify the specific differences between the two mappings:

### Additions
The number of themes present in the second mapping but not in the first.

### Removals
The number of themes present in the first mapping but not in the second.

### Replacements
An approximation of themes that were replaced with different ones, calculated as:
```
min(|themes1|, |themes2|) - |themes1 ∩ themes2|
```

## Cohen's Kappa

Cohen's Kappa measures inter-rater reliability while accounting for agreement by chance.

### Formula
```
κ = (po - pe) / (1 - pe)
```

Where:
- po is the observed agreement
- pe is the expected agreement by chance

### Interpretation
- **Range**: -1.0 to 1.0
- **< 0**: Less agreement than expected by chance
- **0.01-0.20**: Slight agreement
- **0.21-0.40**: Fair agreement
- **0.41-0.60**: Moderate agreement
- **0.61-0.80**: Substantial agreement
- **0.81-1.00**: Almost perfect agreement

### Usage in Theme Comparison
We calculate Cohen's Kappa for each theme individually, treating it as a binary classification problem (theme present or absent). This helps identify which themes have the highest and lowest agreement between the two mappings.

## Theme Distribution

Theme distribution compares the frequency of each theme across both mappings.

### Interpretation
- Similar distributions indicate consistent theme usage
- Large differences in theme frequencies suggest systematic biases or different interpretations
- **Example**: If Theme A appears 150 times in mapping 1 but only 75 times in mapping 2, this suggests a significant difference in how this theme is applied

## Visualization

The comparison results include several visualizations:

### Jaccard Distribution
A histogram showing the distribution of Jaccard similarity scores across all responses.

### Theme Frequency Comparison
A bar chart comparing the frequency of each theme in both mappings.

### Cohen's Kappa by Theme
A bar chart showing the Cohen's Kappa score for each theme, indicating which themes have the highest and lowest agreement.

## Practical Significance

When interpreting these metrics, consider:

1. **Context**: What level of agreement is acceptable depends on the subjectivity of the themes and the intended use of the analysis.

2. **Patterns**: Look for patterns in disagreements. Are certain themes consistently misaligned?

3. **Impact**: Consider how differences might impact downstream analysis or decision-making.

4. **Improvement**: Use the metrics to identify areas where theme definitions or extraction methods could be improved.
