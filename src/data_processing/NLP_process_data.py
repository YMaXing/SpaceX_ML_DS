import re
import string

from abc import ABC, abstractmethod
from cgitb import text
from dataclasses import dataclass
from sys import flags
from xmlrpc.client import Boolean

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from src.config_schemas.data_processing.data_processing_config_schema import Config
from src.utils.config_utils import get_config
from src.utils.NLP_utils import SpellingCorrectionModel


class DatasetCleaner(ABC):
    def __call__(self, text: list[str]) -> list[str]:
        if isinstance(text, str):
            return self.clean_text(text)
        return self.clean_words(text)

    @abstractmethod
    def clean_text(self, text: str) -> str:
        """
        Clean the given text(string).
        """

    @abstractmethod
    def clean_words(self, words: list[str]) -> list[str]:
        """
        Clean each word in a list of words.
        """


class StopwordsDatasetCleaner(DatasetCleaner):
    def __init__(self) -> None:
        super().__init__()
        self.stopwords = set(stopwords.words("english"))

    def clean_text(self, text: str) -> str:
        cleaned_text = " ".join([word for word in word_tokenize(text) if word.lower() not in self.stopwords])
        return cleaned_text

    def clean_words(self, words: list[str]) -> list[str]:
        cleaned_words = [word for word in words if word.lower() not in self.stopwords]
        return cleaned_words


class LowercaseDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return text.lower()

    def clean_words(self, words: list[str]) -> list[str]:
        return [word.lower() for word in words]


class URLRemovalDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

    def clean_words(self, words: list[str]) -> list[str]:
        return [self.clean_text(word) for word in words]


class PunctuationDatasetCleaner(DatasetCleaner):
    def __init__(self, punctuation: str = string.punctuation) -> None:
        super().__init__()
        self.table = str.maketrans("", "", punctuation)

    def clean_text(self, text: str) -> str:
        return " ".join(self.clean_words(text.split()))

    def clean_words(self, words: list[str]) -> list[str]:
        return [word.translate(self.table) for word in words if word.translate(self.table)]


class NonLetterDataasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return " ".join(self.clean_words(text.split()))

    def clean_words(self, words: list[str]) -> list[str]:
        return [word for word in words if word.isalpha()]


class NewLineDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return text.replace("\n", " ")

    def clean_words(self, words: list[str]) -> list[str]:
        return [self.clean_text(word) for word in words]


class NonASCIIDatasetCleaner(DatasetCleaner):
    def clean_text(self, text: str) -> str:
        return " ".join(self.clean_words(text.split()))

    def clean_words(self, words: list[str]) -> list[str]:
        return [word for word in words if word.isascii()]


class XSpecificDatasetCleaner(DatasetCleaner):
    def __init__(self, remove_emoji: Boolean) -> None:
        super().__init__()
        self.remove_emoji = remove_emoji

    def clean_text(self, text: str) -> str:
        # Remove user mentions
        text = re.sub(r"@\w+", "", text)
        # Remove hashtags
        text = re.sub(r"#\w+", "", text)
        # Remove URLs
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)
        # Remove retweets ('RT' at the start of tweets)
        text = re.sub(r"^RT[\s]+", "", text)
        # Optionally, remove emojis (use Unicode range for emojis)
        if self.remove_emoji:
            text = re.sub(r"[^\w\s,]", "", text)  # Remove everything except words, spaces, and commas
        return text.strip()

    def clean_words(self, words: list[str]) -> list[str]:
        text = " ".join(words)
        return self.clean_text(text).split()


class SpellingCorrectionDatasetCleaner(DatasetCleaner):
    def __init__(self, model: SpellingCorrectionModel) -> None:
        super().__init__()
        self.model = model

    def clean_text(self, text: str) -> str:
        return self.model(text)

    def clean_words(self, words: list[str]) -> list[str]:
        text = " ".join(words)
        return self.clean_text(text).split()


class DatasetCleanerManager:
    def __init__(self, dataset_cleaners: dict[str, DatasetCleaner]) -> None:
        self.dataset_cleaners = dataset_cleaners

    def __call__(self, text: list[str]) -> list[str]:
        for dataset_cleaner in self.dataset_cleaners.values():
            text = dataset_cleaner(text)
        return text
