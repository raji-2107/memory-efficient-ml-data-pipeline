import csv
from itertools import islice
from pathlib import Path


class CSVLazyIterator:
    def __init__(self, folder_path: str, batch_size: int):
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0")

        self.folder_path = Path(folder_path)
        self.batch_size = batch_size
        self._rows = self._read_rows()

    def _read_rows(self):
        for file_path in self.folder_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == ".csv":
                with file_path.open(
                    mode="r",
                    newline="",
                    encoding="utf-8"
                ) as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        yield row

    def __iter__(self):
        return self

    def __next__(self):
        batch = list(islice(self._rows, self.batch_size))

        if not batch:
            raise StopIteration

        return batch
    