"""
Data Analysis Agent
Efficient Exploratory Data Analysis with Schema & History Compression
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .schema_compressor import SchemaCompressor
from .history_compressor import HistoryCompressor
from .eda_agent import EDAAgent
from .scaledown_api import ScaleDownIntegration

__all__ = [
    "SchemaCompressor",
    "HistoryCompressor",
    "EDAAgent",
    "ScaleDownIntegration",
]
