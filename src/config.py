from pydantic_settings import BaseSettings, SettingsConfigDict

# defining class to access env variables across code
class Settings(BaseSettings):
    DATABASE_URL : str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()