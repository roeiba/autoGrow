#!/usr/bin/env python3
"""
Tests for the feedback loop system

Run with: python -m pytest tests/test_feedback_loop.py
"""

import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.outcome_tracker import OutcomeTracker, ResolutionStatus
from utils.feedback_analyzer import FeedbackAnalyzer


def test_outcome_tracking():
    """Test basic outcome tracking"""
    # Use temporary database
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        tracker = OutcomeTracker(db_path=db_path)

        # Record an attempt
        record_id = tracker.record_attempt(
            issue_number=1,
            issue_title="Test issue",
            labels=["feature"],
            status=ResolutionStatus.PENDING
        )

        assert record_id > 0

        # Update to resolved
        tracker.update_status(
            issue_number=1,
            status=ResolutionStatus.RESOLVED,
            pr_number=10,
            files_changed=3
        )

        # Get stats
        stats = tracker.get_overall_stats()
        assert stats['total_attempts'] == 1
        assert stats['resolved_count'] == 1


def test_feedback_analyzer():
    """Test feedback analyzer with sample data"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        tracker = OutcomeTracker(db_path=db_path)

        # Create sample data
        for i in range(5):
            tracker.record_attempt(
                issue_number=i,
                issue_title=f"Feature {i}",
                labels=["feature"]
            )
            tracker.update_status(
                issue_number=i,
                status=ResolutionStatus.MERGED,
                pr_number=100 + i,
                files_changed=2
            )

        for i in range(5, 7):
            tracker.record_attempt(
                issue_number=i,
                issue_title=f"Bug {i}",
                labels=["bug"]
            )
            tracker.update_status(
                issue_number=i,
                status=ResolutionStatus.FAILED,
                error_message="Test failure"
            )

        # Test analyzer
        analyzer = FeedbackAnalyzer(tracker)
        guidance = analyzer.get_generation_guidance()

        # Features should be high priority (100% success)
        assert "feature" in guidance.high_priority_types

        # Check distribution - features should have higher weight
        assert guidance.recommended_distribution.get("feature", 0) > 0
        assert guidance.recommended_distribution.get("feature", 0) > guidance.recommended_distribution.get("bug", 0)

        # Verify metrics
        metrics = tracker.get_type_metrics()
        assert metrics["feature"].success_rate == 1.0
        assert metrics["bug"].success_rate == 0.0


def test_type_classification():
    """Test issue type classification"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        tracker = OutcomeTracker(db_path=db_path)

        # Test various label combinations
        test_cases = [
            (["feature"], "feature"),
            (["bug"], "bug"),
            (["documentation"], "documentation"),
            (["security", "bug"], "security"),  # Security has priority
            (["enhancement"], "feature"),  # Enhancement maps to feature
            (["random"], "other"),  # Unknown label
        ]

        for labels, expected_type in test_cases:
            issue_type = tracker._classify_issue_type(labels)
            assert issue_type == expected_type, f"Expected {expected_type} for {labels}, got {issue_type}"


def test_weight_calculation():
    """Test weight calculation logic"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        tracker = OutcomeTracker(db_path=db_path)

        # Test various scenarios
        # 100% success, 5 samples -> high weight
        weight_100 = tracker._calculate_weight(1.0, 5)
        assert weight_100 > 1.5

        # 50% success, 5 samples -> medium weight
        weight_50 = tracker._calculate_weight(0.5, 5)
        assert 0.5 < weight_50 < 1.5

        # 0% success, 5 samples -> low weight
        weight_0 = tracker._calculate_weight(0.0, 5)
        assert weight_0 < 0.5

        # Higher success should always have higher weight
        assert weight_100 > weight_50 > weight_0

        # Low sample size should reduce weight
        weight_low_samples = tracker._calculate_weight(1.0, 1)
        assert weight_low_samples < weight_100


def test_metrics_export():
    """Test JSON export of metrics"""
    import json

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        tracker = OutcomeTracker(db_path=db_path)

        # Add sample data
        tracker.record_attempt(1, "Test", ["feature"])
        tracker.update_status(1, ResolutionStatus.RESOLVED, pr_number=1)

        # Export
        export = tracker.export_metrics_json()
        data = json.loads(export)

        # Verify structure
        assert 'generated_at' in data
        assert 'overall_stats' in data
        assert 'type_metrics' in data
        assert 'recent_outcomes' in data

        # Verify content
        assert data['overall_stats']['total_attempts'] == 1
        assert len(data['recent_outcomes']) == 1


if __name__ == "__main__":
    print("Running feedback loop tests...")
    test_outcome_tracking()
    print("✅ test_outcome_tracking passed")

    test_feedback_analyzer()
    print("✅ test_feedback_analyzer passed")

    test_type_classification()
    print("✅ test_type_classification passed")

    test_weight_calculation()
    print("✅ test_weight_calculation passed")

    test_metrics_export()
    print("✅ test_metrics_export passed")

    print("\n🎉 All tests passed!")
