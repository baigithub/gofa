from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_prefix="GOFER_",
        extra="ignore",
    )

    env: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    database_url: str = "mysql+pymysql://root:root123456@127.0.0.1:3306/gofer?charset=utf8mb4"
    wechat_callback_secret: str = "gofer-wechat-dev-secret"


settings = Settings()

