import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ml_data_pipeline.config import (
    DeviceType,
    PipelineConfig,
    PipelineMode,
)


def test_valid_config():
    config = PipelineConfig(
        data_path="data/raw/sample",
        batch_size=10,
        feature_columns=["name"],
        mode="train",
        device="cpu",
        threshold=0.8,
    )

    assert config.batch_size == 10
    assert config.mode == PipelineMode.TRAIN
    assert config.device == DeviceType.CPU


def test_invalid_batch_size():
    with pytest.raises(ValidationError, match="batch_size"):
        PipelineConfig(
            data_path="data/raw/sample",
            batch_size=0,
            feature_columns=["name"],
            threshold=0.8,
        )


def test_invalid_batch_size_type():
    with pytest.raises(ValidationError, match="batch_size"):
        PipelineConfig(
            data_path="data/raw/sample",
            batch_size="abc",
            feature_columns=["name"],
            threshold=0.8,
        )


def test_nonexistent_data_path():
    with pytest.raises(ValidationError, match="data_path"):
        PipelineConfig(
            data_path="data/raw/not_exist",
            batch_size=10,
            feature_columns=["name"],
            threshold=0.8,
        )


def test_missing_required_threshold():
    with pytest.raises(ValidationError, match="threshold"):
        PipelineConfig(
            data_path="data/raw/sample",
            batch_size=10,
            feature_columns=["name"],
        )


def test_invalid_threshold():
    with pytest.raises(ValidationError, match="threshold"):
        PipelineConfig(
            data_path="data/raw/sample",
            batch_size=10,
            feature_columns=["name"],
            threshold=1.5,
        )


def test_invalid_mode():
    with pytest.raises(ValidationError, match="mode"):
        PipelineConfig(
            data_path="data/raw/sample",
            batch_size=10,
            feature_columns=["name"],
            mode="invalid",
            threshold=0.8,
        )
