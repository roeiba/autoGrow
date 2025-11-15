#!/usr/bin/env python3
"""
Outcome Tracker - Persistent feedback loop for issue resolution success

Tracks:
- Issue resolution outcomes (resolved, failed, timeout)
- PR merge status (merged, closed, pending)
- Time to resolution
- Issue type success rates

Enables the system to learn what works and adapt generation prompts dynamically.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ResolutionStatus(Enum):
    """Status of issue resolution attempt"""
    PENDING = "pending"
    RESOLVED = "resolved"  # PR created
    MERGED = "merged"      # PR merged
    CLOSED = "closed"      # PR closed without merge
    FAILED = "failed"      # Failed to create PR
    TIMEOUT = "timeout"    # Took too long


class IssueType(Enum):
    """Categorization of issues"""
    FEATURE = "feature"
    BUG = "bug"
    DOCUMENTATION = "documentation"
    REFACTOR = "refactor"
    TEST = "test"
    PERFORMANCE = "performance"
    SECURITY = "security"
    CI_CD = "ci/cd"
    OTHER = "other"


@dataclass
class OutcomeRecord:
    """Record of a single issue resolution attempt"""
    issue_number: int
    issue_title: str
    issue_type: str
    labels: str  # JSON array of labels
    status: str
    pr_number: Optional[int] = None
    created_at: str = ""
    resolved_at: Optional[str] = None
    merged_at: Optional[str] = None
    time_to_resolve_minutes: Optional[int] = None
    time_to_merge_minutes: Optional[int] = None
    files_changed: int = 0
    error_message: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()


@dataclass
class TypeSuccessMetrics:
    """Success metrics for a specific issue type"""
    issue_type: str
    total_attempts: int
    resolved_count: int
    merged_count: int
    failed_count: int
    success_rate: float
    merge_rate: float
    avg_time_to_resolve_minutes: Optional[float]
    avg_time_to_merge_minutes: Optional[float]
    weight: float  # Dynamic weight based on success rate


class OutcomeTracker:
    """Tracks issue resolution outcomes and provides analytics"""

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize outcome tracker

        Args:
            db_path: Path to SQLite database (defaults to .seedgpt/outcomes.db)
        """
        if db_path is None:
            db_path = Path.cwd() / ".seedgpt" / "outcomes.db"

        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main outcomes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_number INTEGER NOT NULL,
                issue_title TEXT NOT NULL,
                issue_type TEXT NOT NULL,
                labels TEXT NOT NULL,
                status TEXT NOT NULL,
                pr_number INTEGER,
                created_at TEXT NOT NULL,
                resolved_at TEXT,
                merged_at TEXT,
                time_to_resolve_minutes INTEGER,
                time_to_merge_minutes INTEGER,
                files_changed INTEGER DEFAULT 0,
                error_message TEXT,
                updated_at TEXT NOT NULL
            )
        """)

        # Index for fast lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_issue_number
            ON outcomes(issue_number)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_issue_type
            ON outcomes(issue_type)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status
            ON outcomes(status)
        """)

        conn.commit()
        conn.close()

    def record_attempt(self,
                      issue_number: int,
                      issue_title: str,
                      labels: List[str],
                      status: ResolutionStatus = ResolutionStatus.PENDING) -> int:
        """
        Record a new issue resolution attempt

        Args:
            issue_number: GitHub issue number
            issue_title: Issue title
            labels: List of issue labels
            status: Initial status (default: PENDING)

        Returns:
            Database record ID
        """
        # Determine issue type from labels
        issue_type = self._classify_issue_type(labels)

        record = OutcomeRecord(
            issue_number=issue_number,
            issue_title=issue_title,
            issue_type=issue_type,
            labels=json.dumps(labels),
            status=status.value
        )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO outcomes
            (issue_number, issue_title, issue_type, labels, status,
             created_at, updated_at, files_changed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.issue_number,
            record.issue_title,
            record.issue_type,
            record.labels,
            record.status,
            record.created_at,
            now,
            record.files_changed
        ))

        record_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return record_id

    def update_status(self,
                     issue_number: int,
                     status: ResolutionStatus,
                     pr_number: Optional[int] = None,
                     files_changed: Optional[int] = None,
                     error_message: Optional[str] = None):
        """
        Update the status of an issue resolution attempt

        Args:
            issue_number: GitHub issue number
            status: New status
            pr_number: PR number if created
            files_changed: Number of files changed
            error_message: Error message if failed
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the existing record
        cursor.execute("""
            SELECT created_at FROM outcomes
            WHERE issue_number = ?
            ORDER BY created_at DESC LIMIT 1
        """, (issue_number,))

        result = cursor.fetchone()
        if not result:
            conn.close()
            return

        created_at = datetime.fromisoformat(result[0])
        now = datetime.utcnow()
        updated_at = now.isoformat()

        # Calculate time to resolve
        time_to_resolve = None
        resolved_at = None
        if status in [ResolutionStatus.RESOLVED, ResolutionStatus.MERGED]:
            resolved_at = updated_at
            time_to_resolve = int((now - created_at).total_seconds() / 60)

        # Calculate time to merge
        time_to_merge = None
        merged_at = None
        if status == ResolutionStatus.MERGED:
            merged_at = updated_at
            time_to_merge = int((now - created_at).total_seconds() / 60)

        # Build update query
        update_fields = [
            "status = ?",
            "updated_at = ?"
        ]
        params = [status.value, updated_at]

        if pr_number is not None:
            update_fields.append("pr_number = ?")
            params.append(pr_number)

        if files_changed is not None:
            update_fields.append("files_changed = ?")
            params.append(files_changed)

        if resolved_at is not None:
            update_fields.append("resolved_at = ?")
            update_fields.append("time_to_resolve_minutes = ?")
            params.extend([resolved_at, time_to_resolve])

        if merged_at is not None:
            update_fields.append("merged_at = ?")
            update_fields.append("time_to_merge_minutes = ?")
            params.extend([merged_at, time_to_merge])

        if error_message is not None:
            update_fields.append("error_message = ?")
            params.append(error_message)

        params.append(issue_number)

        cursor.execute(f"""
            UPDATE outcomes
            SET {', '.join(update_fields)}
            WHERE issue_number = ?
        """, params)

        conn.commit()
        conn.close()

    def get_type_metrics(self,
                        days: Optional[int] = None) -> Dict[str, TypeSuccessMetrics]:
        """
        Get success metrics grouped by issue type

        Args:
            days: Only consider records from last N days (default: all time)

        Returns:
            Dictionary mapping issue type to metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build date filter
        date_filter = ""
        params = []
        if days is not None:
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
            date_filter = "WHERE created_at >= ?"
            params.append(cutoff)

        # Query for aggregated metrics by type
        cursor.execute(f"""
            SELECT
                issue_type,
                COUNT(*) as total_attempts,
                SUM(CASE WHEN status IN ('resolved', 'merged') THEN 1 ELSE 0 END) as resolved_count,
                SUM(CASE WHEN status = 'merged' THEN 1 ELSE 0 END) as merged_count,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_count,
                AVG(CASE WHEN time_to_resolve_minutes IS NOT NULL THEN time_to_resolve_minutes END) as avg_resolve_time,
                AVG(CASE WHEN time_to_merge_minutes IS NOT NULL THEN time_to_merge_minutes END) as avg_merge_time
            FROM outcomes
            {date_filter}
            GROUP BY issue_type
        """, params)

        metrics = {}
        for row in cursor.fetchall():
            (issue_type, total, resolved, merged, failed,
             avg_resolve, avg_merge) = row

            # Calculate success and merge rates
            success_rate = resolved / total if total > 0 else 0.0
            merge_rate = merged / total if total > 0 else 0.0

            # Calculate dynamic weight based on success rate
            # Higher success rate = higher weight
            # Use exponential scaling to emphasize successful types
            weight = self._calculate_weight(success_rate, total)

            metrics[issue_type] = TypeSuccessMetrics(
                issue_type=issue_type,
                total_attempts=total,
                resolved_count=resolved,
                merged_count=merged,
                failed_count=failed,
                success_rate=success_rate,
                merge_rate=merge_rate,
                avg_time_to_resolve_minutes=avg_resolve,
                avg_time_to_merge_minutes=avg_merge,
                weight=weight
            )

        conn.close()
        return metrics

    def get_recent_outcomes(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent outcome records

        Args:
            limit: Maximum number of records to return

        Returns:
            List of outcome records as dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                issue_number, issue_title, issue_type, labels, status,
                pr_number, created_at, resolved_at, merged_at,
                time_to_resolve_minutes, time_to_merge_minutes,
                files_changed, error_message
            FROM outcomes
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        columns = [
            'issue_number', 'issue_title', 'issue_type', 'labels', 'status',
            'pr_number', 'created_at', 'resolved_at', 'merged_at',
            'time_to_resolve_minutes', 'time_to_merge_minutes',
            'files_changed', 'error_message'
        ]

        results = []
        for row in cursor.fetchall():
            record = dict(zip(columns, row))
            # Parse labels JSON
            record['labels'] = json.loads(record['labels'])
            results.append(record)

        conn.close()
        return results

    def get_overall_stats(self) -> Dict:
        """Get overall statistics across all issue types"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status IN ('resolved', 'merged') THEN 1 ELSE 0 END) as resolved,
                SUM(CASE WHEN status = 'merged' THEN 1 ELSE 0 END) as merged,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                AVG(CASE WHEN time_to_resolve_minutes IS NOT NULL THEN time_to_resolve_minutes END) as avg_resolve_time,
                AVG(CASE WHEN time_to_merge_minutes IS NOT NULL THEN time_to_merge_minutes END) as avg_merge_time
            FROM outcomes
        """)

        row = cursor.fetchone()
        total, resolved, merged, failed, avg_resolve, avg_merge = row

        stats = {
            'total_attempts': total or 0,
            'resolved_count': resolved or 0,
            'merged_count': merged or 0,
            'failed_count': failed or 0,
            'success_rate': (resolved / total) if total > 0 else 0.0,
            'merge_rate': (merged / total) if total > 0 else 0.0,
            'avg_time_to_resolve_minutes': avg_resolve,
            'avg_time_to_merge_minutes': avg_merge
        }

        conn.close()
        return stats

    def _classify_issue_type(self, labels: List[str]) -> str:
        """Classify issue type from labels"""
        label_lower = [l.lower() for l in labels]

        # Priority order for classification
        type_map = {
            'security': IssueType.SECURITY,
            'bug': IssueType.BUG,
            'performance': IssueType.PERFORMANCE,
            'ci/cd': IssueType.CI_CD,
            'ci-cd': IssueType.CI_CD,
            'test': IssueType.TEST,
            'documentation': IssueType.DOCUMENTATION,
            'docs': IssueType.DOCUMENTATION,
            'refactor': IssueType.REFACTOR,
            'refactoring': IssueType.REFACTOR,
            'feature': IssueType.FEATURE,
            'enhancement': IssueType.FEATURE,
        }

        for label in label_lower:
            for key, issue_type in type_map.items():
                if key in label:
                    return issue_type.value

        return IssueType.OTHER.value

    def _calculate_weight(self, success_rate: float, sample_size: int) -> float:
        """
        Calculate dynamic weight for issue type based on success rate

        Uses exponential scaling with confidence adjustment based on sample size

        Args:
            success_rate: Success rate (0.0 to 1.0)
            sample_size: Number of attempts

        Returns:
            Weight value (0.0 to 2.0+)
        """
        # Minimum sample size for full confidence
        min_confidence_samples = 5

        # Confidence factor (0.0 to 1.0)
        # Lower sample sizes reduce the weight
        confidence = min(1.0, sample_size / min_confidence_samples)

        # Exponential scaling: 0% = 0.1, 50% = 1.0, 100% = 2.0+
        # e^(rate * 1.5) provides good exponential curve
        import math
        base_weight = math.exp(success_rate * 1.5) / math.e  # Normalize

        # Apply confidence adjustment
        adjusted_weight = base_weight * confidence + (1 - confidence) * 0.5

        return round(adjusted_weight, 2)

    def export_metrics_json(self) -> str:
        """Export metrics as JSON string"""
        metrics = self.get_type_metrics()
        overall = self.get_overall_stats()
        recent = self.get_recent_outcomes(limit=5)

        export_data = {
            'generated_at': datetime.utcnow().isoformat(),
            'overall_stats': overall,
            'type_metrics': {
                k: asdict(v) for k, v in metrics.items()
            },
            'recent_outcomes': recent
        }

        return json.dumps(export_data, indent=2)
