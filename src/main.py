from src.config_schemas.config_schema import Config
from src.data_processing.process_data import process_data
from src.utils.config_utils import custom_instantiate, get_config, get_pickle_config
from src.utils.utils import get_logger


@get_config(config_path="../configs/auto_generated", config_name="config")
def main(config: Config) -> None:
    pass


if __name__ == "__main__":
    main()
