# Copyright 2022 Marin Pejcin


from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    user = "postgres"
    password = ""
    host = "localhost"
    port = "5432"
    database = "result_tracker"

    class Config:
        env_prefix = "pg_"
        env_file = ".env"


config = DatabaseConfig()
