from venv import logger
from src.config_schemas.config_schema import Config
from src.utils.config_utils import get_config
from src.utils.data_utils import dvc_init
from src.utils.utils import get_logger
from pathlib import Path


@get_config(config_path="../configs", config_name="config")
def version_data(config: Config) -> None:
    dvc_init()


if __name__ == "__main__":
    version_data()  # type: ignore
