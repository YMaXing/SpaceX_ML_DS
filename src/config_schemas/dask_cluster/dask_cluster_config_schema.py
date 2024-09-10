from asyncio import threads
from dataclasses import MISSING, field
from sched import scheduler
from string import punctuation
from typing import Optional, Protocol

from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass

@dataclass
class WorkerClassConfig:
    pass

@dataclass
class DaskClusterConfig:
    __target__: str = MISSING
    n_workers: int = 1

@dataclass
class LocalDaskClusterConfig(DaskClusterConfig):
    __target__ = "dask.distributed.LocalCluster"
    memory_limit: str = "auto"
    processes: bool = True
    threads_per_worker: int = 1
    scheduler_port: int = 8786
    silence_logs: int = 30
    host: Optional[str] = None
    dashboard_address: str = ":8787"
    asychronous: bool = False
    blocked_handlers: Optional[list[str]] = None
    service_kwargs: Optional[dict[str, dict]] = None
    security: Optional[bool] = None
    protocol: Optional[str] = None
    interface: Optional[str] = None
    worker_class: Optional[WorkerClassConfig] = None

def setup_config() -> None:
    cs=ConfigStore.instance()
    cs.store(name="local_dask_cluster_schema", node=LocalDaskClusterConfig, group="dask_cluster")


