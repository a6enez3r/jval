# os
import os
import pathlib
# logging config
import logging.config


def setup_logging(
        logger,
        std_level=logging.INFO,
        info_level=logging.INFO,
        error_level=logging.ERROR):
    """
        configure logger

        params:
            - logger: logging.Logger object
            - std_level: logging level for std out
            - info_level: logging level for info.log
            - error_level: logging level for error.log
        returns:
            - logger: fully configured logger object with
                      multiple handlers & uniform formatter
    """
    # get the current file's directory
    current_path = pathlib.Path(__file__).parent.absolute()
    # define formatter
    formatter = logging.Formatter(
        "[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(funcName)s:%(lineno)s] - [%(message)s]"
    )
    # define stream handler
    std_handler = logging.StreamHandler()
    # add formatter to stream handler
    std_handler.setFormatter(formatter)
    # set stream handler logging level
    std_handler.setLevel(std_level)
    # add stream handler to logger
    logger.addHandler(std_handler)
    # define file handler (logging level INFO)
    file_info_handler = logging.handlers.RotatingFileHandler(
        # log file location
        os.path.join(current_path, "info.log"),
        # max file size
        maxBytes=1000000,
        # num backups
        backupCount=1
    )
    # set file handler logging level
    file_info_handler.setLevel(info_level)
    # set file handler formatter
    file_info_handler.setFormatter(formatter)
    # define file handler (logging level ERROR)
    file_error_handler = logging.handlers.RotatingFileHandler(
        # log file location
        os.path.join(current_path, "error.log"),
        # max file size
        maxBytes=1000000,
        # num backups
        backupCount=1
    )
    # set file handler logging level
    file_error_handler.setLevel(error_level)
    # set file handler formatter
    file_error_handler.setFormatter(formatter)
    # add both file handlers to logger
    logger.addHandler(file_info_handler)
    logger.addHandler(file_error_handler)
    # return configured logger
    return logger
