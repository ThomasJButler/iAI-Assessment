#!/bin/bash
# Run the complete i.AI Assessment pipeline
# Author: AI Evaluation Engineer
# Date: 31/03/2025

# Set up error handling
set -e  # Exit on error
set -u  # Treat unset variables as errors

# Configuration
RESPONSE_COUNT=300
VARIATION_LEVEL=0.3
DATA_DIR="data"
SCRIPTS_DIR="scripts"
VISUALIZATIONS_DIR="$DATA_DIR/visualizations"

# Create directories if they don't exist
mkdir -p "$DATA_DIR"
mkdir -p "$VISUALIZATIONS_DIR"

# Print header
echo "========================================"
echo "i.AI Assessment Pipeline"
echo "========================================"
echo "Running complete pipeline with:"
echo "- Response count: $RESPONSE_COUNT"
echo "- Variation level: $VARIATION_LEVEL"
echo "========================================"

# Step 1: Generate synthetic data
echo ""
echo "Step 1: Generating synthetic consultation responses..."
python "$SCRIPTS_DIR/data_generation.py" --count "$RESPONSE_COUNT" --output "$DATA_DIR/synthetic_responses.json" --use-sample
echo "✓ Synthetic data generation complete"

# Step 2: Extract themes
echo ""
echo "Step 2: Extracting themes using Themefinder (or fallback)..."
python "$SCRIPTS_DIR/theme_extraction.py" --input "$DATA_DIR/synthetic_responses.json" --output "$DATA_DIR/theme_mapping_1.json"
echo "✓ Theme extraction complete"

# Step 3: Create second theme mapping
echo ""
echo "Step 3: Creating second theme mapping with variation level $VARIATION_LEVEL..."
python "$SCRIPTS_DIR/theme_variation.py" --input "$DATA_DIR/theme_mapping_1.json" --output "$DATA_DIR/theme_mapping_2.json" --variation "$VARIATION_LEVEL"
echo "✓ Second theme mapping created"

# Step 4: Compare theme mappings
echo ""
echo "Step 4: Comparing theme mappings and generating summary..."
python "$SCRIPTS_DIR/theme_comparison.py" --mapping1 "$DATA_DIR/theme_mapping_1.json" --mapping2 "$DATA_DIR/theme_mapping_2.json" --output "$DATA_DIR/comparison_results.json" --summary "summary.md" --visualizations "$VISUALIZATIONS_DIR"
echo "✓ Theme comparison complete"

# Print completion message
echo ""
echo "========================================"
echo "Pipeline completed successfully!"
echo "========================================"
echo "Outputs:"
echo "- Synthetic responses: $DATA_DIR/synthetic_responses.json"
echo "- Theme mapping 1: $DATA_DIR/theme_mapping_1.json"
echo "- Theme mapping 2: $DATA_DIR/theme_mapping_2.json"
echo "- Comparison results: $DATA_DIR/comparison_results.json"
echo "- Summary: summary.md"
echo "- Visualizations: $VISUALIZATIONS_DIR"
echo "========================================"
