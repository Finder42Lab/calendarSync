from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    OUTLOOK_HOST: str
    OUTLOOK_LOGIN: str
    OUTLOOK_PASSWORD: str
    OUTLOOK_SSL_VERIFY: bool = False

    CALDAV_HOST: str
    CALDAV_LOGIN: str
    CALDAV_PASSWORD: str

    CALDAV_CALENDAR_ID: str
    
    NOTIFICATION_URL: str
    NOTIFICATION_TOKEN: str

    TZ: str

    model_config = SettingsConfigDict(env_file="../.env")


config = Config()
