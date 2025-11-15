#!/usr/bin/env python3
"""
Feedback Analyzer - Generates dynamic prompts based on outcome data

Analyzes historical success rates and adapts generation strategies:
- Weights issue types by success rate
- Suggests focus areas based on performance
- Generates adaptive prompt guidance for issue generation
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .outcome_tracker import OutcomeTracker, TypeSuccessMetrics


@dataclass
class GenerationGuidance:
    """Guidance for issue generation based on feedback"""
    high_priority_types: List[str]
    low_priority_types: List[str]
    recommended_distribution: Dict[str, float]
    prompt_adjustments: str
    focus_message: str


class FeedbackAnalyzer:
    """Analyzes outcome data and provides adaptive generation guidance"""

    def __init__(self, tracker: OutcomeTracker):
        """
        Initialize feedback analyzer

        Args:
            tracker: OutcomeTracker instance
        """
        self.tracker = tracker

    def get_generation_guidance(self,
                               days: Optional[int] = 30,
                               min_samples: int = 3) -> GenerationGuidance:
        """
        Generate adaptive guidance for issue generation

        Args:
            days: Consider data from last N days (default: 30)
            min_samples: Minimum samples needed for type to be considered

        Returns:
            GenerationGuidance with recommendations
        """
        # Get metrics by type
        metrics = self.tracker.get_type_metrics(days=days)

        if not metrics:
            # No data yet - use default guidance
            return self._default_guidance()

        # Filter types with sufficient samples
        valid_metrics = {
            k: v for k, v in metrics.items()
            if v.total_attempts >= min_samples
        }

        if not valid_metrics:
            return self._default_guidance()

        # Categorize types by success rate
        high_priority, low_priority = self._categorize_types(valid_metrics)

        # Calculate recommended distribution
        distribution = self._calculate_distribution(valid_metrics)

        # Generate prompt adjustments
        prompt_adjustments = self._generate_prompt_adjustments(
            high_priority, low_priority, valid_metrics
        )

        # Generate focus message
        focus_message = self._generate_focus_message(
            high_priority, low_priority, valid_metrics
        )

        return GenerationGuidance(
            high_priority_types=high_priority,
            low_priority_types=low_priority,
            recommended_distribution=distribution,
            prompt_adjustments=prompt_adjustments,
            focus_message=focus_message
        )

    def _categorize_types(self,
                         metrics: Dict[str, TypeSuccessMetrics]
                         ) -> Tuple[List[str], List[str]]:
        """Categorize types into high and low priority based on success rate"""
        # Sort by success rate
        sorted_types = sorted(
            metrics.items(),
            key=lambda x: x[1].success_rate,
            reverse=True
        )

        # High priority: top 60% success rate or >= 70% success
        high_priority = []
        low_priority = []

        for issue_type, metric in sorted_types:
            if metric.success_rate >= 0.7:
                high_priority.append(issue_type)
            elif metric.success_rate < 0.4:
                low_priority.append(issue_type)

        return high_priority, low_priority

    def _calculate_distribution(self,
                               metrics: Dict[str, TypeSuccessMetrics]
                               ) -> Dict[str, float]:
        """
        Calculate recommended issue type distribution based on weights

        Uses dynamic weights from success rates
        """
        total_weight = sum(m.weight for m in metrics.values())

        if total_weight == 0:
            # Equal distribution if no weights
            equal_weight = 1.0 / len(metrics)
            return {k: equal_weight for k in metrics.keys()}

        # Distribute proportionally to weights
        distribution = {
            k: round(v.weight / total_weight, 2)
            for k, v in metrics.items()
        }

        return distribution

    def _generate_prompt_adjustments(self,
                                    high_priority: List[str],
                                    low_priority: List[str],
                                    metrics: Dict[str, TypeSuccessMetrics]
                                    ) -> str:
        """Generate prompt adjustment text for Claude"""
        adjustments = []

        if high_priority:
            hp_list = ", ".join(high_priority)
            adjustments.append(
                f"**PRIORITIZE these issue types** (proven high success rate): {hp_list}"
            )

            # Add specific stats for top performers
            top_performer = max(
                [(t, metrics[t]) for t in high_priority],
                key=lambda x: x[1].success_rate
            )
            type_name, metric = top_performer
            adjustments.append(
                f"  → {type_name}: {metric.success_rate:.0%} success rate "
                f"({metric.merged_count}/{metric.total_attempts} merged)"
            )

        if low_priority:
            lp_list = ", ".join(low_priority)
            adjustments.append(
                f"\n**REDUCE these issue types** (lower success rate): {lp_list}"
            )

        # Add time-based insights
        fast_resolvers = [
            (k, v) for k, v in metrics.items()
            if v.avg_time_to_resolve_minutes
            and v.avg_time_to_resolve_minutes < 60
            and v.success_rate >= 0.5
        ]

        if fast_resolvers:
            fast_type = min(fast_resolvers, key=lambda x: x[1].avg_time_to_resolve_minutes)
            type_name, metric = fast_type
            adjustments.append(
                f"\n**FAST RESOLUTION**: {type_name} issues resolve in "
                f"~{metric.avg_time_to_resolve_minutes:.0f} minutes on average"
            )

        return "\n".join(adjustments) if adjustments else "No specific adjustments needed."

    def _generate_focus_message(self,
                               high_priority: List[str],
                               low_priority: List[str],
                               metrics: Dict[str, TypeSuccessMetrics]
                               ) -> str:
        """Generate a concise focus message for the user"""
        overall = self.tracker.get_overall_stats()

        message_parts = [
            f"📊 Overall success rate: {overall['success_rate']:.0%} "
            f"({overall['resolved_count']}/{overall['total_attempts']} resolved)"
        ]

        if high_priority:
            message_parts.append(
                f"✅ Focus on: {', '.join(high_priority[:3])}"
            )

        if low_priority:
            message_parts.append(
                f"⚠️  Avoid: {', '.join(low_priority[:2])}"
            )

        return " | ".join(message_parts)

    def _default_guidance(self) -> GenerationGuidance:
        """Return default guidance when no data is available"""
        return GenerationGuidance(
            high_priority_types=[],
            low_priority_types=[],
            recommended_distribution={},
            prompt_adjustments="No historical data available. Generating diverse issue types.",
            focus_message="🆕 Building initial data - no feedback available yet"
        )

    def format_metrics_report(self, days: Optional[int] = 30) -> str:
        """
        Format a comprehensive metrics report

        Args:
            days: Consider data from last N days

        Returns:
            Formatted report string
        """
        metrics = self.tracker.get_type_metrics(days=days)
        overall = self.tracker.get_overall_stats()
        recent = self.tracker.get_recent_outcomes(limit=5)

        lines = [
            "="*80,
            "📊 SEEDGPT FEEDBACK LOOP REPORT",
            "="*80,
            "",
            "OVERALL STATISTICS:",
            f"  Total Attempts:     {overall['total_attempts']}",
            f"  Resolved:           {overall['resolved_count']} ({overall['success_rate']:.1%})",
            f"  Merged:             {overall['merged_count']} ({overall['merge_rate']:.1%})",
            f"  Failed:             {overall['failed_count']}",
        ]

        if overall['avg_time_to_resolve_minutes']:
            lines.append(
                f"  Avg Resolution Time: {overall['avg_time_to_resolve_minutes']:.0f} minutes"
            )

        if overall['avg_time_to_merge_minutes']:
            lines.append(
                f"  Avg Merge Time:      {overall['avg_time_to_merge_minutes']:.0f} minutes"
            )

        if metrics:
            lines.extend([
                "",
                "SUCCESS RATE BY TYPE:",
                "-"*80,
            ])

            # Sort by success rate
            sorted_metrics = sorted(
                metrics.items(),
                key=lambda x: x[1].success_rate,
                reverse=True
            )

            for issue_type, metric in sorted_metrics:
                success_bar = "█" * int(metric.success_rate * 20)
                weight_str = f"[weight: {metric.weight:.2f}]"

                lines.append(
                    f"  {issue_type:15} {success_bar:20} {metric.success_rate:>6.1%} "
                    f"({metric.merged_count}/{metric.total_attempts}) {weight_str}"
                )

                if metric.avg_time_to_resolve_minutes:
                    lines.append(
                        f"                  ⏱️  Avg resolution: {metric.avg_time_to_resolve_minutes:.0f}m"
                    )

        if recent:
            lines.extend([
                "",
                "RECENT OUTCOMES:",
                "-"*80,
            ])

            for record in recent:
                status_icon = {
                    'merged': '✅',
                    'resolved': '🔄',
                    'failed': '❌',
                    'pending': '⏳',
                    'closed': '🚫'
                }.get(record['status'], '❓')

                lines.append(
                    f"  {status_icon} #{record['issue_number']:4} [{record['issue_type']:12}] "
                    f"{record['issue_title'][:50]}"
                )

        lines.extend([
            "",
            "="*80,
        ])

        return "\n".join(lines)

    def get_prompt_enhancement(self) -> str:
        """
        Get prompt enhancement text to inject into issue generation

        Returns:
            Text to append to generation prompt
        """
        guidance = self.get_generation_guidance()

        if not guidance.high_priority_types:
            return ""

        enhancement = f"""

## 🎯 ADAPTIVE GENERATION GUIDANCE (Based on Success Rate Feedback)

{guidance.prompt_adjustments}

**Current Success Metrics:**
{guidance.focus_message}

Consider these insights when selecting issue types, but still maintain diversity."""

        return enhancement
