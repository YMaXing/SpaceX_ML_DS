from dataclasses import MISSING
from hydra.core.config_store import ConfigStore
from dataclasses import dataclass, field
from src.config_schemas.infrastructure.gcp_config_schema import GCP_Config

@dataclass
class Config:

    version: str = MISSING 
    
    dvc_remote_name: str = "gcs-storage"
    dvc_remote_url: str = "gs://ymx-project-1-bucket-1/data/raw"
    dvc_raw_data_folder: str = "data/raw"

     
    data_local_save_dir: str = "data/raw"
    dvc_remote_repo: str = "https://github.com/YMaXing/spaces_ml_ds.git"
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "YMaXing"

    infrastructure: GCP_Config = field(default_factory=GCP_Config) 


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
