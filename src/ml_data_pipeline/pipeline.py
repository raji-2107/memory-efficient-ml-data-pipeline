from abc import ABC, abstractmethod
import logging

from src.ml_data_pipeline.context_manager import managed_resource
from src.ml_data_pipeline.decorators import retry, timeit
from src.ml_data_pipeline.exceptions import (
    PipelineError,
    DataValidationError,
    ProcessingError,
)


class Step(ABC):
    @abstractmethod
    def execute(self, data):
        pass


class NormalizeStep(Step):
    def execute(self, data):
        return [item.strip().lower() for item in data]


class FilterStep(Step):
    def __init__(self, keyword):
        self.keyword = keyword

    def execute(self, data):
        return [item for item in data if self.keyword in item]


class AddPrefixStep(Step):
    def __init__(self, prefix):
        self.prefix = prefix

    def execute(self, data):
        return [f"{self.prefix}{item}" for item in data]


class RemovePrefixStep(Step):
    def __init__(self, prefix):
        self.prefix = prefix

    def execute(self, data):
        return [
            item[len(self.prefix):]
            if item.startswith(self.prefix)
            else item
            for item in data
        ]


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    @timeit
    @retry(max_attempts=3)
    def run(self, data):
        if data is None:
            raise DataValidationError(
                "Input data validation failed in Pipeline.run: "
                "data cannot be None."
            )

        if not isinstance(data, list):
            raise DataValidationError(
                "Input data validation failed in Pipeline.run: "
                f"expected a list, received {type(data).__name__}."
            )

        try:
            result = data

            for step in self.steps:
                result = step.execute(result)

            return result

        except PipelineError:
            raise

        except Exception as error:
            raise ProcessingError(
                "Pipeline processing failed in Pipeline.run: "
                f"{type(error).__name__}: {error}"
            ) from error

    @timeit
    def process_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                with managed_resource(file) as resource:
                    data = [line.strip() for line in resource if line.strip()]

        except FileNotFoundError as error:
            raise DataValidationError(
                "File validation failed in Pipeline.process_file: "
                f"file does not exist: {file_path}"
            ) from error

        except OSError as error:
            raise ProcessingError(
                "File processing failed in Pipeline.process_file: "
                f"could not read '{file_path}': {error}"
            ) from error

        logging.info("Processed file: %s", file_path)
        return self.run(data)
