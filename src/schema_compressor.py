"""
Schema Compression Module
Compresses dataset schema to minimize token usage while preserving semantic meaning.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import json


class SchemaCompressor:
    """
    Compresses dataset schema by extracting essential metadata:
    - Column names and data types
    - Missing value ratios
    - Basic statistics (mean, min, max, std)
    - Cardinality for categorical features
    - Sample values for better context
    """
    
    def __init__(self, max_categorical_samples: int = 5):
        """
        Initialize the SchemaCompressor.
        
        Args:
            max_categorical_samples: Maximum number of unique values to show for categorical columns
        """
        self.max_categorical_samples = max_categorical_samples
    
    def compress(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a compressed schema representation of the dataset.
        
        Args:
            df: Input pandas DataFrame
            
        Returns:
            Dictionary containing compressed schema information
        """
        schema = {
            "shape": {
                "rows": len(df),
                "columns": len(df.columns)
            },
            "columns": {},
            "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024)
        }
        
        for col in df.columns:
            col_info = self._compress_column(df[col])
            schema["columns"][col] = col_info
        
        return schema
    
    def _compress_column(self, series: pd.Series) -> Dict[str, Any]:
        """
        Compress information for a single column.
        
        Args:
            series: Pandas Series representing a column
            
        Returns:
            Dictionary with compressed column information
        """
        col_info = {
            "dtype": str(series.dtype),
            "missing_ratio": series.isna().sum() / len(series),
            "missing_count": int(series.isna().sum()),
        }
        
        # Determine if column is numeric or categorical
        if pd.api.types.is_numeric_dtype(series):
            col_info.update(self._get_numeric_stats(series))
        else:
            col_info.update(self._get_categorical_stats(series))
        
        return col_info
    
    def _get_numeric_stats(self, series: pd.Series) -> Dict[str, Any]:
        """Extract statistics for numeric columns."""
        non_null = series.dropna()
        
        if len(non_null) == 0:
            return {
                "type": "numeric",
                "stats": None
            }
        
        return {
            "type": "numeric",
            "stats": {
                "mean": float(non_null.mean()),
                "std": float(non_null.std()),
                "min": float(non_null.min()),
                "max": float(non_null.max()),
                "median": float(non_null.median()),
                "q25": float(non_null.quantile(0.25)),
                "q75": float(non_null.quantile(0.75)),
            },
            "unique_count": int(series.nunique())
        }
    
    def _get_categorical_stats(self, series: pd.Series) -> Dict[str, Any]:
        """Extract statistics for categorical columns."""
        non_null = series.dropna()
        unique_count = series.nunique()
        
        stats = {
            "type": "categorical",
            "unique_count": int(unique_count),
            "cardinality": "high" if unique_count > 50 else "medium" if unique_count > 10 else "low"
        }
        
        # Add top values for low/medium cardinality
        if unique_count <= self.max_categorical_samples:
            value_counts = series.value_counts().head(self.max_categorical_samples)
            stats["top_values"] = {
                str(k): int(v) for k, v in value_counts.items()
            }
        else:
            # For high cardinality, just show top N
            value_counts = series.value_counts().head(self.max_categorical_samples)
            stats["sample_values"] = list(value_counts.index.astype(str))
        
        return stats
    
    def to_text(self, schema: Dict[str, Any]) -> str:
        """
        Convert compressed schema to human-readable text format.
        
        Args:
            schema: Compressed schema dictionary
            
        Returns:
            Formatted string representation
        """
        lines = [
            "=== DATASET SCHEMA ===",
            f"Shape: {schema['shape']['rows']} rows × {schema['shape']['columns']} columns",
            f"Memory: {schema['memory_usage_mb']:.2f} MB",
            "",
            "=== COLUMNS ===",
        ]
        
        for col_name, col_info in schema["columns"].items():
            lines.append(f"\n[{col_name}]")
            lines.append(f"  Type: {col_info['type']} ({col_info['dtype']})")
            lines.append(f"  Missing: {col_info['missing_ratio']:.1%} ({col_info['missing_count']} values)")
            
            if col_info["type"] == "numeric":
                if col_info["stats"]:
                    stats = col_info["stats"]
                    lines.append(f"  Range: [{stats['min']:.2f}, {stats['max']:.2f}]")
                    lines.append(f"  Mean ± Std: {stats['mean']:.2f} ± {stats['std']:.2f}")
                    lines.append(f"  Median: {stats['median']:.2f}")
                    lines.append(f"  Unique: {col_info['unique_count']}")
            else:
                lines.append(f"  Cardinality: {col_info['cardinality']} ({col_info['unique_count']} unique)")
                if "top_values" in col_info:
                    lines.append(f"  Values: {', '.join(col_info['top_values'].keys())}")
                elif "sample_values" in col_info:
                    lines.append(f"  Sample: {', '.join(col_info['sample_values'][:3])}...")
        
        return "\n".join(lines)
    
    def to_json(self, schema: Dict[str, Any], pretty: bool = True) -> str:
        """
        Convert schema to JSON string.
        
        Args:
            schema: Compressed schema dictionary
            pretty: Whether to format JSON with indentation
            
        Returns:
            JSON string
        """
        if pretty:
            return json.dumps(schema, indent=2)
        return json.dumps(schema)
    
    def estimate_token_reduction(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Estimate token reduction compared to sending full dataset.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with token estimates
        """
        # Rough estimation: 1 token ≈ 4 characters
        schema = self.compress(df)
        schema_text = self.to_text(schema)
        schema_tokens = len(schema_text) // 4
        
        # Estimate full dataset size (first 100 rows as sample)
        sample_text = df.head(100).to_string()
        full_dataset_tokens = (len(sample_text) * len(df)) // (100 * 4)
        
        return {
            "schema_tokens": schema_tokens,
            "estimated_full_tokens": full_dataset_tokens,
            "reduction_ratio": full_dataset_tokens / schema_tokens if schema_tokens > 0 else 0,
            "tokens_saved": full_dataset_tokens - schema_tokens
        }
