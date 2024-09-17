from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass
from omegaconf import MISSING
from pydantic import validator



@dataclass
class DecoderConfig:
    _target_: str = MISSING

@dataclass
class BPEDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoder.BPEDecoder"
    suffix: str = "</w>"

@dataclass
class ByteLevelDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoder.ByteLevel"

@dataclass
class CTCDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoder.CTC"
    pad_token: str = "<pad>"
    word_delimiter_token: str = "|"
    cleanup: bool = True

@dataclass
class MetaspaceDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoder.Metaspace"
    replacement: str = "▁"
    add_prefix_space: bool = True

    @validator("replacement")
    def validate_replacement(cls, replacement: str):
        if len(replacement) > 1:
            raise ValueError(f"{len(replacement)} must be 1, got: {len(replacement)}")
        return replacement

@dataclass
class WordPieceDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoder.WordPiece"
    prefix: str = "##"
    cleanup: bool = True

def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(name="bpe_decoder_schema", 
             node=BPEDecoderConfig,
             group="tokenizer/decoder")
    
    cs.store(name="byte_level_bpe_decoder_schema",
            node=ByteLevelDecoderConfig,
            group="tokenizer/decoder")
    
    cs.store(name="ctc_decoder_schema",
            node=CTCDecoderConfig,
            group="tokenizer/decoder")
    
    cs.store(name="metaspace_decoder_schema",
            node=MetaspaceDecoderConfig,
            group="tokenizer/decoder")
    
    cs.store(name="word_piece_decoder_schema",
            node=WordPieceDecoderConfig,
            group="tokenizer/decoder")
    
    cs.store(name="tokenizer/decoder_schema",
            node=DecoderConfig)