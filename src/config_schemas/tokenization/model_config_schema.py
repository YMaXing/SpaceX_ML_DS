from typing import Optional, Any
from hydra.core.config_store import ConfigStore
from dataclasses import dataclass
from omegaconf import MISSING, SI



@dataclass
class ModelConfig:
    _target_: str = MISSING

@dataclass
class BPEModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.BPE"
    vocab_size: Optional[dict[str, int]] = None
    merges: Optional[list[Any]] = None
    cache_capacity: int = 10_000
    dropout: Optional[float] = None
    unk_token: Optional[str] = SI("$(tokenizer.unk_token)")
    fuse_unk: bool = False

@dataclass
class UnigramModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.Unigram"
    vocab: Optional[dict[str, float]] = None

@dataclass
class WordLevelModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.WordLevel"
    vocab: Optional[dict[str, int]] = None
    unk_token: Optional[str] = SI("$(tokenizer.unk_token)")

@dataclass
class WordPieceModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.WordPiece"
    vocab: Optional[dict[str, int]] = None
    unk_token: Optional[str] = SI("$(tokenizer.unk_token)")
    max_input_chars_per_word: Optional[int] = None

def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(name="model_schema", node=ModelConfig)

    cs.store(name="bpe_model_schema", 
             node=BPEModelConfig, 
             group="tokenizer/model")
    
    cs.store(name="unigram_model_schema",
                node=UnigramModelConfig,
                group="tokenizer/model")
    
    cs.store(name="word_level_model_schema",
                node=WordLevelModelConfig,
                group="tokenizer/model")
    
    cs.store(name="word_piece_model_schema",
                node=WordPieceModelConfig,
                group="tokenizer/model")