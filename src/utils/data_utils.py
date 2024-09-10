from pathlib import Path
from pdb import run
from shutil import rmtree
from subprocess import CalledProcessError
from typing import Literal, Optional
import dask.dataframe as dd
import psutil

from src.utils.utils import get_logger, run_shell_cmd

DATA_UTILS_LOGGER = get_logger(Path(__file__).name)


def dvc_init() -> None:
    if dvc_initialized():
        DATA_UTILS_LOGGER.info("DVC is already initialized")
        return
    DATA_UTILS_LOGGER.info("DVC is being initialized")
    run_shell_cmd("dvc init")
    run_shell_cmd("dvc config core.analytics false")
    run_shell_cmd("dvc config core.autostage true")
    run_shell_cmd("git add .dvc")
    run_shell_cmd("git commit -nm 'Initialized DVC'")
    DATA_UTILS_LOGGER.info("DVC initialization complete")


def dvc_initialized() -> bool:
    return (Path().cwd() / ".dvc").exists()


def initialize_dvc_storage(dvc_remote_name: str, dvc_remote_url: str) -> None:
    if not run_shell_cmd("dvc remote list"):
        DATA_UTILS_LOGGER.info("Initializing DVC storage")
        run_shell_cmd(f"dvc remote add -d {dvc_remote_name} {dvc_remote_url}")
        run_shell_cmd("git add .dvc/config")
        run_shell_cmd(f"git commit -nm 'Configured DVC remote storage at {dvc_remote_url}'")
        DATA_UTILS_LOGGER.info("DVC storage initialization complete")
    else:
        DATA_UTILS_LOGGER.info("DVC storage is already initialized")


def make_new_data_version(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    try:
        status = run_shell_cmd(f"dvc status {dvc_raw_data_folder}.dvc")
        if status == "Data and pipelines are up to date.\n":
            DATA_UTILS_LOGGER.info("Data and pipelines is already up to date")
            return
        else:
            commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)
    except CalledProcessError:
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)


def commit_to_dvc(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    current_version = run_shell_cmd("git tag --list | sort -t v -k 2 -g | tail -1 | sed 's/v//'").strip()
    if not current_version:
        current_version = "0"
    next_version = f"v{int(current_version)+1}"
    run_shell_cmd(f"dvc add {dvc_raw_data_folder}")
    run_shell_cmd("git add .")
    run_shell_cmd(f"git commit -nm 'Updated version of the data from v{current_version} to v{next_version}'")
    run_shell_cmd(f"git tag -a data_v{next_version} -m 'Data version {next_version}'")
    run_shell_cmd(f"dvc push -r {dvc_remote_name}")
    run_shell_cmd("git push --follow-tags")
    run_shell_cmd("git push -f --tags")


def get_cmd_to_get_raw_data(
    version: str,
    data_local_save_dir: str,
    dvc_remote_repo: str,
    dvc_data_folder: str,
    github_user_name: str,
    github_access_token: str,
) -> str:
    """
    Get shell command to download raw data from dvc store

    Parameters
    ----------
    version : str
        version of the data
    data_local_save_dir : str
        local directory to save the data
    dvc_remote_repo : str
        remote dvc repo holding data information
    dvc_data_folder : str
        dvc folder where data is stored
    github_user_name : str
        github user name
    github_access_token : str
        github access token

    Returns
    -------
    str
        shell command to download raw data from dvc store
    """
    dvc_remote_repo = f"https://{github_user_name}:{github_access_token}@{dvc_remote_repo}"
    command = f"dvc get {dvc_remote_repo} {dvc_data_folder} --rev {version} -o {data_local_save_dir}"

    return command


def get_raw_data_with_version(
    version: str,
    data_local_save_dir: str,
    dvc_remote_repo: str,
    dvc_data_folder: str,
    github_user_name: str,
    github_access_token: str,
) -> None:
    rmtree(data_local_save_dir, ignore_errors=True)
    command = get_cmd_to_get_raw_data(
        version, data_local_save_dir, dvc_remote_repo, dvc_data_folder, github_user_name, github_access_token
    )
    run_shell_cmd(command)


def get_num_partition(
    df_memory_usage: int,
    num_worker: int,
    available_memory: Optional[int],
    min_partition_size: int,
    aimed_num_partition_per_worker: int,
) -> int:
    if available_memory is None:
        available_memory = psutil.virtual_memory().available
    if df_memory_usage <= available_memory:
        return 1
    if df_memory_usage / num_worker <= min_partition_size:
        return round(df_memory_usage / min_partition_size)
    
    num_partition_per_worker = 0
    required_memory = float("inf")

    while required_memory > available_memory:
        num_partition_per_worker += 1
        required_memory = df_memory_usage / num_partition_per_worker
    
    num_partition = num_partition_per_worker * num_worker

    while (df_memory_usage / (num_partition + 1)) > min_partition_size and (num_partition // num_worker) < aimed_num_partition_per_worker:
        num_partition += 1
    
    return num_partition

def repartition_dataframe(
    df: dd.core.Dataframe,
    num_worker: int,
    available_memory: Optional[int] = None,
    min_partition_size: int = 15 * 1024**2,
    aimed_num_partition_per_worker: int = 10,
) -> dd.core.Dataframe:
    df_memory_usage = df.memory_usage(deep=True).sum().compute()
    num_partition = get_num_partition(df_memory_usage, num_worker, available_memory, min_partition_size, aimed_num_partition_per_worker)
    partitioned_df = df.repartition(npartitions=1).repartition(npartitions=num_partition)
    return partitioned_df

