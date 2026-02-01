# 🎯 Getting Started with Data Analysis Agent

Welcome! This guide will help you set up and start using the Data Analysis Agent.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 100 MB free disk space

## 🚀 Installation

### Option 1: Automated Setup (Recommended)

#### Linux/Mac:
```bash
./setup.sh
```

#### Windows:
```batch
setup.bat
```

This will:
1. Create a virtual environment
2. Install all dependencies
3. Run tests to verify setup

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test installation
python test_modules.py
```

## 🎓 Your First Analysis

### Method 1: Using the Demo Notebook (Best for Learning)

```bash
# Activate virtual environment
source venv/bin/activate

# Start Jupyter
jupyter notebook examples/demo_analysis.ipynb
```

The notebook includes:
- Complete walkthrough
- Sample datasets
- Visualizations
- Token efficiency metrics

### Method 2: Command Line (Quick)

```bash
# Activate virtual environment
source venv/bin/activate

# Analyze a sample dataset
python cli.py sample titanic

# Or analyze your own CSV
python cli.py analyze your_data.csv --auto
```

### Method 3: Python Script (For Integration)

Create a file `my_analysis.py`:

```python
from src.eda_agent import EDAAgent
from src.utils import load_sample_data
import pandas as pd

# Load data (or use your own: pd.read_csv('file.csv'))
df = load_sample_data('titanic')

# Create agent
agent = EDAAgent(df, name="My Analysis")

# Run automated analysis
results = agent.run_automated_eda()

# Print report
print(results['summary_report'])
```

Run it:
```bash
python my_analysis.py
```

## 📊 Key Features & Usage

### 1. Schema Compression

```python
from src.schema_compressor import SchemaCompressor
import pandas as pd

df = pd.read_csv('data.csv')
compressor = SchemaCompressor()

# Compress schema
schema = compressor.compress(df)
print(compressor.to_text(schema))

# See token savings
stats = compressor.estimate_token_reduction(df)
print(f"Reduction: {stats['reduction_ratio']:.1f}x")
```

**Output:**
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

### 2. History Compression

```python
from src.history_compressor import HistoryCompressor

history = HistoryCompressor()

# Add analysis steps
history.add_step(
    action="visualization",
    description="Created distribution plots",
    insights=["Age is right-skewed", "Fare has outliers"]
)

# Get compressed context (for LLM)
context = history.get_context_for_next_step()
print(f"Context tokens: ~{len(context) // 4}")
```

### 3. EDA Agent

```python
from src.eda_agent import EDAAgent

agent = EDAAgent(df)

# Run specific analyses
agent.analyze_missing_values()
agent.analyze_distributions()
agent.analyze_correlations()
agent.detect_outliers()

# Get suggestions for next steps
for suggestion in agent.suggest_next_steps():
    print(f"→ {suggestion}")

# Generate report
print(agent.generate_summary_report())
```

## 🔧 CLI Commands

```bash
# Analyze CSV file
python cli.py analyze data.csv

# Automated analysis with report output
python cli.py analyze data.csv --auto --output report.txt

# Analyze sample dataset
python cli.py sample iris
python cli.py sample titanic
python cli.py sample tips

# Compress schema only
python cli.py schema data.csv --output schema.txt
```

## 📚 Available Sample Datasets

- `iris` - Classic Iris flower dataset (150 rows, 5 columns)
- `titanic` - Titanic survival data (200 rows, 10 columns)
- `tips` - Restaurant tips data (150 rows, 7 columns)
- `random` - Randomly generated data (100 rows, 8 columns)

## 💡 Common Use Cases

### Use Case 1: Quick Data Exploration

```python
from src.eda_agent import EDAAgent
import pandas as pd

df = pd.read_csv('new_dataset.csv')
agent = EDAAgent(df)
results = agent.run_automated_eda()
print(results['summary_report'])
```

### Use Case 2: LLM Integration

```python
from src.schema_compressor import SchemaCompressor

# Get compressed schema for LLM prompt
compressor = SchemaCompressor()
schema = compressor.compress(df)
llm_context = compressor.to_text(schema)

# Use with your LLM
prompt = f"""
Analyze this dataset:

{llm_context}

What insights can you provide?
"""
```

### Use Case 3: Iterative Analysis

```python
agent = EDAAgent(df)

# Step 1
agent.analyze_missing_values()

# Step 2 - based on suggestions
suggestions = agent.suggest_next_steps()
print(suggestions[0])  # Follow first suggestion

# Step 3
agent.analyze_correlations()

# Get compressed history for context
history = agent.get_history_context()
print(f"History uses only {len(history)//4} tokens")
```

## 🎨 Visualizations

```python
from src.visualizations import *

# Setup plotting style
setup_plot_style()

# Visualize missing values
plot_missing_values(df)

# Plot correlations
plot_correlation_matrix(df)

# Plot distributions
plot_numeric_distributions(df)

# Detect outliers visually
plot_outlier_detection(df, 'Age')
```

## 📈 Token Efficiency Examples

### Real-world Savings

| Dataset Size | Traditional | Compressed | Saved | Cost Saved* |
|-------------|------------|------------|-------|-------------|
| 1K rows × 10 cols | 50K tokens | 500 tokens | 99% | $0.099 |
| 10K rows × 20 cols | 500K tokens | 1K tokens | 99.8% | $0.998 |
| 100K rows × 50 cols | 5M tokens | 2.5K tokens | 99.95% | $9.99 |

*At $0.002 per 1K tokens (GPT-4 pricing)

## 🐛 Troubleshooting

### Import Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Jupyter Kernel Issues
```bash
# Install kernel
python -m ipykernel install --user --name=venv
```

### Module Not Found
```bash
# Make sure you're in the project directory
cd "Data Analysis Agent"

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## 📖 Next Steps

1. ✅ Complete the demo notebook: `examples/demo_analysis.ipynb`
2. 📊 Try with your own datasets
3. 🔧 Customize compression parameters
4. 🤖 Integrate with your LLM workflows
5. 📚 Read the full README.md for advanced features

## 🆘 Getting Help

- 📖 **Documentation**: See README.md
- 🐛 **Issues**: Report bugs on GitHub
- 💬 **Questions**: Open a discussion
- 📧 **Email**: support@example.com

## 🎉 You're Ready!

You now have everything you need to start efficient data analysis with minimal token usage. Happy analyzing! 🚀
