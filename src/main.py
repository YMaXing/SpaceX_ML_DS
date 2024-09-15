from src.data_processing.process_data import process_data
from src.config_schemas.config_schema import Config
from src.utils.config_utils import get_config, get_pickle_config, custom_instantiate
from src.utils.utils import get_logger



@get_config(config_path="../configs/auto_generated", config_name="config")
def main(config: Config):
    pass


if __name__ == "__main__":
    main()