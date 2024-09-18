from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import dask.dataframe as dd
import pandas as pd

from dvc.api import get_url

from src.utils.data_utils import get_repo_url_with_access_token, repartition_dataframe
from src.utils.utils import get_logger


class DatasetReader(ABC):
    def __init__(
        self,
        dataset_dir: str,
        dataset_name: str,
        required_columns: list[str],
        split_names: list[str],
        data_format: str,
        use_dask: bool,
        gcp_project_id: str,
        gcp_github_access_token_secret_id: str,
        dvc_remote_repo: str,
        github_user_name: str,
        version: str,
    ) -> None:
        super().__init__()
        self.split_names = split_names
        self.dataset_dir = dataset_dir
        self.dataset_name = dataset_name
        self.required_columns = required_columns
        self.data_format = data_format
        self.use_dask = use_dask
        self.version = version
        self.dvc_remote_repo = get_repo_url_with_access_token(
            gcp_project_id, gcp_github_access_token_secret_id, dvc_remote_repo, github_user_name
        )
        self.logger = get_logger(self.__class__.__name__)

    def read_data(self) -> pd.DataFrame | dd.core.DataFrame:
        df_train, df_val, df_test = self._read_data_pd() if not self.use_dask else self._read_data_dd()
        df = self.assign_split_and_merge(df_train, df_val, df_test)
        df["df_name"] = self.dataset_name
        if any(self.required_columns) not in df.columns:
            raise ValueError(f"Required columns: {self.required_columns} not all found in the data.")
        split_unique = (
            set(df["split"].unique().to_list()) if not self.use_dask else set(df["split"].unique().compute().to_list())
        )
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

    def assign_split_and_merge(self, df_train: pd.DataFrame | dd.core.DataFrame, df_val: pd.DataFrame | dd.core.DataFrame, df_test: pd.DataFrame | dd.core.DataFrame) -> pd.DataFrame | dd.core.DataFrame:
        df_train["split"] = "train"
        df_val["split"] = "val"
        df_test["split"] = "test"
        df = (
            pd.concat([df_train, df_val, df_test], axis=0)
            if not self.use_dask
            else dd.concat([df_train, df_val, df_test], axis=0)
        )
        return df

    def get_remote_data_url(self, dataset_path: str) -> str:
        url: str = get_url(path=dataset_path, repo=self.dvc_remote_repo, ref=self.version)
        return url


class XDatasetReader(DatasetReader):
    def __init__(
        self,
        dataset_dir: str,
        dataset_name: str,
        required_columns: list[str],
        split_names: list[str],
        use_dask: bool,
        gcp_project_id: str,
        gcp_github_access_token_secret_id: str,
        dvc_remote_repo: str,
        github_user_name: str,
        version: str,
        data_format: str = "csv",
    ) -> None:
        super().__init__(
            dataset_dir=dataset_dir,
            dataset_name=dataset_name,
            gcp_github_access_token_secret_id="github_access_token",
            dvc_remote_repo=dvc_remote_repo,
            github_user_name=github_user_name,
            version=version,
            required_columns=required_columns,
            split_names=split_names,
            data_format=data_format,
            use_dask=use_dask,
            gcp_project_id=gcp_project_id
        )

    def _read_data_pd(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        self.logger.info("Reading X(Twitter) data using Pandas.")

        # Mapping of formats to their corresponding pandas read functions
        readers = {
            "csv": pd.read_csv,
            "tsv": pd.read_table,
            "parquet": pd.read_parquet,
            "feather": pd.read_feather,
            "json": pd.read_json,
            "excel": pd.read_excel,
            "xml": pd.read_xml,
        }

        # Use the appropriate reader function based on the data format
        read_func = readers.get(self.data_format)
        if read_func:
            train_path = f"{self.dataset_dir}/{self.dataset_name}_train.{self.data_format}"
            val_path = f"{self.dataset_dir}/{self.dataset_name}_val.{self.data_format}"
            test_path = f"{self.dataset_dir}/{self.dataset_name}_test.{self.data_format}"

            train_url = self.get_remote_data_url(train_path)
            val_url = self.get_remote_data_url(val_path)
            test_url = self.get_remote_data_url(test_path)

            df_train = read_func(train_url)
            df_val = read_func(val_url)
            df_test = read_func(test_url)
        else:
            raise ValueError(f"Unsupported data format: {self.data_format}")

        return df_train, df_val, df_test

    def _read_data_dd(self) -> tuple[dd.core.DataFrame, dd.core.DataFrame, dd.core.DataFrame]:
        self.logger.info("Reading X(Twitter) data using Dask.")

        # Mapping of formats to their corresponding dask read functions
        readers = {
            "csv": dd.read_csv,
            "tsv": dd.read_table,
            "parquet": dd.read_parquet,
            "json": pd.read_json,
        }

        # Use the appropriate reader function based on the data format
        read_func = readers.get(self.data_format)

        if read_func:
            train_path = f"{self.dataset_dir}/{self.dataset_name}_train.{self.data_format}"
            val_path = f"{self.dataset_dir}/{self.dataset_name}_val.{self.data_format}"
            test_path = f"{self.dataset_dir}/{self.dataset_name}_test.{self.data_format}"

            train_url = self.get_remote_data_url(train_path)
            val_url = self.get_remote_data_url(val_path)
            test_url = self.get_remote_data_url(test_path)

            df_train = read_func(train_url)
            df_val = read_func(val_url)
            df_test = read_func(test_url)
        else:
            raise ValueError(f"Unsupported data format: {self.data_format}")

        return df_train, df_val, df_test


class DatasetReaderManager:
    def __init__(
        self,
        dataset_readers: dict[str, DatasetReader],
        use_dask: bool,
        repartition: bool = True,
        available_memory: Optional[float] = None,
    ) -> None:
        self.dataset_readers = dataset_readers
        self.use_dask = use_dask
        self.repartition = repartition
        self.available_memory = available_memory

    def read_data(self, num_worker: int) -> pd.DataFrame | dd.core.DataFrame:
        dfs = [dataset_reader.read_data() for dataset_reader in self.dataset_readers.values()]
        if self.repartition:
            dfs = repartition_dataframe(dfs, num_worker=num_worker, available_memory=self.available_memory)
        return pd.concat(dfs, axis=0) if not self.use_dask else dd.concat(dfs, axis=0)
