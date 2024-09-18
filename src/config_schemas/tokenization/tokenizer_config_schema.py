from dataclasses import field
from tokenize import group
from typing import Any, Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from pydantic import validator
from pydantic.dataclasses import dataclass

import src.config_schemas.tokenization.decoder_config_schema as decoder_schemas
import src.config_schemas.tokenization.model_config_schema as model_schemas
import src.config_schemas.tokenization.normalizer_config_schema as normalizer_schemas
import src.config_schemas.tokenization.post_processor_config_schema as post_processor_schemas
import src.config_schemas.tokenization.pre_tokenizer_config_schema as pre_tokenizer_schemas
import src.config_schemas.tokenization.trainer_config_schema as trainer_schemas


@dataclass
class TokenizerConfig:
    _target_: str = MISSING


@dataclass
class HuggingFaceTokenizerConfig(TokenizerConfig):
    _target_: str = "src.tokenization.tokenizer.HuggingFaceTokenizer"
    pre_tokenizer: pre_tokenizer_schemas.PreTokenizerConfig = MISSING
    trainer: trainer_schemas.TrainerConfig = MISSING
    model: model_schemas.ModelConfig = MISSING
    normalizer: Optional[normalizer_schemas.NormalizerConfig] = None
    post_processor: Optional[post_processor_schemas.PostProcessorConfig] = None
    decoder: Optional[decoder_schemas.DecoderConfig] = None

    unk_token: Optional[str] = "[UNK]"
    cls_token: Optional[str] = "[CLS]"
    sep_token: Optional[str] = "[SEP]"
    pad_token: Optional[str] = "[PAD]"
    mask_token: Optional[str] = "[MASK]"


def setup_config() -> None:
    decoder_schemas.setup_config()
    normalizer_schemas.setup_config()
    pre_tokenizer_schemas.setup_config()
    post_processor_schemas.setup_config()
    decoder_schemas.setup_config()
    model_schemas.setup_config()
    trainer_schemas.setup_config()

    cs = ConfigStore.instance()

    cs.store(name="huggingface_tokenizer_schema", node=HuggingFaceTokenizerConfig, group="tokenizer")
