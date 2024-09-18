from typing import Any

import yaml

from fsspec import AbstractFileSystem, filesystem

GCS_PREFIX = "gs://"
GCS_FILE_SYSTEM_NAME = "gcs"
LOCAL_FILE_SYSTEM_NAME = "file"
TMP_FILE_PATH = "/tmp/"


def choose_file_system(path: str) -> AbstractFileSystem:
    return filesystem(GCS_FILE_SYSTEM_NAME) if path.startswith(GCS_PREFIX) else filesystem(LOCAL_FILE_SYSTEM_NAME)


def open_file(path: str, mode: str = "r") -> Any:
    fs = choose_file_system(path)
    return fs.open(path, mode)


def write_yaml(yaml_path: str, yaml_content: dict[Any, Any]) -> None:
    with open_file(yaml_path, "w") as f:
        yaml.dump(yaml_content, f)


def is_dir(path: str) -> bool:
    fs = choose_file_system(path)
    result: bool = fs.isdir(path)
    return result


def is_file(path: str) -> bool:
    fs = choose_file_system(path)
    result: bool = fs.isfile(path)
    return result


def make_dirs(path: str) -> None:
    fs = choose_file_system(path)
    fs.makedirs(path, exist_ok=True)


def list_paths(path: str) -> list[str]:
    fs = choose_file_system(path)
    if not is_dir(path):
        return []
    paths: list[str] = fs.ls(path)
    if GCS_FILE_SYSTEM_NAME in fs.protocol:
        gs_paths: list[str] = [f"{GCS_PREFIX}{path}" for path in paths]
        return gs_paths
    return paths


def copy_file(source_dir: str, target_dir: str) -> None:
    if not is_dir(target_dir):
        make_dirs(target_dir)
    source_files = list_paths(source_dir)
    for source_file in source_files:
        target_file = f"{target_dir}/{source_file.split('/')[-1]}"
        if is_file(source_file):
            with open_file(source_file, "rb") as source, open_file(target_file, "wb") as target:
                content = source.read()
                target.write(content)
        else:
            raise ValueError(f"{source_file} is not a file.")
