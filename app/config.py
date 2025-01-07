from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str
    secret_key: str

    class Config:
        env_file = ".envs/.env"


settings = Settings()
