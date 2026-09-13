import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.ml_data_pipeline.csv_iterator import CSVLazyIterator


def create_csv_file(path, rows):
    with open(path, "w", encoding="utf-8") as file:
        file.write("id,name,score\n")

        for row in rows:
            file.write(f"{row[0]},{row[1]},{row[2]}\n")


def test_iterator_returns_correct_batches(tmp_path):
    csv_file = tmp_path / "students.csv"

    create_csv_file(
        csv_file,
        [
            (1, "Alice", 85),
            (2, "Bob", 90),
            (3, "Charlie", 78),
            (4, "David", 92),
            (5, "Eva", 88),
        ],
    )

    iterator = CSVLazyIterator(tmp_path, 2)

    assert next(iterator) == [
        {"id": "1", "name": "Alice", "score": "85"},
        {"id": "2", "name": "Bob", "score": "90"},
    ]

    assert next(iterator) == [
        {"id": "3", "name": "Charlie", "score": "78"},
        {"id": "4", "name": "David", "score": "92"},
    ]

    assert next(iterator) == [
        {"id": "5", "name": "Eva", "score": "88"},
    ]


def test_iterator_stops_when_data_is_finished(tmp_path):
    csv_file = tmp_path / "students.csv"

    create_csv_file(
        csv_file,
        [
            (1, "Alice", 85),
        ],
    )

    iterator = CSVLazyIterator(tmp_path, 2)

    next(iterator)

    try:
        next(iterator)
        assert False
    except StopIteration:
        assert True


def test_invalid_batch_size(tmp_path):
    try:
        CSVLazyIterator(tmp_path, 0)
        assert False
    except ValueError:
        assert True