from dataclasses import MISSING, field
from tokenize import group

from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class DatasetReaderConfig:
    dataset_dir: str = MISSING  # Required field
    dataset_name: str = MISSING  # Required field
    required_columns: list[str] = MISSING  # Required field
    data_format: str = MISSING  # Required field
    _target_: str = MISSING  # Required field
    split_names: list[str] = field(default_factory=lambda: ["train", "val", "test"])


@dataclass
class XDatasetReaderConfig(DatasetReaderConfig):
    _target_: str = "src.data_processing.dataset_readers.XDatasetReader"  # Default field


@dataclass
class DatasetReaderManagerConfig:
    dataset_readers: dict[str, DatasetReaderConfig] = MISSING
    repartition: bool = True
    num_worker: int = 1
    _target_ = "src.data_processing.dataset_readers.DatasetReaderManager"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="xdataset_reader_schema", node=XDatasetReaderConfig, group="dataset_reader_manager/dataset_readers")
    cs.store(name="dataset_reader_manager_schema", node=DatasetReaderManagerConfig, group="dataset_reader_manager")
