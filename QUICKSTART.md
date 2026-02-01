# Quick Start Guide

## Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd "Data Analysis Agent"

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Automated EDA (Quickest Way)

```python
from src.eda_agent import EDAAgent
from src.utils import load_sample_data

# Load data
df = load_sample_data('titanic')

# Create agent and run automated analysis
agent = EDAAgent(df)
results = agent.run_automated_eda()
print(results['summary_report'])
```

### Step-by-Step Analysis

```python
import pandas as pd
from src.eda_agent import EDAAgent

# Load your data
df = pd.read_csv('your_data.csv')

# Initialize agent
agent = EDAAgent(df, name="My Analysis")

# Run individual analyses
agent.analyze_missing_values()
agent.analyze_distributions()
agent.analyze_correlations()
agent.detect_outliers()

# Get suggestions
suggestions = agent.suggest_next_steps()
for s in suggestions:
    print(f"→ {s}")
```

### Using Schema Compression

```python
from src.schema_compressor import SchemaCompressor
import pandas as pd

df = pd.read_csv('data.csv')
compressor = SchemaCompressor()

# Compress schema
schema = compressor.compress(df)

# Display in text format
print(compressor.to_text(schema))

# Estimate token savings
stats = compressor.estimate_token_reduction(df)
print(f"Token reduction: {stats['reduction_ratio']:.1f}x")
```

### Using History Compression

```python
from src.history_compressor import HistoryCompressor

history = HistoryCompressor()

# Add analysis steps
history.add_step(
    action="visualization",
    description="Plotted distributions",
    insights=["Age is right-skewed", "Fare has outliers"]
)

# Get compressed context
context = history.get_context_for_next_step()
print(context)

# Estimate savings
stats = history.estimate_token_savings()
print(f"Compression: {stats['compression_ratio']:.1f}x")
```

## Running the Demo Notebook

```bash
# Start Jupyter
jupyter notebook

# Navigate to:
examples/demo_analysis.ipynb
```

## Example Outputs

### Compressed Schema
```
=== DATASET SCHEMA ===
Shape: 200 rows × 10 columns
Memory: 0.15 MB

[Age]
  Type: numeric (float64)
  Missing: 20.0%
  Range: [0.50, 80.00]
  Mean ± Std: 29.50 ± 14.25
```

### Compressed History
```
Recent: missing_value_analysis: Found 2 columns with missing 
→ distribution_analysis: Age is right-skewed 
→ correlation_analysis: Strong correlation between Pclass and Fare

Key findings: 20% missing in Age; Fare is right-skewed; 
Strong negative correlation between Pclass and Fare
```

## Next Steps

1. Try with your own data
2. Explore the demo notebook
3. Integrate with your LLM workflow
4. Customize compression parameters

## Troubleshooting

**Import Error:**
```bash
# Make sure you're in the project directory
cd "Data Analysis Agent"
pip install -r requirements.txt
```

**Jupyter Kernel Issues:**
```bash
python -m ipykernel install --user --name=venv
```

## Support

- 📖 See README.md for full documentation
- 🐛 Report issues on GitHub
- 💬 Ask questions in Discussions
