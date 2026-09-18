import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ml_data_pipeline.exceptions import (
    ConfigError,
    DataValidationError,
    ProcessingError,
)
from src.ml_data_pipeline.pipeline import Pipeline


def show_error(name, action):
    print(f"\n--- {name} ---")

    try:
        action()
    except Exception as error:
        print(f"Error type: {type(error).__name__}")
        print(f"Message: {error}")

        if error.__cause__:
            print(f"Original cause: {type(error.__cause__).__name__}: {error.__cause__}")


def invalid_data():
    Pipeline([]).run(None)


def processing_failure():
    class FailingStep:
        def execute(self, data):
            raise ValueError("unexpected calculation failure")

    Pipeline([FailingStep()]).run(["data"])


def missing_file():
    Pipeline([]).process_file("data/raw/does_not_exist.txt")


def invalid_config():
    raise ConfigError(
        "Configuration validation failed in PipelineConfig: "
        "batch_size must be greater than 0."
    )


if __name__ == "__main__":
    show_error("Data validation failure", invalid_data)
    show_error("Processing failure", processing_failure)
    show_error("Missing file failure", missing_file)
    show_error("Configuration failure", invalid_config)
