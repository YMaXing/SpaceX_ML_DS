from xmlrpc.client import Boolean

import pandas as pd
import scipy as sp
import dask as dd
from src.config_schemas.config_schema import Config
from src.configs import dataset_reader_manager
from src.utils.config_utils import get_config
from src.utils.gcp_utils import access_secret_version
from src.utils.data_utils import get_raw_data_with_version
from src.utils.utils import get_logger
from abc import ABC, abstractmethod
from hydra.utils import instantiate


@get_config(config_path="../configs", config_name="config")
def prepare_data(config: Config) -> None:
    github_access_token = access_secret_version(project_id=config.infrastructure.project_id, secret_id=config.infrastructure.secret_id)
    get_raw_data_with_version(version=config.version,
                              data_local_save_dir=config.data_local_save_dir,
                              dvc_remote_repo=config.dvc_remote_repo,
                              dvc_data_folder=config.dvc_data_folder,
                              github_user_name=config.github_user_name,
                              github_access_token=github_access_token)
    
    dataset_reader_manager = instantiate(config.dataset_reader_manager)
    dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)

class DatasetReader(ABC):
    def __init__(self, dataset_dir: str, dataset_name: str, required_columns: list[str], split_names: list[str], data_format: str, use_dask: Boolean) -> None:
        super().__init__()
        self.split_names = split_names
        self.dataset_dir = dataset_dir 
        self.dataset_name = dataset_name
        self.required_columns = required_columns
        self.data_format = data_format
        self.use_dask = use_dask
        self.logger = get_logger(self.__class__.__name__)

    def read_data(self):
        df_train, df_val, df_test = self._read_data_pd() if not self.use_dask else self._read_data_dd()
        df = self.assign_split_and_merge(df_train, df_val, df_test)
        df["df_name"] = self.dataset_name
        if any(self.required_columns) not in df.columns:
            raise ValueError(f"Required columns: {self.required_columns} not all found in the data.")
        split_unique = set(df["split"].unique().to_list()) if not self.use_dask else set(df["split"].unique().compute().to_list())
        if split_unique != set(self.split_names):
            raise ValueError(f"Split names: {self.split_names} not all found in the data.")
        return df
    
    @abstractmethod
    def _read_data_pd(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Read and split data into 3 different splits, namely train, validation, test using Pandas.
        The return value must be Pandas or Dask DataFrame(s) with required columns: self.required_columns.
        """
    
    @abstractmethod
    def _read_data_dd(self) -> tuple[dd.core.DataFrame, dd.core.DataFrame, dd.core.DataFrame]:
        """
        Read and split data into 3 different splits, namely train, validation, test using Dask.
        The return value must be Pandas or Dask DataFrame(s) with required columns: self.required_columns.
        """ 
    
    def assign_split_and_merge(self, df_train, df_val, df_test):
        df_train["split"] = "train"
        df_val["split"] = "val"
        df_test["split"] = "test"
        df = pd.concat([df_train, df_val, df_test], axis=0) if not self.use_dask else dd.concat([df_train, df_val, df_test], axis=0)
        return df
    

class XDatasetReader(DatasetReader):
    def __init__(self, dataset_dir: str, dataset_name: str, required_columns: list[str], data_format: str = 'csv', use_dask: Boolean = False) -> None:
        super().__init__(dataset_dir=dataset_dir, dataset_name=dataset_name, required_columns=required_columns, data_format=data_format, use_dask=use_dask)
    
    def _read_data_pd(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        self.logger.info("Reading X(Twitter) data using Pandas.")

        # Mapping of formats to their corresponding pandas read functions
        readers = {
            'csv': pd.read_csv,
            'tsv': pd.read_table,
            'parquet': pd.read_parquet,
            'feather': pd.read_feather,
            'json': pd.read_json,
            'excel': pd.read_excel,
            'xml': pd.read_xml
        }

        # Use the appropriate reader function based on the data format
        read_func = readers.get(self.data_format)
        
        if read_func:
            df_train = read_func(f"{self.dataset_dir}/{self.dataset_name}_train.{self.data_format}")
            df_val = read_func(f"{self.dataset_dir}/{self.dataset_name}_val.{self.data_format}")
            df_test = read_func(f"{self.dataset_dir}/{self.dataset_name}_test.{self.data_format}")
        else:
            raise ValueError(f"Unsupported data format: {self.data_format}")

        return super()._read_data_pd()

    
    def _read_data_dd(self) -> tuple[dd.core.DataFrame, dd.core.DataFrame, dd.core.DataFrame]:
        self.logger.info("Reading X(Twitter) data using Dask.")

        # Mapping of formats to their corresponding dask read functions
        readers = {
            'csv': dd.read_csv,
            'tsv': dd.read_table, 
            'parquet': dd.read_parquet,
            'json': pd.read_json,
        }

        # Use the appropriate reader function based on the data format
        read_func = readers.get(self.data_format)
        
        if read_func:
            df_train = read_func(f"{self.dataset_dir}/{self.dataset_name}_train.{self.data_format}")
            df_val = read_func(f"{self.dataset_dir}/{self.dataset_name}_val.{self.data_format}")
            df_test = read_func(f"{self.dataset_dir}/{self.dataset_name}_test.{self.data_format}")
        else:
            raise ValueError(f"Unsupported data format: {self.data_format}")

        return super()._read_data_dd()
    

class DatasetReaderManager:
    def __init__(self, dataset_readers: dict[str, DatasetReader], use_dask: Boolean) -> None:
        self.dataset_readers = dataset_readers
        self.use_dask = use_dask
    
    def read_data(self):
        dfs = [dataset_reader.read_data() for dataset_reader in self.dataset_readers.values()]
        return pd.concat(dfs, axis=0) if not self.use_dask else dd.concat(dfs, axis=0)

if __name__ == "__main__":
    prepare_data()  # type: ignore