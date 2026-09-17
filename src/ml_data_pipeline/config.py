from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class PipelineMode(str, Enum):
    TRAIN = "train"
    INFERENCE = "inference"


class DeviceType(str, Enum):
    CPU = "cpu"
    GPU = "gpu"


class PipelineConfig(BaseModel):
    data_path: Path
    batch_size: int = Field(gt=0, le=10000)
    feature_columns: list[str]
    mode: PipelineMode = PipelineMode.TRAIN
    device: DeviceType = DeviceType.CPU
    threshold: float = Field(ge=0.0, le=1.0)

    @field_validator("data_path")
    @classmethod
    def validate_data_path(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"data_path does not exist: {value}")

        if not value.is_dir():
            raise ValueError(f"data_path must be a directory: {value}")

        return value
