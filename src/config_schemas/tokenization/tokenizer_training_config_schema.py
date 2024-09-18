from dataclasses import dataclass, field
from omegaconf import MISSING
from hydra.core.config_store import ConfigStore

from src.config_schemas.infrastructure import gcp_config_schema
from src.config_schemas.tokenization import tokenizer_config_schema


@dataclass
class TokenizerTrainingConfig:
    docker_image_name: str = MISSING
    docker_image_tag: str = MISSING

    data_parquet_path: str = MISSING
    text_column_name: str = MISSING

    tokenizer: tokenizer_config_schema.TokenizerConfig = MISSING

    infrastructure: gcp_config_schema.GCP_Config = field(default_factory=gcp_config_schema.GCP_Config)


def setup_config() -> None:
    gcp_config_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="tokenizer_training_schema", node=TokenizerTrainingConfig)
