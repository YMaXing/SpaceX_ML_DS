from src.config_schemas.config_schema import Config
from src.utils.config_utils import get_config
from src.utils.gcp_utils import access_secret_version
from src.utils.data_utils import get_raw_data_with_version


@get_config(config_path="../configs", config_name="config")
def prepare_data(config: Config) -> None:
    github_access_token = access_secret_version(project_id=config.infrastructure.project_id, secret_id=config.infrastructure.secret_id)
    get_raw_data_with_version(version=config.version,
                              data_local_save_dir=config.data_local_save_dir,
                              dvc_remote_repo=config.dvc_remote_repo,
                              dvc_data_folder=config.dvc_data_folder,
                              github_user_name=config.github_user_name,
                              github_access_token=github_access_token)


if __name__ == "__main__":
    prepare_data()  # type: ignore