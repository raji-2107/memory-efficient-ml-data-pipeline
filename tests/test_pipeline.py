import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ml_data_pipeline.pipeline import (
    AddPrefixStep,
    FilterStep,
    NormalizeStep,
    Pipeline,
    RemovePrefixStep,
    Step,
)


def test_step_is_abstract():
    with pytest.raises(TypeError):
        Step()


def test_pipeline_runs_steps_in_sequence():
    data = ["  Apple  ", " Banana ", " Apple Pie "]

    pipeline = Pipeline(
        [
            NormalizeStep(),
            FilterStep("apple"),
            AddPrefixStep("product: "),
        ]
    )

    result = pipeline.run(data)

    assert result == [
        "product: apple",
        "product: apple pie",
    ]


def test_pipeline_can_swap_step_at_runtime():
    pipeline = Pipeline(
        [
            NormalizeStep(),
            AddPrefixStep("product: "),
        ]
    )

    original_result = pipeline.run(["  Apple  ", " Apple Pie "])

    pipeline.steps[1] = RemovePrefixStep("product: ")

    swapped_result = pipeline.run(
        ["product: apple", "product: apple pie"]
    )

    assert original_result == [
        "product: apple",
        "product: apple pie",
    ]

    assert swapped_result == [
        "apple",
        "apple pie",
    ]


def test_filter_step():
    data = ["apple", "banana", "apple pie"]

    step = FilterStep("apple")

    assert step.execute(data) == [
        "apple",
        "apple pie",
    ]


def test_normalize_step():
    data = ["  Apple  ", " BANANA "]

    step = NormalizeStep()

    assert step.execute(data) == [
        "apple",
        "banana",
    ]
