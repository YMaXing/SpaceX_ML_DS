from pathlib import Path
from venv import logger

from src.config_schemas.config_schema import Config
from src.utils.config_utils import get_config
from src.utils.data_utils import dvc_init, initialize_dvc_storage, make_new_data_version
from src.utils.utils import get_logger


@get_config(config_path="../configs", config_name="config")
def version_data(config: Config) -> None:
    dvc_init()
    initialize_dvc_storage(config.dvc_remote_name, config.dvc_remote_url)
    make_new_data_version(config.dvc_raw_data_folder, config.dvc_remote_name)


if __name__ == "__main__":
    version_data()
