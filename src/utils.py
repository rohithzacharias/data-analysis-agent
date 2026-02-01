"""
Utility functions for the Data Analysis Agent.
"""

import pandas as pd
import numpy as np
from typing import Optional


def load_sample_data(dataset_name: str = "iris") -> pd.DataFrame:
    """
    Load a sample dataset for testing and demonstration.
    
    Args:
        dataset_name: Name of the dataset ('iris', 'titanic', 'tips', 'random')
        
    Returns:
        Sample DataFrame
    """
    if dataset_name == "iris":
        return load_iris_data()
    elif dataset_name == "titanic":
        return load_titanic_sample()
    elif dataset_name == "tips":
        return load_tips_sample()
    elif dataset_name == "random":
        return generate_random_data()
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")


def load_iris_data() -> pd.DataFrame:
    """Load the Iris dataset."""
    from sklearn.datasets import load_iris
    
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = iris.target_names[iris.target]
    return df


def load_titanic_sample() -> pd.DataFrame:
    """Create a sample Titanic-like dataset."""
    np.random.seed(42)
    n = 200
    
    df = pd.DataFrame({
        'PassengerId': range(1, n + 1),
        'Survived': np.random.choice([0, 1], n, p=[0.62, 0.38]),
        'Pclass': np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55]),
        'Name': [f"Passenger {i}" for i in range(1, n + 1)],
        'Sex': np.random.choice(['male', 'female'], n, p=[0.65, 0.35]),
        'Age': np.random.normal(30, 14, n).clip(0.5, 80),
        'SibSp': np.random.poisson(0.5, n),
        'Parch': np.random.poisson(0.4, n),
        'Fare': np.random.lognormal(3, 1, n),
        'Embarked': np.random.choice(['C', 'Q', 'S'], n, p=[0.19, 0.09, 0.72])
    })
    
    # Introduce some missing values
    missing_mask = np.random.random(n) < 0.2
    df.loc[missing_mask, 'Age'] = np.nan
    
    missing_mask = np.random.random(n) < 0.05
    df.loc[missing_mask, 'Embarked'] = np.nan
    
    return df


def load_tips_sample() -> pd.DataFrame:
    """Create a sample tips dataset."""
    np.random.seed(42)
    n = 150
    
    df = pd.DataFrame({
        'total_bill': np.random.uniform(10, 50, n),
        'tip': np.random.uniform(1, 10, n),
        'sex': np.random.choice(['Male', 'Female'], n),
        'smoker': np.random.choice(['Yes', 'No'], n, p=[0.3, 0.7]),
        'day': np.random.choice(['Thur', 'Fri', 'Sat', 'Sun'], n),
        'time': np.random.choice(['Lunch', 'Dinner'], n, p=[0.35, 0.65]),
        'size': np.random.choice([1, 2, 3, 4, 5, 6], n, p=[0.05, 0.35, 0.25, 0.20, 0.10, 0.05])
    })
    
    # Make tip correlate somewhat with total_bill
    df['tip'] = df['total_bill'] * 0.15 + np.random.normal(0, 1, n)
    df['tip'] = df['tip'].clip(1, None)
    
    return df


def generate_random_data(
    n_rows: int = 100,
    n_numeric: int = 5,
    n_categorical: int = 3,
    missing_ratio: float = 0.1
) -> pd.DataFrame:
    """
    Generate random synthetic data.
    
    Args:
        n_rows: Number of rows
        n_numeric: Number of numeric columns
        n_categorical: Number of categorical columns
        missing_ratio: Ratio of missing values to introduce
        
    Returns:
        Random DataFrame
    """
    np.random.seed(42)
    data = {}
    
    # Generate numeric columns
    for i in range(n_numeric):
        if i % 3 == 0:
            # Normal distribution
            data[f'numeric_{i}'] = np.random.normal(100, 20, n_rows)
        elif i % 3 == 1:
            # Skewed distribution
            data[f'numeric_{i}'] = np.random.lognormal(3, 1, n_rows)
        else:
            # Uniform distribution
            data[f'numeric_{i}'] = np.random.uniform(0, 100, n_rows)
    
    # Generate categorical columns
    for i in range(n_categorical):
        n_categories = np.random.randint(3, 10)
        categories = [f'cat_{j}' for j in range(n_categories)]
        data[f'categorical_{i}'] = np.random.choice(categories, n_rows)
    
    df = pd.DataFrame(data)
    
    # Introduce missing values
    if missing_ratio > 0:
        for col in df.columns:
            missing_mask = np.random.random(n_rows) < missing_ratio
            df.loc[missing_mask, col] = np.nan
    
    return df


def format_bytes(bytes_size: int) -> str:
    """
    Format bytes into human-readable string.
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in text.
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    # Rough approximation: 1 token ≈ 4 characters
    return len(text) // 4
