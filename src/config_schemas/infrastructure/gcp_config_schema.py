from dataclasses import MISSING

from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class GCP_Config:
    project_id = "966043703721"
    secret_id = "GCP-data-access-token"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="gcp_config_schema", node=GCP_Config)
