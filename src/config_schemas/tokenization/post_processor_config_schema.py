from typing import Optional, Any
from hydra.core.config_store import ConfigStore
from dataclasses import dataclass, field
from omegaconf import MISSING, SI



@dataclass
class PostProcessorConfig:
    _target_: str = MISSING

@dataclass
class BertPostProcessorConfig(PostProcessorConfig):
    _target_: str = "tokenizers.processors.BertProcessing"
    sep: tuple[str, int] = MISSING
    cls: tuple[str, int] = MISSING

@dataclass
class ByteLevelPostProcessorConfig(PostProcessorConfig):
    _target_: str = "tokenizers.processors.ByteLevel"
    trim_offsets: bool = True

@dataclass
class RobertaPostProcessorConfig(PostProcessorConfig):
    _target_: str = "tokenizers.processors.RobertaProcessing"
    sep: tuple[str, int] = MISSING
    cls: tuple[str, int] = MISSING
    trim_offsets: bool = True
    add_prefix_space: bool = True

def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(name="post_processor_schema", node=PostProcessorConfig)

    cs.store(name="bert_post_processor_schema", 
             node=BertPostProcessorConfig,
             group="tokenizer/post_processor")
      
    cs.store(name="post_processor_schema", 
             node=PostProcessorConfig,
             group="tokenizer/post_processor")
    
    cs.store(name="byte_level_post_processor_schema",
                node=ByteLevelPostProcessorConfig,
                group="tokenizer/post_processor")
    
    cs.store(name="roberta_post_processor_schema",
                node=RobertaPostProcessorConfig,
                group="tokenizer/post_processor")