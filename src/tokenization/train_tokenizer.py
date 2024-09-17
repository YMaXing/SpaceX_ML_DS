from pathlib import Path
import dask.dataframe as dd
from dask.distributed import Client
import pandas as pd

from hydra.utils import instantiate

from src.config_schemas.tokenization.tokenizer_training_config_schema import TokenizerTrainingConfig
from src.tokenization import tokenizer
from src.utils.config_utils import get_config, get_pickle_config, custom_instantiate
from src.utils.io_utils import write_yaml
from src.utils.utils import get_logger


@get_config(config_path="../configs/auto_generated", config_name="tokenizer_training_config")
def train_tokenizer(config: TokenizerTrainingConfig):
    logger = get_logger(Path(__file__).name)
    logger.info("Training tokenizer...")

    data_parquet_path = config.data_parquet_path
    text_column_name = config.text_column_name

    tokenizer = instantiate(config.tokenizer)

    logger.info("Reading data...")
    df = pd.read_parquet(data_parquet_path)

    logger.info("Starting training tokenizer...")
    tokenizer.train(df[text_column_name].values)

    logger.info("Saving tokenizer...")
    tokenizer_save_dir = data_parquet_path / "tokenizer"
    tokenizer.save(tokenizer_save_dir)

    logger.info("Saving tokenizer training docker info...")
    docker_info = {"docker_image": config.docker_image_name, "docker_tag": config.docker_image_tag}
    docker_info_save_path = tokenizer_save_dir / "tokenizer_training_docker_info.yaml"
    write_yaml(docker_info_save_path, docker_info)

    logger.info("Tokenizer training completed.")   


if __name__ == "__main__":
    train_tokenizer()