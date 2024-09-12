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
    _target_: str = "src.process_data.XDatasetReader"  # Default field


@dataclass
class DatasetReaderManagerConfig:
    dataset_readers: dict[str, DatasetReaderConfig] = MISSING
    repartition: bool = True
    use_dask: bool = False
    num_worker: int = 1
    _target_ = "src.process_data.DatasetReaderManager"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="xdataset_reader_schema", node=XDatasetReaderConfig, group="dataset_reader_manager/dataset_readers/x")
    cs.store(name="dataset_reader_manager_schema", node=DatasetReaderManagerConfig, group="dataset_reader_manager")
