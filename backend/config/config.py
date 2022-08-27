from pydantic import BaseSettings


class Settings(BaseSettings):
    """_summary_

    Args:
        BaseSettings (_type_): Basic setting and add env
    """
    app_name: str = "Dates APi"
    admin_email: str = "er.rushabhdoshi@gmail.com"
    secret_api_key: str = "akljnv13bvi2vfo0b0bw"

    class Config:
        env_file = ".env"
