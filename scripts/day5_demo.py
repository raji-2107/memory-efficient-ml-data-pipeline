import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ml_data_pipeline.pipeline import NormalizeStep, Pipeline


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


class UnstableStep(NormalizeStep):
    def __init__(self):
        self.attempts = 0

    def execute(self, data):
        self.attempts += 1

        if self.attempts < 2:
            raise ValueError("Temporary pipeline failure")

        return super().execute(data)


if __name__ == "__main__":
    pipeline = Pipeline(
        [
            UnstableStep(),
        ]
    )

    result = pipeline.run([" Apple ", " Banana "])

    print("Pipeline result:", result)
