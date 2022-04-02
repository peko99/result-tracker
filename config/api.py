# Copyright 2022 Marin Pejcin


from pydantic import BaseSettings


class APIConfig(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 5000

    class Config:
        env_prefix = 'api_'
        env_file = '.env'

config = APIConfig()
