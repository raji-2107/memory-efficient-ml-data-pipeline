import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))




from pydantic import ValidationError

from src.ml_data_pipeline.config import PipelineConfig


configs = [
    (
        "Invalid batch size",
        {
            "data_path": "data/raw/sample",
            "batch_size": 0,
            "feature_columns": ["name"],
            "threshold": 0.8,
        },
    ),
    (
        "Non-existent data path",
        {
            "data_path": "data/raw/not_exist",
            "batch_size": 10,
            "feature_columns": ["name"],
            "threshold": 0.8,
        },
    ),
    (
        "Invalid batch size type",
        {
            "data_path": "data/raw/sample",
            "batch_size": "abc",
            "feature_columns": ["name"],
            "threshold": 0.8,
        },
    ),
]


for name, config_data in configs:
    print(f"\n--- {name} ---")

    try:
        PipelineConfig(**config_data)
    except ValidationError as error:
        print(error)
