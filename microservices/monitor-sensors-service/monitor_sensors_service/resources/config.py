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

from monitor_sensors_service.resources.defines import logger, app_settings, \
    SensorRuntimeFailedToReadConfigFileError, Any


class Configuration(object):

    @staticmethod
    def __log(message: str = ""):
        print(message)
        logger.debug(message)
        raise SensorRuntimeFailedToReadConfigFileError(details=message)

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

            sens_config: list[dict[str, Any]] = cls.config.get("sensors", None)
            if sens_config is None:
                cls.__log("Configuration - Attribute Error: missing required Sensors list attribute.")
            elif not sens_config:
                cls.__log("Configuration - Attribute Error: missing Sensors list is empty.")

            sensor_items: list = sens_config
            # Add config.sensors items for existing yaml entry with valid attribute (typ, valid_range)
            cls.instance.__dict__["sensors"] = dict([(str(v["type"]).lower(), v) for v in sensor_items
                                                     if v.get("type", None) is not None
                                                     and v.get("valid_range", None) is not None
                                                     and len(v.get("valid_range", [])) != 0])

        return cls.instance

    def __setattr__(self, name, value):
        raise Configuration.__log("Failed to read config.yaml file, using default values")


app_config = Configuration()
