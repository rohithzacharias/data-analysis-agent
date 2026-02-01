"""
Simple Example: Data Analysis Agent in Action

This script demonstrates the core functionality of the Data Analysis Agent.
Run this after setting up the environment to see the system in action.

Usage:
    python simple_example.py
"""

import sys
sys.path.insert(0, 'src')

print("=" * 70)
print("🧠 DATA ANALYSIS AGENT - Simple Example")
print("=" * 70)
print()

# Step 1: Import modules
print("📦 Step 1: Importing modules...")
try:
    from src.eda_agent import EDAAgent
    from src.utils import load_sample_data
    from src.schema_compressor import SchemaCompressor
    print("✓ Modules imported successfully\n")
except ImportError as e:
    print(f"✗ Error importing modules: {e}")
    print("\nMake sure you've installed dependencies:")
    print("  pip install -r requirements.txt\n")
    sys.exit(1)

# Step 2: Load sample data
print("📊 Step 2: Loading sample dataset...")
df = load_sample_data('titanic')
print(f"✓ Loaded Titanic dataset: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  Columns: {', '.join(df.columns.tolist()[:5])}...\n")

# Step 3: Demonstrate schema compression
print("🗜️  Step 3: Compressing schema...")
compressor = SchemaCompressor()
schema = compressor.compress(df)
print(compressor.to_text(schema))
print()

# Show token savings
stats = compressor.estimate_token_reduction(df)
print(f"💰 Token Efficiency:")
print(f"  • Schema tokens: {stats['schema_tokens']:,}")
print(f"  • Full dataset tokens (estimated): {stats['estimated_full_tokens']:,}")
print(f"  • Reduction ratio: {stats['reduction_ratio']:.1f}x")
print(f"  • Tokens saved: {stats['tokens_saved']:,}")
print(f"  • Cost saved (at $0.002/1K tokens): ${stats['tokens_saved'] * 0.002 / 1000:.4f}\n")

# Step 4: Initialize EDA Agent
print("🤖 Step 4: Initializing EDA Agent...")
agent = EDAAgent(df, name="Titanic Analysis")
print("✓ Agent initialized\n")

# Step 5: Get suggestions
print("💡 Step 5: Getting analysis suggestions...")
suggestions = agent.suggest_next_steps()
print("Agent suggests:")
for i, suggestion in enumerate(suggestions[:3], 1):
    print(f"  {i}. {suggestion}")
print()

# Step 6: Run quick analyses
print("🔍 Step 6: Running analyses...")
print("\n[Missing Value Analysis]")
missing_results = agent.analyze_missing_values()
for insight in missing_results['insights']:
    print(f"  • {insight}")

print("\n[Distribution Analysis]")
dist_results = agent.analyze_distributions()
for insight in dist_results['insights'][:3]:
    print(f"  • {insight}")

print("\n[Correlation Analysis]")
corr_results = agent.analyze_correlations(threshold=0.5)
for insight in corr_results['insights'][:3]:
    print(f"  • {insight}")

# Step 7: Show history compression
print("\n📝 Step 7: Viewing compressed history...")
history_context = agent.get_history_context()
print(f"Compressed history context ({len(history_context)} chars, ~{len(history_context)//4} tokens):")
print(f"  {history_context}\n")

history_stats = agent.history_compressor.estimate_token_savings()
print(f"History compression:")
print(f"  • Full history: {history_stats['full_history_tokens']:,} tokens")
print(f"  • Compressed: {history_stats['compressed_tokens']:,} tokens")
print(f"  • Compression ratio: {history_stats['compression_ratio']:.1f}x\n")

# Step 8: Generate summary
print("📋 Step 8: Generating summary report...")
print()
print("=" * 70)
report = agent.generate_summary_report()
print(report)

print("\n" + "=" * 70)
print("✅ Example completed successfully!")
print("=" * 70)
print()
print("🎯 Next Steps:")
print("  1. Run the full demo notebook: jupyter notebook examples/demo_analysis.ipynb")
print("  2. Try the CLI: python cli.py sample iris")
print("  3. Analyze your own data: python cli.py analyze your_data.csv --auto")
print("  4. Read GETTING_STARTED.md for more examples")
print()