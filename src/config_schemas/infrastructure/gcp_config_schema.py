from dataclasses import MISSING

from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class GCP_Config:
    project_id : str = "966043703721"
    secret_id : str = "GCP-data-access-token"
    zone : str = "us-west2-b"
    network: str = "default"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="gcp_config_schema", node=GCP_Config)
