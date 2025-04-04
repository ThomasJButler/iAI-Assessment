# Fast Batch Generation for i.AI Assessment

This document explains how to quickly generate the 300 synthetic consultation responses in batches to avoid hitting API rate limits.

## Background

The OpenAI API has rate limits that prevent generating all 300 responses at once. The `generate_in_batches.py` script helps work around these limits by:

1. Generating responses in larger batches (25 responses per batch by default)
2. Waiting briefly between batches (15 seconds by default)
3. Combining all batches into a single file
4. Removing any duplicate responses

## Usage

### Basic Usage

To generate 300 responses with the default settings:

```bash
python3 generate_in_batches.py
```

This will:
- Generate 12 batches of 25 responses each
- Wait 15 seconds between batches
- Save the combined responses to `data/synthetic_responses.json`

### Custom Settings

You can customize the batch size, total count, and wait time:

```bash
python3 generate_in_batches.py --total 100 --batch-size 5 --wait-time 60
```

This will:
- Generate 100 responses in batches of 5
- Wait 60 seconds between batches

### Output

The script saves:
- Individual batch files in `data/temp/batch_*.json`
- Combined responses in `data/synthetic_responses.json`
- Logs in `batch_generation.log`

## Handling Interruptions

If the script is interrupted (e.g., by pressing Ctrl+C), you can restart it later. It will:
- Skip to the next batch if interrupted during generation
- Continue with the next batch if interrupted during the wait period
- Combine all successfully generated batches at the end

## Running the Pipeline

After generating the responses, you can run the rest of the pipeline:

```bash
python3 scripts/theme_extraction.py --input data/synthetic_responses.json --output data/theme_mapping_1.json
python3 scripts/theme_variation.py --input data/theme_mapping_1.json --output data/theme_mapping_2.json --variation 0.3
python3 scripts/theme_comparison.py --mapping1 data/theme_mapping_1.json --mapping2 data/theme_mapping_2.json --output data/comparison_results.json --summary summary.md
```

Or use the pipeline script:

```bash
python3 run_pipeline.py --skip-generation
```

## Tips

- The script should complete in approximately 10-15 minutes with the default settings
- If you encounter rate limit errors, you can increase the wait time (e.g., `--wait-time 30`)
- If you need to stop it, press Ctrl+C and it will try to gracefully exit
- You can resume by running the script again, and it will combine any batches that were already generated
- For maximum speed, we've set the temperature to 1.0 and reduced retry delays
