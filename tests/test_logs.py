import logging
from validateJSON.logs import setup_logging


def test_setup_logging():
    # create logger
    logger = setup_logging(logging.getLogger(__name__))
    # assert logger type
    assert type(logger) == logging.Logger
