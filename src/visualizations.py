"""
Visualization utilities for the Data Analysis Agent.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional, Tuple


def setup_plot_style():
    """Set up consistent plotting style."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10


def plot_missing_values(df: pd.DataFrame, figsize: Tuple[int, int] = (10, 6)):
    """
    Visualize missing values in the dataset.
    
    Args:
        df: Input DataFrame
        figsize: Figure size tuple
    """
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
    
    if len(missing_data) == 0:
        print("✓ No missing values in the dataset!")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Bar plot of missing counts
    missing_data.plot(kind='bar', ax=ax1, color='coral')
    ax1.set_title('Missing Values Count')
    ax1.set_xlabel('Columns')
    ax1.set_ylabel('Count')
    ax1.tick_params(axis='x', rotation=45)
    
    # Percentage plot
    missing_pct = (missing_data / len(df) * 100)
    missing_pct.plot(kind='bar', ax=ax2, color='steelblue')
    ax2.set_title('Missing Values Percentage')
    ax2.set_xlabel('Columns')
    ax2.set_ylabel('Percentage (%)')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()


def plot_numeric_distributions(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    ncols: int = 3
):
    """
    Plot distributions of numeric columns.
    
    Args:
        df: Input DataFrame
        columns: Specific columns to plot (None = all numeric)
        ncols: Number of columns in the subplot grid
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not columns:
        print("No numeric columns to plot!")
        return
    
    nrows = (len(columns) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = axes.flatten() if nrows > 1 or ncols > 1 else [axes]
    
    for idx, col in enumerate(columns):
        ax = axes[idx]
        data = df[col].dropna()
        
        # Histogram with KDE
        ax.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax.set_title(f'{col}\n(μ={data.mean():.2f}, σ={data.std():.2f})')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        
        # Add KDE line
        try:
            data.plot(kind='density', ax=ax, secondary_y=True, color='red', alpha=0.5)
        except:
            pass
    
    # Hide empty subplots
    for idx in range(len(columns), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (10, 8),
    annot: bool = True
):
    """
    Plot correlation matrix heatmap.
    
    Args:
        df: Input DataFrame
        columns: Specific columns (None = all numeric)
        figsize: Figure size
        annot: Whether to annotate cells with values
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(columns) < 2:
        print("Need at least 2 numeric columns for correlation!")
        return
    
    corr_matrix = df[columns].corr()
    
    plt.figure(figsize=figsize)
    sns.heatmap(
        corr_matrix,
        annot=annot,
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        fmt='.2f' if annot else None
    )
    plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_categorical_distributions(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    ncols: int = 2
):
    """
    Plot distributions of categorical columns.
    
    Args:
        df: Input DataFrame
        columns: Specific columns (None = all categorical)
        ncols: Number of columns in subplot grid
    """
    if columns is None:
        columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not columns:
        print("No categorical columns to plot!")
        return
    
    nrows = (len(columns) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows))
    axes = axes.flatten() if nrows > 1 or ncols > 1 else [axes]
    
    for idx, col in enumerate(columns):
        ax = axes[idx]
        value_counts = df[col].value_counts().head(10)  # Top 10 only
        
        value_counts.plot(kind='bar', ax=ax, color='lightgreen', edgecolor='black')
        ax.set_title(f'{col}\n({df[col].nunique()} unique values)')
        ax.set_xlabel('')
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', rotation=45)
    
    # Hide empty subplots
    for idx in range(len(columns), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.show()


def plot_outlier_detection(
    df: pd.DataFrame,
    column: str,
    method: str = 'iqr'
):
    """
    Visualize outliers in a numeric column.
    
    Args:
        df: Input DataFrame
        column: Column name
        method: Detection method ('iqr' or 'zscore')
    """
    data = df[column].dropna()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Box plot
    ax1.boxplot(data, vert=True)
    ax1.set_title(f'Box Plot: {column}')
    ax1.set_ylabel('Value')
    ax1.grid(True, alpha=0.3)
    
    # Scatter plot with outliers highlighted
    if method == 'iqr':
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = (data < lower_bound) | (data > upper_bound)
    else:  # zscore
        z_scores = np.abs((data - data.mean()) / data.std())
        outliers = z_scores > 3
    
    colors = ['red' if outlier else 'blue' for outlier in outliers]
    ax2.scatter(range(len(data)), data, c=colors, alpha=0.6)
    ax2.set_title(f'Outliers in {column} ({method.upper()} method)')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Value')
    ax2.legend(['Normal', 'Outlier'])
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n📊 Outlier Summary:")
    print(f"Total outliers: {outliers.sum()} ({outliers.sum() / len(data) * 100:.2f}%)")
    print(f"Method: {method.upper()}")
