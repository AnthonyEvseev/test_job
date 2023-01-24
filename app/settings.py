from pydantic import BaseSettings
from environs import Env

env = Env()
env.read_env()


class Settings(BaseSettings):
    version: str = "0.0.1"
    redis_dsn: str = env.str('REDIS_DSN')
    rabbit_dsn: str = env.str('RABBIT_DSM')
    host: str = env.str('HOST')
    port: int = env.int('PORT')
    queue_name: str = "calc_queue"


conf = Settings()
