from utils import get_logger, run_shell_cmd
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

def dvc_initialized() -> bool:
    return (Path().cwd() / ".dvc").exists()
