from dataclasses import dataclass, field
from omegaconf import MISSING
from hydra.core.config_store import ConfigStore


@dataclass
class Config:
    # This is a required field
    field1: int = MISSING
    # This is an optional field
    field2: str = "default_value"
    # This is a field with a default value that can be overridden
    field3: float = 3.14
