# Copyright 2021 Group 21 @ PI (120)


from pydantic import BaseSettings

class DatabaseConfig(BaseSettings):
    user = 'postgres'
    password = ''
    host = 'localhost'
    port = '5432'
    database = 'result_tracker'

    class Config:
        env_prefix = 'pg_'
        env_file = '.env'

config = DatabaseConfig()
