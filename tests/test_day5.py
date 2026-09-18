import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ml_data_pipeline.context_manager import managed_resource
from src.ml_data_pipeline.decorators import retry, timeit


def test_timeit_preserves_function_metadata():
    @timeit
    def sample_function():
        """Sample function."""
        return "done"

    assert sample_function() == "done"
    assert sample_function.__name__ == "sample_function"
    assert sample_function.__doc__ == "Sample function."


def test_retry_succeeds_after_failures():
    attempts = {"count": 0}

    @retry(max_attempts=3)
    def unstable_function():
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise ValueError("temporary failure")

        return "success"

    assert unstable_function() == "success"
    assert attempts["count"] == 3


def test_retry_raises_after_max_attempts():
    attempts = {"count": 0}

    @retry(max_attempts=3)
    def failing_function():
        attempts["count"] += 1
        raise ValueError("permanent failure")

    with pytest.raises(ValueError, match="permanent failure"):
        failing_function()

    assert attempts["count"] == 3


def test_retry_rejects_invalid_attempt_count():
    with pytest.raises(ValueError, match="greater than 0"):
        retry(max_attempts=0)


def test_context_manager_closes_resource():
    class TestResource:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    resource = TestResource()

    with managed_resource(resource) as active_resource:
        assert active_resource is resource
        assert not resource.closed

    assert resource.closed


def test_context_manager_closes_resource_on_exception():
    class TestResource:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    resource = TestResource()

    with pytest.raises(RuntimeError):
        with managed_resource(resource):
            raise RuntimeError("test failure")

    assert resource.closed
