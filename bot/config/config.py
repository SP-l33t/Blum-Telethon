from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import dirname, abspath
import __main__ as main


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    PLAY_GAMES: bool = True
    POINTS: list[int] = [190, 230]

    USE_REF: bool = False
    REF_ID: str = ''

    USE_PROXY_FROM_FILE: bool = False

    PROJECT_ROOT: str = dirname(abspath(main.__file__))


settings = Settings()


