from pathlib import Path

import dask.dataframe as dd
import pandas as pd

from dask.distributed import Client
from hydra.utils import instantiate

from src.config_schemas.data_processing.data_processing_config_schema import DataProcessingConfig
from src.config_schemas.data_processing.dataset_cleaners_config_schema import DatasetCleanerManagerConfig
from src.utils.config_utils import custom_instantiate, get_config, get_pickle_config
from src.utils.io_utils import write_yaml
from src.utils.utils import get_logger


@get_config(config_path="../configs/auto_generated", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None:
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")
    if config.use_dask:
        cluster = custom_instantiate(config.dask_cluster)
        client = Client(cluster)
        try:
            prepare_data(config)
        finally:
            logger.info("Closing Dask client and cluster...")
            client.close()
            cluster.close()
    else:
        prepare_data(config)


def process_raw_data(
    df_partition: dd.core.DataFrame, dataset_cleaner_manager: DatasetCleanerManagerConfig
) -> dd.core.Series:
    cleaned_text: dd.core.Series = df_partition["text"].apply(dataset_cleaner_manager)
    return cleaned_text


@get_config(config_path="../configs/auto_generated", config_name="data_processing_config")
def prepare_data(config: DataProcessingConfig) -> None:

    dataset_reader_manager = instantiate(config.dataset_reader_manager, use_dask=config.use_dask)
    dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)

    if config.use_dask:
        df = dataset_reader_manager.read_data(num_worker=config.dataset_reader_manager.num_worker)
        logger = get_logger(Path(__file__).name)
        logger.info("Cleaning data...")
        df = df.assign(
            cleaned_text=df.map_partitions(
                process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager, meta=("text", "object")
            )
        )
        df = df.compute()
    else:
        df = dataset_reader_manager.read_data()
        df = df.assign(cleaned_text=df["text"].apply(dataset_cleaner_manager))

    processed_data_save_dir = Path(config.data_local_save_dir) / "processed"
    train_parquet_path = processed_data_save_dir / "train.parquet"
    val_parquet_path = processed_data_save_dir / "val.parquet"
    test_parquet_path = processed_data_save_dir / "test.parquet"

    df.loc[df["split"] == "train"].to_parquet(train_parquet_path)
    df.loc[df["split"] == "val"].to_parquet(val_parquet_path)
    df.loc[df["split"] == "test"].to_parquet(test_parquet_path)

    docker_info = {"docker_image": config.docker_image_name, "docker_tag": config.docker_image_tag}
    docker_info_save_path = processed_data_save_dir / "docker_info.yaml"

    write_yaml(str(docker_info_save_path), docker_info)

    logger.info("Data processing finished, processed data saved.")


if __name__ == "__main__":
    process_data()
