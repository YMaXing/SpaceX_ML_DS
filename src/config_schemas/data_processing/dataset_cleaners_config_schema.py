import string
from dataclasses import dataclass, field
from string import punctuation

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING

@dataclass
class DatasetCleanerConfig:
    _target_: str = MISSING

@dataclass
class StopwordsDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "src.data_processing.NLP_process_data.StopwordsDatasetCleaner"


@dataclass
class LowercaseDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "src.data_processing.NLP_process_data.LowercaseDatasetCleaner"


@dataclass
class URLRemovalDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "src.data_processing.NLP_process_data.URLRemovalDatasetCleaner"


@dataclass
class PunctuationDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "src.data_processing.NLP_process_data.PunctuationDatasetCleaner"
    punctuation: str = field(default_factory=lambda: string.punctuation)


@dataclass
class NonLetterDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "src.data_processing.NLP_process_data.NonLetterDatasetCleaner"


@dataclass
class NewLineDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "src.data_processing.NLP_process_data.NewLineDatasetCleaner"


@dataclass
class NonASCIIDatasetCleanerConfig(DatasetCleanerConfig):
    _target_: str = "src.data_processing.NLP_process_data.NonASCIIDatasetCleaner"


@dataclass
class XSpecificDatasetCleanerConfig(DatasetCleanerConfig):
    remove_emoji: bool = False
    _target_: str = "src.data_processing.NLP_process_data.XSpecificDatasetCleaner"


@dataclass
class SpellingCorrectionModelConfig:
    _target_: str = "src.data_processing.NLP_process_data.SpellingCorrectionModel"
    max_dict_edit_dist: int = 2
    prefix_length: int = 7
    count_threshold: int = 1


@dataclass
class SpellingCorrectionDatasetCleanerConfig(DatasetCleanerConfig):
    model: SpellingCorrectionModelConfig = field(default_factory=lambda: SpellingCorrectionModelConfig)
    _target_: str = "src.data_processing.NLP_process_data.SpellingCorrectionDatasetCleaner"


@dataclass
class DatasetCleanerManagerConfig:
    _target_: str = "src.data_processing.NLP_process_data.DatasetCleanerManager"
    dataset_cleaners: dict[str, DatasetCleanerConfig] = field(default_factory=lambda: {})


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(name="dataset_cleaner_manager_schema", node=DatasetCleanerManagerConfig, group="dataset_cleaner_manager")
    cs.store(
        name="stopwords_dataset_cleaner_schema",
        node=StopwordsDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/stopwords",
    )
    cs.store(
        name="lowercase_dataset_cleaner_schema",
        node=LowercaseDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/lowercase",
    )
    cs.store(
        name="url_dataset_cleaner_schema",
        node=URLRemovalDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/url",
    )
    cs.store(
        name="punctuation_dataset_cleaner_schema",
        node=PunctuationDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/punctuation",
    )
    cs.store(
        name="non_letter_dataset_cleaner_schema",
        node=NonLetterDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/non_letter",
    )
    cs.store(
        name="new_line_dataset_cleaner_schema",
        node=NewLineDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/newline",
    )
    cs.store(
        name="non_ascii_dataset_cleaner_schema",
        node=NonASCIIDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/non_ascii",
    )
    cs.store(
        name="x_specific_dataset_cleaner_schema",
        node=XSpecificDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/x_specific",
    )
    cs.store(
        name="spelling_correction_dataset_cleaner_schema",
        node=SpellingCorrectionDatasetCleanerConfig,
        group="dataset_cleaner_manager/dataset_cleaners/spelling_correction",
    )