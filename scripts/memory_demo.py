import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ml_data_pipeline.csv_iterator import CSVLazyIterator


def get_object_size(obj):
    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        for key, value in obj.items():
            size += sys.getsizeof(key)
            size += sys.getsizeof(value)

    elif isinstance(obj, list):
        for item in obj:
            size += get_object_size(item)

    return size


def measure_memory(folder_path, batch_size):
    iterator = CSVLazyIterator(folder_path, batch_size)

    batch_count = 0
    row_count = 0
    max_batch_memory = 0

    for batch in iterator:
        batch_count += 1
        row_count += len(batch)

        batch_memory = get_object_size(batch)
        max_batch_memory = max(max_batch_memory, batch_memory)

        del batch

    return batch_count, row_count, max_batch_memory


if __name__ == "__main__":
    test_cases = [
        ("data/raw/test_100", 10),
        ("data/raw/test_10000", 10),
    ]

    for folder, batch_size in test_cases:
        batches, rows, memory = measure_memory(folder, batch_size)

        file_count = 100 if "test_10000" not in folder else 10000

        print(
            f"Files: {file_count} | "
            f"Batches: {batches} | "
            f"Rows: {rows} | "
            f"Maximum batch memory: {memory / 1024:.2f} KB"
        )