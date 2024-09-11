import string

from cgitb import text
from dataclasses import MISSING, field
from string import punctuation

from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class DatasetCleaner:
    text: list[str] = MISSING  # Required field
    __target__: str = MISSING


@dataclass
class StopwordsDatasetCleanerConfig(DatasetCleaner):
    __target__: str = "src.NLP_process_data.StopwordsDatasetCleaner"


@dataclass
class LowercaseDatasetCleanerConfig(DatasetCleaner):
    __target__: str = "src.NLP_process_data.LowercaseDatasetCleaner"


@dataclass
class URLRemovalDatasetCleanerConfig(DatasetCleaner):
    __target__: str = "src.NLP_process_data.URLRemovalDatasetCleaner"


@dataclass
class PunctuationDatasetCleanerConfig(DatasetCleaner):
    __target__: str = "src.NLP_process_data.PunctuationDatasetCleaner"
    punctuation: str = field(default_factory=lambda: string.punctuation)


@dataclass
class NonLetterDatasetCleanerConfig(DatasetCleaner):
    __target__: str = "src.NLP_process_data.NonLetterDatasetCleaner"


@dataclass
class NewLineDatasetCleanerConfig(DatasetCleaner):
    __target__: str = "src.NLP_process_data.NewLineDatasetCleaner"


@dataclass
class NonASCIIDatasetCleanerConfig(DatasetCleaner):
    __target__: str = "src.NLP_process_data.NonASCIIDatasetCleaner"


@dataclass
class XSpecificDatasetCleanerConfig(DatasetCleaner):
    remove_emoji: bool = False
    __target__: str = "src.NLP_process_data.XSpecificDatasetCleaner"


@dataclass
class SpellingCorrectionModelConfig:
    __target__: str = "src.NLP_process_data.SpellingCorrectionModel"
    max_dict_edit_dist: int = 2
    prefix_length: int = 7
    count_threshold: int = 1


@dataclass
class SpellingCorrectionDatasetCleanerConfig(DatasetCleaner):
    model: SpellingCorrectionModelConfig = field(default_factory=lambda: SpellingCorrectionModelConfig)
    _target_: str = "src.NLP_process_data.SpellingCorrectionDatasetCleaner"


@dataclass
class DatasetCleanerManagerConfig:
    _target_: str = "src.NLP_process_data.DatasetCleanerManager"
    dataset_cleaners: dict[str, DatasetCleaner] = field(default_factory=lambda: {})


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="dataset_cleaner_manager_schema", node=DatasetCleanerManagerConfig, group="dataset_cleaner_manager")
    cs.store(
        name="stopwords_dataset_cleaner_schema",
        node=StopwordsDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
    cs.store(
        name="lowercase_dataset_cleaner_schema",
        node=LowercaseDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
    cs.store(
        name="url_dataset_cleaner_schema",
        node=URLRemovalDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
    cs.store(
        name="punctuation_dataset_cleaner_schema",
        node=PunctuationDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
    cs.store(
        name="non_letter_dataset_cleaner_schema",
        node=NonLetterDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
    cs.store(
        name="new_line_dataset_cleaner_schema",
        node=NewLineDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
    cs.store(
        name="non_ascii_dataset_cleaner_schema",
        node=NonASCIIDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
    cs.store(
        name="x_specific_dataset_cleaner_schema",
        node=XSpecificDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
    cs.store(
        name="spelling_correction_dataset_cleaner_schema",
        node=SpellingCorrectionDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners",
    )
