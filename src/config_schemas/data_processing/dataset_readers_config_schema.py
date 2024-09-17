from dataclasses import dataclass, field
from omegaconf import SI, MISSING

from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass
from typing import Optional

@dataclass
class DatasetReaderConfig:
    dataset_dir: str = MISSING  # Required field
    dataset_name: str = MISSING  # Required field
    required_columns: list[str] = MISSING  # Required field
    data_format: str = MISSING  # Required field
    _target_: str = MISSING  # Required field
    gcp_project_id: str = SI("${infrastructure.project_id}")
    gcp_github_access_token_secret_id: str = SI("${infrastructure.secret_id}")
    dvc_remote_repo: str = SI("${dvc_remote_repo}")
    github_user_name: str = SI("${github_user_name}")
    version: str = SI("${version}")
    split_names: list[str] = field(default_factory=lambda: ["train", "val", "test"])


@dataclass
class XDatasetReaderConfig(DatasetReaderConfig):
    _target_: str = "src.data_processing.dataset_reader.XDatasetReader"  # Default field


@dataclass
class DatasetReaderManagerConfig:
    dataset_readers: dict[str, DatasetReaderConfig] = MISSING
    repartition: bool = True
    use_dask: bool = False
    num_worker: int = 1
    available_memory: Optional[float] = None
    _target_ = "src.data_processing.dataset_reader.DatasetReaderManager"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="xdataset_reader_schema", node=XDatasetReaderConfig, group="dataset_reader_manager/dataset_readers/x")
    cs.store(name="dataset_reader_manager_schema", node=DatasetReaderManagerConfig, group="dataset_reader_manager")
