import logging
import os

def setup_logging(log_file='test_agent.log', verbose=False):
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level
    )
    logger = logging.getLogger(__name__)
    return logger
