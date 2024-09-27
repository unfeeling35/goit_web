from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    user: str
    password: str
    db_name: str
    domain: str
    port: int
    database_url: str
    mail_username: str
    mail_password: str
    mail_port: int
    mail_server: str
    api_key: str
    api_secret: str
    api_name: str
    redis_port: int
    algorithm: str
    redis_host: str

    class Config:
        env_file = ".ENV"
        env_file_encoding = "utf-8"


settings = Settings()

#print(settings.model_dump())