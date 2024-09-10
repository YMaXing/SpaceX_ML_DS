from dataclasses import MISSING, dataclass, field

from hydra.core.config_store import ConfigStore

from src.config_schemas.data_processing import dataset_cleaners_config_schema, dataset_readers_config_schema
from src.config_schemas.infrastructure import gcp_config_schema
from src.config_schemas.dask_cluster import dask_cluster_config_schema


@dataclass
class Config:

    version: str = MISSING
    dataset_reader_manager: dataset_readers_config_schema.DatasetReaderManagerConfig = MISSING
    dataset_cleaner_manager: dataset_cleaners_config_schema.DatasetCleanerManagerConfig = MISSING
    dask_cluster: dask_cluster_config_schema.DaskClusterConfig = MISSING
    processed_data_save_dir: str = MISSING

    dvc_remote_name: str = "gcs-storage"
    dvc_remote_url: str = "gs://ymx-project-1-bucket-1/data/raw"
    dvc_raw_data_folder: str = "data/raw"

    data_local_save_dir: str = "data/raw"
    dvc_remote_repo: str = "https://github.com/YMaXing/spaces_ml_ds.git"
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "YMaXing"

    infrastructure: gcp_config_schema.GCP_Config = field(default_factory=gcp_config_schema.GCP_Config)
    use_dask: bool = False

def setup_config() -> None:
    dataset_readers_config_schema.setup_config()
    gcp_config_schema.setup_config()
    dataset_cleaners_config_schema.setup_config()

    gcp_config_schema.setup_config()
    dataset_readers_config_schema.setup_config()
    dataset_cleaners_config_schema.setup_config()

    dask_cluster_config_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
