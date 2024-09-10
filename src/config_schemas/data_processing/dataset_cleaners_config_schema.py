from cgitb import text
from dataclasses import MISSING
from string import punctuation
from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass
from dataclasses import field
import string


@dataclass
class DatasetCleaner:
    text: str | list[str] = MISSING # Required field
    __target__: str = MISSING

@dataclass
class StopwordsDatasetCleaner(DatasetCleaner):
    __target__: str = "src.NLP_process_data.StopwordsDatasetCleaner"

@dataclass
class LowercaseDatasetCleaner(DatasetCleaner):
    __target__: str = "src.NLP_process_data.LowercaseDatasetCleaner"

@dataclass
class URLRemovalDatasetCleaner(DatasetCleaner):
    __target__: str = "src.NLP_process_data.URLRemovalDatasetCleaner"

@dataclass
class PunctuationDatasetCleaner(DatasetCleaner):
    __target__: str = "src.NLP_process_data.PunctuationDatasetCleaner"

@dataclass
class NonLetterDatasetCleaner(DatasetCleaner):
    __target__: str = "src.NLP_process_data.NonLetterDatasetCleaner"

@dataclass
class NewLineDatasetCleaner(DatasetCleaner):
    __target__: str = "src.NLP_process_data.NewLineDatasetCleaner"
    punctuation = field(default_factory=lambda: string.punctuation)

@dataclass
class NonASCIIDatasetCleaner(DatasetCleaner):
    __target__: str = "src.NLP_process_data.NonASCIIDatasetCleaner"

@dataclass
class XSpecificDatasetCleaner(DatasetCleaner):
    remove_emoji: bool = False
    __target__: str = "src.NLP_process_data.XSpecificDatasetCleaner"

@dataclass
class SpellingCorrectionModel:
    __target__: str = "src.NLP_process_data.SpellingCorrectionModel"
    max_dict_edit_dist: int = 2
    prefix_length: int = 7
    count_threshold: int = 1

@dataclass
class SpellingCorrectionDatasetCleaner(DatasetCleaner):
    model: SpellingCorrectionModel = SpellingCorrectionModel()  
    __target__: str = "src.NLP_process_data.SpellingCorrectionDatasetCleaner"



@dataclass
class DatasetCleanerManager:
    __target__: str = "src.NLP_process_data.DatasetCleanerManager"
    dataset_cleaners: dict[str, DatasetCleaner] = field(default_factory=lambda: {}) 

def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="dataset_cleaner_manager_schema", node=DatasetCleanerManager, group="dataset_cleaner_manager")
    cs.store(name="stopwords_dataset_cleaner_schema", node=StopwordsDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
    cs.store(name="lowercase_dataset_cleaner_schema", node=LowercaseDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
    cs.store(name="url_dataset_cleaner_schema", node=URLRemovalDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
    cs.store(name="punctuation_dataset_cleaner_schema", node=PunctuationDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
    cs.store(name="non_letter_dataset_cleaner_schema", node=NonLetterDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
    cs.store(name="new_line_dataset_cleaner_schema", node=NewLineDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
    cs.store(name="non_ascii_dataset_cleaner_schema", node=NonASCIIDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
    cs.store(name="x_specific_dataset_cleaner_schema", node=XSpecificDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
    cs.store(name="spelling_correction_dataset_cleaner_schema", node=SpellingCorrectionDatasetCleaner, group="dataset_cleaner_manager/dataset_cleaners")
