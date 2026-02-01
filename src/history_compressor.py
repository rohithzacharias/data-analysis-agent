"""
Analysis History Compression Module
Compresses previous analytical steps to reduce token overhead while retaining key insights.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class AnalysisStep:
    """Represents a single analysis step in the EDA process."""
    
    def __init__(
        self,
        step_number: int,
        action: str,
        description: str,
        insights: List[str],
        code: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize an analysis step.
        
        Args:
            step_number: Sequential number of the analysis step
            action: Type of action (e.g., 'visualization', 'statistics', 'cleaning')
            description: Brief description of what was done
            insights: Key findings or insights from this step
            code: Optional code snippet that was executed
            timestamp: When the step was performed
        """
        self.step_number = step_number
        self.action = action
        self.description = description
        self.insights = insights
        self.code = code
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "step_number": self.step_number,
            "action": self.action,
            "description": self.description,
            "insights": self.insights,
            "code": self.code,
            "timestamp": self.timestamp.isoformat()
        }


class HistoryCompressor:
    """
    Compresses analysis history by:
    - Extracting key insights
    - Removing redundant information
    - Summarizing similar steps
    - Maintaining causal relationships between analyses
    """
    
    def __init__(self, max_steps_to_keep: int = 10):
        """
        Initialize the HistoryCompressor.
        
        Args:
            max_steps_to_keep: Maximum number of detailed steps to keep in memory
        """
        self.max_steps_to_keep = max_steps_to_keep
        self.history: List[AnalysisStep] = []
        self.archived_summary: List[str] = []
    
    def add_step(
        self,
        action: str,
        description: str,
        insights: List[str],
        code: Optional[str] = None
    ) -> AnalysisStep:
        """
        Add a new analysis step to the history.
        
        Args:
            action: Type of action performed
            description: Brief description
            insights: List of key insights
            code: Optional code snippet
            
        Returns:
            The created AnalysisStep
        """
        step_number = len(self.history) + 1
        step = AnalysisStep(step_number, action, description, insights, code)
        self.history.append(step)
        
        # If history exceeds limit, compress older steps
        if len(self.history) > self.max_steps_to_keep:
            self._archive_old_steps()
        
        return step
    
    def _archive_old_steps(self):
        """Move older steps to archived summary."""
        # Take the oldest step
        old_step = self.history.pop(0)
        
        # Create a summary entry
        summary = f"Step {old_step.step_number} ({old_step.action}): "
        summary += f"{old_step.description}. "
        if old_step.insights:
            summary += f"Insights: {'; '.join(old_step.insights)}"
        
        self.archived_summary.append(summary)
    
    def get_compressed_history(self) -> Dict[str, Any]:
        """
        Get a compressed representation of the analysis history.
        
        Returns:
            Dictionary with compressed history
        """
        return {
            "archived_count": len(self.archived_summary),
            "archived_summary": self.archived_summary,
            "recent_steps": [step.to_dict() for step in self.history],
            "total_steps": len(self.archived_summary) + len(self.history),
            "key_insights": self._extract_key_insights()
        }
    
    def _extract_key_insights(self) -> List[str]:
        """Extract all key insights from history."""
        insights = []
        for step in self.history:
            insights.extend(step.insights)
        return insights
    
    def to_text(self) -> str:
        """
        Convert history to human-readable text format.
        
        Returns:
            Formatted string representation
        """
        lines = ["=== ANALYSIS HISTORY ===", ""]
        
        if self.archived_summary:
            lines.append("📦 ARCHIVED STEPS:")
            for summary in self.archived_summary:
                lines.append(f"  • {summary}")
            lines.append("")
        
        if self.history:
            lines.append("🔍 RECENT STEPS:")
            for step in self.history:
                lines.append(f"\nStep {step.step_number}: {step.action.upper()}")
                lines.append(f"  Description: {step.description}")
                if step.insights:
                    lines.append(f"  Insights:")
                    for insight in step.insights:
                        lines.append(f"    - {insight}")
        
        # Add key insights summary
        key_insights = self._extract_key_insights()
        if key_insights:
            lines.append("\n💡 KEY INSIGHTS SUMMARY:")
            for i, insight in enumerate(key_insights[-5:], 1):  # Last 5 insights
                lines.append(f"  {i}. {insight}")
        
        return "\n".join(lines)
    
    def get_context_for_next_step(self) -> str:
        """
        Generate context string for the next analysis step.
        This is optimized for LLM consumption.
        
        Returns:
            Compressed context string
        """
        context_parts = []
        
        # Add archived summary if exists
        if self.archived_summary:
            context_parts.append(
                f"Previous analysis ({len(self.archived_summary)} steps completed): " +
                " → ".join(self.archived_summary[-3:])  # Last 3 archived
            )
        
        # Add recent steps with more detail
        if self.history:
            recent = []
            for step in self.history[-3:]:  # Last 3 detailed steps
                step_text = f"{step.action}: {step.description}"
                if step.insights:
                    step_text += f" (Found: {step.insights[0]})"  # First insight only
                recent.append(step_text)
            context_parts.append("Recent: " + " → ".join(recent))
        
        # Add key insights
        key_insights = self._extract_key_insights()
        if key_insights:
            context_parts.append(
                f"Key findings: {'; '.join(key_insights[-3:])}"  # Last 3 insights
            )
        
        return " | ".join(context_parts)
    
    def clear_history(self):
        """Clear all history (useful for starting fresh analysis)."""
        self.history.clear()
        self.archived_summary.clear()
    
    def export_full_history(self) -> str:
        """Export complete history as JSON."""
        export_data = {
            "archived_summary": self.archived_summary,
            "recent_steps": [step.to_dict() for step in self.history],
            "export_timestamp": datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2)
    
    def estimate_token_savings(self) -> Dict[str, int]:
        """
        Estimate token savings from compression.
        
        Returns:
            Dictionary with token estimates
        """
        # Full history tokens (if we kept everything)
        full_history_text = ""
        for step in self.history:
            full_history_text += f"Step {step.step_number}: {step.action}\n"
            full_history_text += f"Description: {step.description}\n"
            full_history_text += f"Insights: {', '.join(step.insights)}\n"
            if step.code:
                full_history_text += f"Code:\n{step.code}\n"
            full_history_text += "\n"
        
        full_tokens = len(full_history_text) // 4  # Rough estimate
        
        # Compressed context tokens
        compressed_text = self.get_context_for_next_step()
        compressed_tokens = len(compressed_text) // 4
        
        return {
            "full_history_tokens": full_tokens,
            "compressed_tokens": compressed_tokens,
            "tokens_saved": full_tokens - compressed_tokens,
            "compression_ratio": full_tokens / compressed_tokens if compressed_tokens > 0 else 0
        }
