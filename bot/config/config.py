from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int = None
    API_HASH: str = None
    GLOBAL_CONFIG_PATH: str = "TG_FARM"

    FIX_CERT: bool = False

    PLAY_GAMES: bool = True
    POINTS: list[int] = [190, 230]

    PERFORM_TASKS: bool = False

    USE_RANDOM_DELAY_IN_RUN: bool = True
    RANDOM_DELAY_IN_RUN: list[int] = [5, 30]

    REF_ID: str = ''

    SESSIONS_PER_PROXY: int = 1
    USE_PROXY_FROM_FILE: bool = True
    DISABLE_PROXY_REPLACE: bool = False
    USE_PROXY_CHAIN: bool = False

    DEVICE_PARAMS: bool = False

    DEBUG_LOGGING: bool = False


settings = Settings()
