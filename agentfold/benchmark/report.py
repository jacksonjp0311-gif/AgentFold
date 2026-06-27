"""Benchmark report — formatted benchmark output."""

from __future__ import annotations

from agentfold.benchmark.runner import BenchmarkRunner, BenchmarkResult


class BenchmarkReport:
    """Generate formatted benchmark reports."""

    def __init__(self, runner: BenchmarkRunner):
        self.runner = runner

    def to_dict(self) -> dict:
        """Return report as dict."""
        results = self.runner.results or self.runner.run_all()
        summary = self.runner.summary()
        return {
            "summary": summary,
            "results": [r.to_dict() for r in results],
        }

    def to_table(self) -> list[dict]:
        """Return results as table rows."""
        results = self.runner.results or self.runner.run_all()
        rows = []
        for r in results:
            rows.append({
                "task_id": r.task_id,
                "passed": "PASS" if r.passed else "FAIL",
                "details": r.details,
            })
        return rows
