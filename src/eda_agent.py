"""
EDA AI Agent
Intelligent agent for automated exploratory data analysis using compressed schema and history.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List, Optional, Tuple
import warnings

from .schema_compressor import SchemaCompressor
from .history_compressor import HistoryCompressor, AnalysisStep

warnings.filterwarnings('ignore')


class EDAAgent:
    """
    AI-powered EDA agent that:
    - Uses compressed schema for context
    - Maintains compressed analysis history
    - Suggests next analytical steps
    - Generates insights and visualizations
    - Minimizes token usage for LLM integration
    """
    
    def __init__(self, df: pd.DataFrame, name: str = "EDA Agent"):
        """
        Initialize the EDA Agent.
        
        Args:
            df: Input pandas DataFrame
            name: Name identifier for the agent
        """
        self.df = df
        self.name = name
        self.schema_compressor = SchemaCompressor()
        self.history_compressor = HistoryCompressor()
        
        # Generate compressed schema
        self.compressed_schema = self.schema_compressor.compress(df)
        
        # Initialize analysis state
        self.current_step = 0
        
    def get_schema_context(self) -> str:
        """Get compressed schema as text context."""
        return self.schema_compressor.to_text(self.compressed_schema)
    
    def get_history_context(self) -> str:
        """Get compressed history as text context."""
        return self.history_compressor.get_context_for_next_step()
    
    def get_full_context(self) -> str:
        """Get combined context for LLM prompting."""
        context = [
            f"=== {self.name} Context ===\n",
            self.get_schema_context(),
            "\n\n",
            self.history_compressor.to_text()
        ]
        return "".join(context)
    
    def suggest_next_steps(self) -> List[str]:
        """
        Suggest next analytical steps based on current state.
        
        Returns:
            List of suggested actions
        """
        suggestions = []
        
        # Check if initial exploration is done
        if self.current_step == 0:
            suggestions.extend([
                "Examine basic statistics and data distribution",
                "Check for missing values and data quality issues",
                "Identify column types and potential features"
            ])
            return suggestions
        
        # Analyze schema for specific suggestions
        for col_name, col_info in self.compressed_schema["columns"].items():
            
            # Missing value suggestions
            if col_info["missing_ratio"] > 0.1:
                suggestions.append(
                    f"Investigate missing values in '{col_name}' ({col_info['missing_ratio']:.1%} missing)"
                )
            
            # Numeric analysis suggestions
            if col_info["type"] == "numeric" and col_info["stats"]:
                stats = col_info["stats"]
                # Check for outliers (simple IQR-based heuristic)
                iqr = stats["q75"] - stats["q25"]
                if iqr > 0:
                    lower_bound = stats["q25"] - 1.5 * iqr
                    upper_bound = stats["q75"] + 1.5 * iqr
                    if stats["min"] < lower_bound or stats["max"] > upper_bound:
                        suggestions.append(
                            f"Analyze potential outliers in '{col_name}'"
                        )
                
                # Check for skewness
                if stats["mean"] > stats["median"] * 1.5 or stats["mean"] < stats["median"] * 0.67:
                    suggestions.append(
                        f"Examine distribution skewness in '{col_name}'"
                    )
            
            # Categorical analysis suggestions
            if col_info["type"] == "categorical":
                if col_info["cardinality"] == "high":
                    suggestions.append(
                        f"Analyze high cardinality in '{col_name}' ({col_info['unique_count']} unique values)"
                    )
        
        # Relationship analysis
        numeric_cols = [
            col for col, info in self.compressed_schema["columns"].items()
            if info["type"] == "numeric"
        ]
        if len(numeric_cols) >= 2:
            suggestions.append("Explore correlations between numeric features")
        
        # Limit suggestions
        return suggestions[:5]
    
    def analyze_missing_values(self) -> Dict[str, Any]:
        """
        Analyze missing values in the dataset.
        
        Returns:
            Dictionary with missing value analysis results
        """
        missing_summary = {}
        missing_cols = []
        
        for col in self.df.columns:
            missing_count = self.df[col].isna().sum()
            if missing_count > 0:
                missing_ratio = missing_count / len(self.df)
                missing_cols.append(col)
                missing_summary[col] = {
                    "count": int(missing_count),
                    "ratio": float(missing_ratio)
                }
        
        insights = []
        if missing_cols:
            insights.append(f"Found {len(missing_cols)} columns with missing values")
            high_missing = [c for c, v in missing_summary.items() if v["ratio"] > 0.3]
            if high_missing:
                insights.append(f"{len(high_missing)} columns have >30% missing data")
        else:
            insights.append("No missing values detected in dataset")
        
        # Record in history
        self.history_compressor.add_step(
            action="missing_value_analysis",
            description=f"Analyzed missing values across {len(self.df.columns)} columns",
            insights=insights
        )
        
        self.current_step += 1
        
        return {
            "summary": missing_summary,
            "insights": insights,
            "columns_with_missing": missing_cols
        }
    
    def analyze_distributions(self, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze distributions of numeric columns.
        
        Args:
            columns: Specific columns to analyze (None = all numeric)
            
        Returns:
            Dictionary with distribution analysis
        """
        if columns is None:
            columns = [
                col for col, info in self.compressed_schema["columns"].items()
                if info["type"] == "numeric"
            ]
        
        distributions = {}
        insights = []
        
        for col in columns:
            if col not in self.df.columns:
                continue
                
            series = self.df[col].dropna()
            if len(series) == 0:
                continue
            
            # Calculate distribution metrics
            skewness = series.skew()
            kurtosis = series.kurtosis()
            
            dist_type = "normal"
            if abs(skewness) > 1:
                dist_type = "right-skewed" if skewness > 0 else "left-skewed"
            
            distributions[col] = {
                "skewness": float(skewness),
                "kurtosis": float(kurtosis),
                "distribution_type": dist_type
            }
            
            if abs(skewness) > 1:
                insights.append(f"'{col}' is {dist_type} (skew={skewness:.2f})")
        
        # Record in history
        self.history_compressor.add_step(
            action="distribution_analysis",
            description=f"Analyzed distributions for {len(columns)} numeric columns",
            insights=insights if insights else ["All distributions appear relatively normal"]
        )
        
        self.current_step += 1
        
        return {
            "distributions": distributions,
            "insights": insights
        }
    
    def analyze_correlations(self, threshold: float = 0.7) -> Dict[str, Any]:
        """
        Analyze correlations between numeric features.
        
        Args:
            threshold: Correlation threshold for flagging strong relationships
            
        Returns:
            Dictionary with correlation analysis
        """
        numeric_cols = [
            col for col, info in self.compressed_schema["columns"].items()
            if info["type"] == "numeric"
        ]
        
        if len(numeric_cols) < 2:
            return {
                "correlations": None,
                "insights": ["Not enough numeric columns for correlation analysis"]
            }
        
        corr_matrix = self.df[numeric_cols].corr()
        
        # Find strong correlations
        strong_correlations = []
        insights = []
        
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_correlations.append({
                        "feature1": numeric_cols[i],
                        "feature2": numeric_cols[j],
                        "correlation": float(corr_value)
                    })
                    insights.append(
                        f"Strong correlation ({corr_value:.2f}) between "
                        f"'{numeric_cols[i]}' and '{numeric_cols[j]}'"
                    )
        
        if not insights:
            insights.append(f"No strong correlations found (threshold={threshold})")
        
        # Record in history
        self.history_compressor.add_step(
            action="correlation_analysis",
            description=f"Analyzed correlations among {len(numeric_cols)} numeric features",
            insights=insights
        )
        
        self.current_step += 1
        
        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_correlations,
            "insights": insights
        }
    
    def detect_outliers(self, columns: Optional[List[str]] = None, method: str = "iqr") -> Dict[str, Any]:
        """
        Detect outliers in numeric columns.
        
        Args:
            columns: Specific columns to check (None = all numeric)
            method: Detection method ('iqr' or 'zscore')
            
        Returns:
            Dictionary with outlier analysis
        """
        if columns is None:
            columns = [
                col for col, info in self.compressed_schema["columns"].items()
                if info["type"] == "numeric"
            ]
        
        outliers = {}
        insights = []
        
        for col in columns:
            if col not in self.df.columns:
                continue
                
            series = self.df[col].dropna()
            if len(series) == 0:
                continue
            
            if method == "iqr":
                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outlier_mask = (series < lower_bound) | (series > upper_bound)
            else:  # zscore
                z_scores = np.abs((series - series.mean()) / series.std())
                outlier_mask = z_scores > 3
            
            outlier_count = outlier_mask.sum()
            if outlier_count > 0:
                outliers[col] = {
                    "count": int(outlier_count),
                    "ratio": float(outlier_count / len(series))
                }
                insights.append(
                    f"'{col}' has {outlier_count} outliers ({outliers[col]['ratio']:.1%})"
                )
        
        if not insights:
            insights.append("No significant outliers detected")
        
        # Record in history
        self.history_compressor.add_step(
            action="outlier_detection",
            description=f"Detected outliers using {method} method",
            insights=insights
        )
        
        self.current_step += 1
        
        return {
            "outliers": outliers,
            "insights": insights,
            "method": method
        }
    
    def generate_summary_report(self) -> str:
        """
        Generate a comprehensive summary report.
        
        Returns:
            Formatted report string
        """
        report_sections = [
            "=" * 60,
            f"{self.name} - Analysis Summary Report",
            "=" * 60,
            "",
            self.get_schema_context(),
            "\n",
            self.history_compressor.to_text(),
            "\n",
            "=" * 60,
            "SUGGESTED NEXT STEPS:",
            "=" * 60,
        ]
        
        suggestions = self.suggest_next_steps()
        for i, suggestion in enumerate(suggestions, 1):
            report_sections.append(f"{i}. {suggestion}")
        
        # Add token efficiency stats
        report_sections.extend([
            "\n",
            "=" * 60,
            "TOKEN EFFICIENCY METRICS:",
            "=" * 60,
        ])
        
        schema_stats = self.schema_compressor.estimate_token_reduction(self.df)
        report_sections.append(
            f"Schema Compression: {schema_stats['reduction_ratio']:.1f}x reduction "
            f"({schema_stats['tokens_saved']:,} tokens saved)"
        )
        
        if self.current_step > 0:
            history_stats = self.history_compressor.estimate_token_savings()
            report_sections.append(
                f"History Compression: {history_stats['compression_ratio']:.1f}x reduction "
                f"({history_stats['tokens_saved']:,} tokens saved)"
            )
        
        return "\n".join(report_sections)
    
    def run_automated_eda(self) -> Dict[str, Any]:
        """
        Run a complete automated EDA sequence.
        
        Returns:
            Dictionary with all analysis results
        """
        results = {
            "schema": self.compressed_schema,
            "analyses": {}
        }
        
        # Step 1: Missing values
        results["analyses"]["missing_values"] = self.analyze_missing_values()
        
        # Step 2: Distributions
        results["analyses"]["distributions"] = self.analyze_distributions()
        
        # Step 3: Correlations (if enough numeric columns)
        results["analyses"]["correlations"] = self.analyze_correlations()
        
        # Step 4: Outliers
        results["analyses"]["outliers"] = self.detect_outliers()
        
        # Generate final report
        results["summary_report"] = self.generate_summary_report()
        
        return results
