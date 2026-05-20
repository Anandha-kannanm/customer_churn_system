"""Conversion tracking for A/B experiments."""
import json
from datetime import datetime
from pathlib import Path


class MetricsTracker:
    def __init__(self, log_path: Path | None = None):
        self.log_path = log_path or Path(__file__).parent / "experiment_log.jsonl"
        self.events: list[dict] = []

    def track_event(
        self,
        customer_id: str,
        experiment: str,
        variant: str,
        event: str,
        converted: bool = False,
    ) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "customer_id": customer_id,
            "experiment": experiment,
            "variant": variant,
            "event": event,
            "converted": converted,
        }
        self.events.append(entry)
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def conversion_rate(self, experiment: str, variant: str) -> float:
        """Calculate conversion rate from logged events."""
        relevant = [
            e for e in self._load_events()
            if e["experiment"] == experiment and e["variant"] == variant
        ]
        if not relevant:
            return 0.0
        conversions = sum(1 for e in relevant if e.get("converted"))
        return conversions / len(relevant)

    def _load_events(self) -> list[dict]:
        if not self.log_path.exists():
            return self.events
        events = []
        with open(self.log_path) as f:
            for line in f:
                events.append(json.loads(line))
        return events
