from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


auth_settings = AuthConfig()
