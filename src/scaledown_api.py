"""
ScaleDown API Integration
Integrates the Data Analysis Agent with ScaleDown API for maximum compression.
"""

import requests
import json
from typing import Dict, Any, Optional


class ScaleDownIntegration:
    """
    Integrates Data Analysis Agent with ScaleDown API for ultra-compression.
    
    This provides an additional layer of compression on top of the agent's
    built-in schema and history compression.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize ScaleDown integration.
        
        Args:
            api_key: ScaleDown API key
        """
        self.api_key = api_key
        self.base_url = "https://api.scaledown.xyz/compress/raw/"
        self.headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        }
    
    def compress_schema(
        self,
        schema_text: str,
        model: str = "gpt-4o",
        rate: str = "auto"
    ) -> Dict[str, Any]:
        """
        Compress schema text using ScaleDown API.
        
        Args:
            schema_text: Compressed schema from SchemaCompressor
            model: Target LLM model
            rate: Compression rate ('auto', 'high', 'medium', 'low')
            
        Returns:
            API response with compressed content
        """
        payload = {
            "context": "This is a compressed dataset schema for exploratory data analysis",
            "prompt": schema_text,
            "model": model,
            "scaledown": {
                "rate": rate
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def compress_analysis_context(
        self,
        context: str,
        model: str = "gpt-4o",
        rate: str = "auto"
    ) -> Dict[str, Any]:
        """
        Compress analysis context using ScaleDown API.
        
        Args:
            context: Analysis context from HistoryCompressor
            model: Target LLM model
            rate: Compression rate
            
        Returns:
            API response with compressed content
        """
        payload = {
            "context": "This is analysis history and insights from exploratory data analysis",
            "prompt": context,
            "model": model,
            "scaledown": {
                "rate": rate
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def compress_full_report(
        self,
        report: str,
        model: str = "gpt-4o",
        rate: str = "auto"
    ) -> Dict[str, Any]:
        """
        Compress full analysis report using ScaleDown API.
        
        Args:
            report: Complete analysis report
            model: Target LLM model
            rate: Compression rate
            
        Returns:
            API response with compressed content
        """
        payload = {
            "context": "This is a comprehensive data analysis report with insights and statistics",
            "prompt": report,
            "model": model,
            "scaledown": {
                "rate": rate
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def get_compression_stats(
        self,
        original_text: str,
        compressed_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate compression statistics.
        
        Args:
            original_text: Original text before compression
            compressed_result: Result from ScaleDown API
            
        Returns:
            Dictionary with compression statistics
        """
        if "error" in compressed_result:
            return {
                "error": "Cannot calculate stats due to API error",
                "api_error": compressed_result["error"]
            }
        
        original_tokens = len(original_text) // 4  # Rough estimate
        compressed_text = compressed_result.get("compressed", {}).get("content", "")
        compressed_tokens = len(compressed_text) // 4
        
        return {
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "reduction_ratio": original_tokens / compressed_tokens if compressed_tokens > 0 else 0,
            "tokens_saved": original_tokens - compressed_tokens,
            "compression_rate": compressed_result.get("scaledown", {}).get("rate", "unknown")
        }


def load_api_key(filepath: str = "config.json") -> Optional[str]:
    """
    Load API key from configuration file.
    
    Args:
        filepath: Path to config file
        
    Returns:
        API key or None if not found
    """
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
            return config.get("scaledown_api_key")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_api_key(api_key: str, filepath: str = "config.json"):
    """
    Save API key to configuration file.
    
    Args:
        api_key: ScaleDown API key
        filepath: Path to config file
    """
    config = {
        "scaledown_api_key": api_key
    }
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=2)
