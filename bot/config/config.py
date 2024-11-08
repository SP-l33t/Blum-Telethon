from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int = None
    API_HASH: str = None
    GLOBAL_CONFIG_PATH: str = "TG_FARM"

    FIX_CERT: bool = False

    TRACK_BOT_UPDATES: bool = True

    JOIN_TRIBE: str = "6361f86f-6a55-4b6b-b2bd-f73e79e09e38"
    PLAY_GAMES: bool = True
    GAMES_PER_CYCLE: list[int] = [0, 20]
    LOCAL_PAYLOAD: bool = False
    PAYLOAD_API_KEY: str = ""
    POINTS: list[int] = [190, 230]

    PERFORM_TASKS: bool = False

    SESSION_START_DELAY: int = 360

    REF_ID: str = ''

    SESSIONS_PER_PROXY: int = 1
    USE_PROXY_FROM_FILE: bool = True
    DISABLE_PROXY_REPLACE: bool = False
    USE_PROXY_CHAIN: bool = False

    DEVICE_PARAMS: bool = False

    DEBUG_LOGGING: bool = False


settings = Settings()
