"""
ModelTrainer Agent - Automates retraining of pattern detection models
Periodically retrains models based on new campaign feedback.
"""

import json
from typing import Dict, Any, List

class ModelTrainer:
    """Manages ML model training and updates."""

    def __init__(self):
        self.model_version = 1.0
        self.training_data = []
        self.last_trained = None

    def add_training_example(self, pattern_data: Dict[str, Any],
                           success: bool) -> bool:
        """Add a training example to the dataset."""
        example = {
            "data": pattern_data,
            "label": "success" if success else "failure",
            "timestamp": json.dumps({"time": "now"})
        }
        self.training_data.append(example)
        return True

    def retrain(self) -> Dict[str, Any]:
        """Retrain the model with accumulated data."""
        total = len(self.training_data)
        if total < 10:
            return {"status": "insufficient_data", "min_required": 10}

        successes = sum(1 for e in self.training_data if e["label"] == "success")
        success_rate = successes / total

        self.model_version += 0.1
        self.last_trained = json.dumps({"time": "now", "version": self.model_version})

        return {
            "status": "retrained",
            "new_version": self.model_version,
            "success_rate": success_rate,
            "training_examples": total
        }

    def should_retrain(self, campaign_threshold: int = 100) -> bool:
        """Check if retraining is needed based on data volume."""
        return len(self.training_data) >= campaign_threshold

# Example usage
if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.add_training_example({"open": 40, "reply": 18}, True)
    trainer.add_training_example({"open": 15, "reply": 3}, False)
    print(json.dumps(trainer.retrain(), indent=2))
