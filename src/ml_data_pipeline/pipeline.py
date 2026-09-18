from abc import ABC, abstractmethod
import logging

from src.ml_data_pipeline.context_manager import managed_resource
from src.ml_data_pipeline.decorators import retry, timeit


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
        result = data

        for step in self.steps:
            result = step.execute(result)

        return result

    @timeit
    def process_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            with managed_resource(file) as resource:
                data = [line.strip() for line in resource if line.strip()]

        logging.info("Processed file: %s", file_path)
        return self.run(data)
