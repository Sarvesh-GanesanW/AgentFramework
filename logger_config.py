# logger_config.py
import logging
import os

def setup_logging(log_file='test_agent.log', verbose=False):
    # Ensure the log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set up logging configuration
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        filename=log_file,
        filemode='a',  # Append to the log file
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level
    )
    logger = logging.getLogger(__name__)
    return logger
