from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'sqlite:///./sivefoc-local.db'
    secret_key: str = ''
    cors_origins: str = 'http://localhost:5173'
    access_token_minutes: int = 30
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
