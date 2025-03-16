from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


auth_settings = AuthConfig()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
