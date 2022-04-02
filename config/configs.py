# Copyright 2022 Marin Pejcin


from functools import lru_cache

from config import api, database


@lru_cache()
def get_api_config():
    return api.config


@lru_cache()
def get_database_config():
    return database.config
