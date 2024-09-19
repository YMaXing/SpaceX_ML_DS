from math import e
import os
import mlflow
from contextlib import contextmanager
from typing import Optional, Iterable 

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")

@contextmanager
def activate_mlflow(
    experiment_name: Optional[str] = None,
    run_id: Optional[str] = None,
    run_name: Optional[str] = None,
    **kwargs
) -> Iterable[mlflow.ActiveRun]:
    
    set_experiment(experiment_name)

def set_experiment(experiment_name: Optional[str] = None) -> None:
    if experiment_name is None:
        experiment_name = "Default"
    
    try:
        mlflow.create_experiment(experiment_name)
    except mlflow.exceptions.RestException:
        pass
     