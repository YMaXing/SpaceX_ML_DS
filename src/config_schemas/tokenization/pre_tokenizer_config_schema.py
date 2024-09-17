from typing import Optional, Any
from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass
from pydantic import validator
from dataclasses import field
from omegaconf import MISSING, SI

from src.utils.schema_utils import validate_config_parameter_is_in

SPLIT_DELIMITER_BEHAVIOR_OPTIONS = {"removed", "isolated", "merged_with_previous", "merged_with_next", "contiguous"}

@dataclass
class PreTokenizerConfig:
    _target_: str = MISSING

@dataclass
class BertPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.BertPreTokenizer"

@dataclass
class ByteLevelPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.ByteLevelPreTokenizer"

@dataclass
class CharDelimiterSplitPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.CharDelimiterSplit"

@dataclass
class DigitsPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Digits"
    individual_digits: bool = False

@dataclass
class MetaspacePreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Metaspace"
    replacement: str = "▁"
    add_prefix_space: bool = True

@dataclass
class PunctuationPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Punctuation"

    @validator("behavior")
    def validate_behavior(cls, behavior: str):
        validate_config_parameter_is_in(SPLIT_DELIMITER_BEHAVIOR_OPTIONS, behavior, "behavior")
        return behavior

@dataclass
class SequencePreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Sequence"
    pre_tokenizers: list[PreTokenizerConfig] = field(default_factory=lambda: [])
    _pretokenizers_dict: dict[str, PreTokenizerConfig] = field(default_factory=lambda: {}) 

@dataclass
class SplitPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Split"
    pattern: str = MISSING
    behavior: str = MISSING
    invert: bool = False

    @validator("behavior")
    def validate_behavior(cls, behavior: str):
        validate_config_parameter_is_in(SPLIT_DELIMITER_BEHAVIOR_OPTIONS, behavior, "behavior")
        return behavior

@dataclass
class UnicodeScriptsPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.UnicodeScripts"

@dataclass
class WhitespacePreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.Whitespace"

@dataclass
class WhitespaceSplitPreTokenizerConfig(PreTokenizerConfig):
    _target_: str = "tokenizers.pre_tokenizers.WhitespaceSplit"

def setup_config() -> None:
    cs = ConfigStore.instance()
    
    cs.store(name="pre_tokenizer_schema", node=PreTokenizerConfig)

    cs.store(name="bert_pre_tokenizer_schema", 
             node=BertPreTokenizerConfig,
             group="tokenizer/pre_tokenizer")
    
    cs.store(name="byte_level_pre_tokenizer_schema",
                node=ByteLevelPreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="char_delimiter_split_pre_tokenizer_schema",
                node=CharDelimiterSplitPreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="digits_pre_tokenizer_schema",
                node=DigitsPreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="metaspace_pre_tokenizer_schema",
                node=MetaspacePreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="punctuation_pre_tokenizer_schema",
                node=PunctuationPreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="sequence_pre_tokenizer_schema",
                node=SequencePreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="split_pre_tokenizer_schema",
                node=SplitPreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="unicode_scripts_pre_tokenizer_schema",
                node=UnicodeScriptsPreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="whitespace_pre_tokenizer_schema",
                node=WhitespacePreTokenizerConfig,
                group="tokenizer/pre_tokenizer")
    
    cs.store(name="whitespace_split_pre_tokenizer_schema",
                node=WhitespaceSplitPreTokenizerConfig,
                group="tokenizer/pre_tokenizer")