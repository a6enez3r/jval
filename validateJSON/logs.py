import os, pathlib
# logging
import logging.config


def setup_logging(logger, std_level=logging.INFO, info_level=logging.INFO, error_level=logging.ERROR):
    """
        setup logging configuration. add formatter and 3 handlers
        (std out, info file, error file)

        params:
            - logger: python logger object
            - std_level: std out logging level
            - info_level: info file logging level
            - error_level: error file logging level
        returns:
            configured logger
    """
    # get dir path
    current_path = pathlib.Path(__file__).parent.absolute()
    # define formatter
    formatter = logging.Formatter(
        "[%(asctime)s] - %(name)-25s %(levelname)-10s %(funcName)s:%(lineno)-18s   %(message)s"
    )
    # define stream handler
    std_handler = logging.StreamHandler()
    # add formatter to stream handler
    std_handler.setFormatter(formatter)
    # set level
    std_handler.setLevel(std_level)
    # add handler
    logger.addHandler(std_handler)
    # define file info handler
    file_info_handler = logging.handlers.RotatingFileHandler(
        os.path.join(current_path, "info.log"),
        maxBytes=1000000,
        backupCount=1
    )
    # set level
    file_info_handler.setLevel(info_level)
    # set formatter
    file_info_handler.setFormatter(formatter)
    # add handler
    logger.addHandler(file_info_handler)
    # define file error handler
    file_error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(current_path, "error.log"),
        maxBytes=1000000,
        backupCount=1
    )
    # set level
    file_error_handler.setLevel(error_level)
    # set formatter
    file_error_handler.setFormatter(formatter)
    # add handler to logger
    logger.addHandler(file_error_handler)
    # return logger
    return logger
