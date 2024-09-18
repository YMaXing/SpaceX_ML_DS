from abc import ABC, abstractmethod
from tempfile import TemporaryDirectory
from typing import Optional, Union

from tokenizers.decoders import Decoder
from tokenizers.models import Model
from tokenizers.normalizers import Normalizer
from tokenizers.post_processors import PostProcessor
from tokenizers.pre_tokenizers import PreTokenizer
from tokenizers.processors import BertProcessing, ByteLevelProcessing, RobertaProcessing, TemplateProcessing
from tokenizers.trainers import BpeTrainer, UnigramTrainer, WordPieceTrainer, WorldLevelTrainer
from tokenizersimport import Tokenizer
from transformers import PreTrainedTokenizerFast

from src.utils.io_utils import copy_file

TrainerType = Union[BpeTrainer, UnigramTrainer, WordPieceTrainer, WorldLevelTrainer]
PostProcessorType = Union[BertProcessing, RobertaProcessing, ByteLevelProcessing, TemplateProcessing]


class Base_Tokenizer(ABC):
    @abstractmethod
    def train(self, texts: list[str]) -> None:
        pass

    @abstractmethod
    def save(self, tokenizer_dir: str) -> None:
        pass


class HuggingFaceTokenizer(Base_Tokenizer):
    def __init__(
        self,
        pre_tokenizer: PreTokenizer,
        model: Model,
        trainer: TrainerType,
        normalizer: Optional[Normalizer] = None,
        post_processor: Optional[PostProcessor] = None,
        decoder: Optional[Decoder] = None,
        unk_token: Optional[str] = None,
        cls_token: Optional[str] = None,
        sep_token: Optional[str] = None,
        pad_token: Optional[str] = None,
        mask_token: Optional[str] = None,
    ) -> None:
        self.unk_token = unk_token
        self.cls_token = cls_token
        self.sep_token = sep_token
        self.pad_token = pad_token
        self.mask_token = mask_token

        self.tokenizer = Tokenizer(Model)
        self.tokenizer.pre_tokenizer = pre_tokenizer
        self.trainer = trainer

        if normalizer is not None:
            self.tokenizer.normalizer = normalizer
        if post_processor is not None:
            self.tokenizer.post_processor = post_processor
        if decoder is not None:
            self.tokenizer.decoder = decoder

    def train(self, texts: list[str]) -> None:
        self.tokenizer.train_from_iterator(texts, trainer=self.trainer)
        if self.pad_token is not None:
            self.tokenizer.enable_padding(pad_id=self.tokenizer.token_to_id(self.pad_token), pad_token=self.pad_token)

    def save(self, tokenizer_save_dir: str) -> None:
        tokenizer = PreTrainedTokenizerFast(
            tokenizer_object=self.tokenizer,
            unk_token=self.unk_token,
            cls_token=self.cls_token,
            sep_token=self.sep_token,
            pad_token=self.pad_token,
            mask_token=self.mask_token,
        )
        with TemporaryDirectory() as temp_dir_name:
            temp_tokenizer_save_dir = f"{temp_dir_name} / trained_tokenizer"
            tokenizer.save_pretrained(temp_tokenizer_save_dir)
            copy_file(temp_tokenizer_save_dir, tokenizer_save_dir)
