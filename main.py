# Copyright 2022 Marin Pejcin


import uvicorn

from core import api
from config.configs import get_api_config


def main():
    uvicorn.run(api, host=get_api_config().host, port=get_api_config().port)


if __name__ == '__main__':
    main()
