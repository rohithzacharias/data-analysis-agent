"""
Simple test script to verify all modules work correctly.
Run this after installation to ensure everything is set up properly.
"""

import sys
import pandas as pd
import numpy as np

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    try:
        from src.schema_compressor import SchemaCompressor
        from src.history_compressor import HistoryCompressor
        from src.eda_agent import EDAAgent
        from src.utils import load_sample_data
        from src.visualizations import setup_plot_style
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_schema_compression():
    """Test schema compression module."""
    print("\nTesting schema compression...")
    try:
        from src.schema_compressor import SchemaCompressor
        from src.utils import load_sample_data
        
        df = load_sample_data('iris')
        compressor = SchemaCompressor()
        schema = compressor.compress(df)
        text = compressor.to_text(schema)
        stats = compressor.estimate_token_reduction(df)
        
        assert 'shape' in schema
        assert 'columns' in schema
        assert len(text) > 0
        assert stats['reduction_ratio'] > 1
        
        print(f"✓ Schema compression works (reduction: {stats['reduction_ratio']:.1f}x)")
        return True
    except Exception as e:
        print(f"✗ Schema compression error: {e}")
        return False


def test_history_compression():
    """Test history compression module."""
    print("\nTesting history compression...")
    try:
        from src.history_compressor import HistoryCompressor
        
        history = HistoryCompressor()
        history.add_step(
            action="test",
            description="Test step",
            insights=["Test insight"]
        )
        
        context = history.get_context_for_next_step()
        text = history.to_text()
        
        assert len(context) > 0
        assert len(text) > 0
        assert len(history.history) == 1
        
        print("✓ History compression works")
        return True
    except Exception as e:
        print(f"✗ History compression error: {e}")
        return False


def test_eda_agent():
    """Test EDA agent module."""
    print("\nTesting EDA agent...")
    try:
        from src.eda_agent import EDAAgent
        from src.utils import load_sample_data
        
        df = load_sample_data('iris')
        agent = EDAAgent(df, name="Test Agent")
        
        # Test individual analyses
        missing_results = agent.analyze_missing_values()
        dist_results = agent.analyze_distributions()
        corr_results = agent.analyze_correlations()
        
        assert 'insights' in missing_results
        assert 'insights' in dist_results
        assert 'insights' in corr_results
        
        # Test suggestions
        suggestions = agent.suggest_next_steps()
        assert isinstance(suggestions, list)
        
        # Test report generation
        report = agent.generate_summary_report()
        assert len(report) > 0
        
        print("✓ EDA agent works")
        return True
    except Exception as e:
        print(f"✗ EDA agent error: {e}")
        return False


def test_sample_data():
    """Test sample data loading."""
    print("\nTesting sample data loading...")
    try:
        from src.utils import load_sample_data
        
        datasets = ['iris', 'titanic', 'tips', 'random']
        for name in datasets:
            df = load_sample_data(name)
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0
            print(f"  ✓ {name} dataset loaded ({df.shape[0]} rows)")
        
        print("✓ Sample data loading works")
        return True
    except Exception as e:
        print(f"✗ Sample data error: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Data Analysis Agent - Module Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_schema_compression,
        test_history_compression,
        test_eda_agent,
        test_sample_data
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n🎉 All tests passed! The system is ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
