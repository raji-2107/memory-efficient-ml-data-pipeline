class PipelineError(Exception):
    """Base exception for the ML data pipeline."""


class DataValidationError(PipelineError):
    """Raised when input data fails validation."""


class ConfigError(PipelineError):
    """Raised when pipeline configuration is invalid."""


class ProcessingError(PipelineError):
    """Raised when pipeline processing fails."""
