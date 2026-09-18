import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ml_data_pipeline.exceptions import (
    ConfigError,
    DataValidationError,
    PipelineError,
    ProcessingError,
)
from src.ml_data_pipeline.pipeline import Pipeline


def test_exception_hierarchy():
    assert issubclass(DataValidationError, PipelineError)
    assert issubclass(ConfigError, PipelineError)
    assert issubclass(ProcessingError, PipelineError)


def test_data_validation_error():
    pipeline = Pipeline([])

    with pytest.raises(DataValidationError, match="data cannot be None"):
        pipeline.run(None)


def test_data_validation_error_for_wrong_type():
    pipeline = Pipeline([])

    with pytest.raises(DataValidationError, match="expected a list"):
        pipeline.run("invalid data")


def test_processing_error_with_exception_chaining():
    class FailingStep:
        def execute(self, data):
            raise ValueError("step calculation failed")

    pipeline = Pipeline([FailingStep()])

    with pytest.raises(ProcessingError, match="Pipeline processing failed"):
        pipeline.run(["data"])

    try:
        pipeline.run(["data"])
    except ProcessingError as error:
        assert isinstance(error.__cause__, ValueError)
        assert str(error.__cause__) == "step calculation failed"


def test_missing_file_raises_data_validation_error():
    pipeline = Pipeline([])

    with pytest.raises(DataValidationError, match="file does not exist"):
        pipeline.process_file("data/raw/does_not_exist.txt")
