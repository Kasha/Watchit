"""! @brief Defines the dynamic configuration class built from config.yaml."""
# @file config.py
#  - Configuration module.
#  - Creating Configuration singleton with Sensors new attributes taken from config.yaml
#
# @section author_configuration Author(s)
# - Created by Liad Kashanovsky on 29/04/2024.
#
# Copyright (c) 2024 Liad Kashanovsky.  All rights reserved.

from os import path

import yaml

from alert_notifier_service.resources.defines import logger, app_settings, AlertRuntimeFailedToReadConfigFileError, Any


class Configuration(object):

    @staticmethod
    def __log(message: str = ""):
        print(message)
        logger.debug(message)
        raise AlertRuntimeFailedToReadConfigFileError(details=message)

    def __new__(cls):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)

            file_name = app_settings.CONFIG_FILE_NAME

            if not path.exists(file_name):
                file_name = f"{app_settings.CONFIG_DIR}config.yaml"

            try:
                with open(file_name) as configFile:
                    cls.config = yaml.load(configFile, Loader=yaml.FullLoader)
            except FileNotFoundError as e:
                cls.__log(f"Configuration - File Not Found: {file_name} Error:{e}.")
            except AttributeError as e:
                cls.__log(f"Configuration - Attribute Error:{e}.")

            alert_config: list[dict[str, Any]] = cls.config.get("alert", None)
            if alert_config is None:
                cls.__log("Configuration - Attribute Error: missing required Alert list attribute.")
            elif not alert_config:
                cls.__log("Configuration - Attribute Error: missing Alert list is empty.")

            cls.instance.__dict__["alert"] = dict([(v["type"], v) for v in alert_config])

        return cls.instance

    def __setattr__(self, name, value):
        raise Configuration.__log("Failed to read config.yaml file, using default values")


app_config = Configuration()
