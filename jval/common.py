"""
Module-wide / shared constants.

Attributes
----------
    LOGGING_DICT (dict): Logging configuration dictionary.

"""
LOGGING_DICT = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(funcName)s:%(lineno)s] - [%(message)s]"  # pylint: disable=line-too-long
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "mock": {
            "handlers": ["console"],
            "propagate": True,
            "level": "WARNING",
        }
    },
}
