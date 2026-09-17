from abc import ABC, abstractmethod


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

    def run(self, data):
        result = data

        for step in self.steps:
            result = step.execute(result)

        return result
