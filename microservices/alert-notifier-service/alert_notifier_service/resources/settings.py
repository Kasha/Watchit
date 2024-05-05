# pylint: disable=E0213

"""! @brief Defines the settings suitable for dev/staging/production environments"""
# @file setttings.py
#  - Dev/Staging/Production Settings module.
#
# @section author_configuration Author(s)
# - Created by Liad Kashanovsky on 29/04/2024.
#
# Copyright (c) 2024 Liad Kashanovsky.  All rights reserved.

import logging
import os
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
env = os.getenv("STAGING", "dev").lower()


class EnvTypes(str, Enum):
    """Possible environment"""
    PROD: str = "prod"
    STG: str = "stg"
    DEV: str = "dev"


class AppSettings(BaseModel):
    """Shared settings to all"""
    ENV: EnvTypes = env
    LOGGING_LEVEL: int = logging.DEBUG
    LOG_FILE_NAME: str = f'{env}_watchit_alert.log'
    ABS_DIR: str = f"{str(Path(__file__).parent.parent.resolve())}"
    CONFIG_DIR: str = f"{str(Path(__file__).parent.parent.resolve())}/resources/"
    CONFIG_FILE_NAME: str = f"{CONFIG_DIR}{ENV}_config.yaml"


class AppProdSettings(AppSettings):
    """Production specific settings"""
    LOGGING_LEVEL: int = logging.INFO


class AppStgSettings(AppSettings):
    """Staging specific settings"""
    pass


class AppDevSettings(AppSettings):
    """Development specific settings"""
    pass


def __get_app_settings() -> AppSettings:
    """Factory method to choose settings according to environment"""
    match env:
        case EnvTypes.DEV:
            return AppDevSettings()  # pragma: no cover
        case EnvTypes.PROD:
            return AppProdSettings()  # pragma: no cover
        case EnvTypes.STG:
            return AppStgSettings()  # pragma: no cover

    return AppSettings()  # pragma: no cover


app_settings = __get_app_settings()
