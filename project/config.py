from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    OUTLOOK_HOST: str
    OUTLOOK_LOGIN: str
    OUTLOOK_PASSWORD: str

    CALDAV_HOST: str
    CALDAV_LOGIN: str
    CALDAV_PASSWORD: str

    CALDAV_CALENDAR_ID: str

    TZ: str

    model_config = SettingsConfigDict(env_file="../.env")


config = Config()
