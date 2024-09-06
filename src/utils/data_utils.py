from pdb import run
from subprocess import CalledProcessError
from typing import Literal
from src.utils.utils import get_logger, run_shell_cmd
from pathlib import Path


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
        status=run_shell_cmd(f"dvc status {dvc_raw_data_folder}.dvc")
        if status=="Data and pipelines are up to date.\n":
            DATA_UTILS_LOGGER.info("Data and pipelines is already up to date")
            return
        else:
            commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)
    except CalledProcessError:
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)


def commit_to_dvc(dvc_raw_data_folder: str, dvc_remote_name: str):
    current_version = run_shell_cmd("git tag --list | sort -t v -k 2 -g | tail -1 | sed 's/v//'").strip()
    if not current_version:
        current_version="0"
    next_version=f"v{int(current_version)+1}"
    run_shell_cmd(f"dvc add {dvc_raw_data_folder}")
    run_shell_cmd("git add .")
    run_shell_cmd(f"git commit -nm 'Updated version of the data from v{current_version} to v{next_version}'")
    run_shell_cmd(f"git tag -a data_v{next_version} -m 'Data version {next_version}'")
    run_shell_cmd(f"dvc push -r {dvc_remote_name}")
    run_shell_cmd("git push --follow-tags")
    run_shell_cmd("git push -f --tags")
