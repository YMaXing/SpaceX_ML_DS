from fsspec import AbstractFileSystem, filesystem
from typing import Any


GCS_PREFIX = "gs://"
GCS_FILE_SYSTEM_NAME = "gcs" 
LOCAL_FILE_SYSTEM_NAME = "file"
TMP_FILE_PATH = "/tmp/"

def choose_file_type(path: str) -> AbstractFileSystem:
    return filesystem(GCS_FILE_SYSTEM_NAME) if path.startswith(GCS_PREFIX) else filesystem(LOCAL_FILE_SYSTEM_NAME)

def open_file(path: str, mode: str="r") -> Any:
    fs = choose_file_type(path)
    return fs.open(path, mode)