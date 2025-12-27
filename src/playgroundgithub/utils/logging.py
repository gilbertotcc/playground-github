import logging
import sys


def setup_logging() -> None:
    logging.basicConfig(stream=sys.stderr,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

