"""
Command-line interface for the Data Analysis Agent.
"""

import argparse
import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.eda_agent import EDAAgent
from src.schema_compressor import SchemaCompressor
from src.utils import load_sample_data


def analyze_file(filepath, output=None, auto=False):
    """Analyze a CSV file."""
    print(f"Loading data from {filepath}...")
    
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        return 1
    
    print("\nInitializing EDA Agent...")
    agent = EDAAgent(df, name=Path(filepath).stem)
    
    if auto:
        print("\n" + "=" * 60)
        print("Running Automated EDA...")
        print("=" * 60)
        results = agent.run_automated_eda()
        report = results['summary_report']
    else:
        print("\nRunning step-by-step analysis...")
        agent.analyze_missing_values()
        agent.analyze_distributions()
        agent.analyze_correlations()
        agent.detect_outliers()
        report = agent.generate_summary_report()
    
    print("\n" + report)
    
    if output:
        print(f"\nSaving report to {output}...")
        with open(output, 'w') as f:
            f.write(report)
        print("✓ Report saved")
    
    return 0


def analyze_sample(dataset_name, output=None):
    """Analyze a sample dataset."""
    print(f"Loading sample dataset: {dataset_name}...")
    
    try:
        df = load_sample_data(dataset_name)
        print(f"✓ Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    except Exception as e:
        print(f"✗ Error loading sample: {e}")
        return 1
    
    print("\nRunning automated EDA...")
    agent = EDAAgent(df, name=f"{dataset_name.title()} Analysis")
    results = agent.run_automated_eda()
    report = results['summary_report']
    
    print("\n" + report)
    
    if output:
        print(f"\nSaving report to {output}...")
        with open(output, 'w') as f:
            f.write(report)
        print("✓ Report saved")
    
    return 0


def compress_schema(filepath, output=None):
    """Compress schema of a CSV file."""
    print(f"Loading data from {filepath}...")
    
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        return 1
    
    print("\nCompressing schema...")
    compressor = SchemaCompressor()
    schema = compressor.compress(df)
    schema_text = compressor.to_text(schema)
    
    print("\n" + "=" * 60)
    print(schema_text)
    print("=" * 60)
    
    # Show token efficiency
    stats = compressor.estimate_token_reduction(df)
    print(f"\n💰 Token Efficiency:")
    print(f"  Schema tokens: {stats['schema_tokens']:,}")
    print(f"  Estimated full tokens: {stats['estimated_full_tokens']:,}")
    print(f"  Reduction: {stats['reduction_ratio']:.1f}x")
    print(f"  Tokens saved: {stats['tokens_saved']:,}")
    
    if output:
        print(f"\nSaving schema to {output}...")
        with open(output, 'w') as f:
            f.write(schema_text)
        print("✓ Schema saved")
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Data Analysis Agent - AI-powered EDA with compression",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a CSV file
  python cli.py analyze data.csv

  # Automated analysis with output
  python cli.py analyze data.csv --auto --output report.txt

  # Analyze sample dataset
  python cli.py sample titanic

  # Compress schema only
  python cli.py schema data.csv --output schema.txt
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a CSV file')
    analyze_parser.add_argument('file', help='Path to CSV file')
    analyze_parser.add_argument('--output', '-o', help='Output file for report')
    analyze_parser.add_argument('--auto', '-a', action='store_true', 
                               help='Run automated EDA')
    
    # Sample command
    sample_parser = subparsers.add_parser('sample', help='Analyze sample dataset')
    sample_parser.add_argument('dataset', 
                              choices=['iris', 'titanic', 'tips', 'random'],
                              help='Sample dataset name')
    sample_parser.add_argument('--output', '-o', help='Output file for report')
    
    # Schema command
    schema_parser = subparsers.add_parser('schema', help='Compress schema only')
    schema_parser.add_argument('file', help='Path to CSV file')
    schema_parser.add_argument('--output', '-o', help='Output file for schema')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'analyze':
            return analyze_file(args.file, args.output, args.auto)
        elif args.command == 'sample':
            return analyze_sample(args.dataset, args.output)
        elif args.command == 'schema':
            return compress_schema(args.file, args.output)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
