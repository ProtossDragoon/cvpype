# Built-In
import sys
import logging


def set_basic_config(level=logging.INFO):
    logging.basicConfig(
        format=f'(%(asctime)s)[%(levelname)s]:%(module)s: %(message)s',
        datefmt='%Y/%m/%d-%H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        level=level
    )
