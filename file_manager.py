import os
from datetime import datetime
from termcolor import colored
import logging

logger = logging.getLogger(__name__)

def save_code(code, filepath, verbose=False):
    if not code:
        logger.warning("No code generated; skipping file saving.")
        return
    
    logger.debug(f"Attempting to save code to {filepath}")
    logger.debug(f"Code to be saved:\n{repr(code)}")
    
    # Ensure directory exists
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        logger.debug(f"Created directory: {directory}")
    
    # Handle file conflicts with timestamped backups
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_filepath = f"{filepath}.{timestamp}.bak"
        os.rename(filepath, backup_filepath)
        logger.debug(f"Backed up existing file to {backup_filepath}")
    
    try:
        with open(filepath, 'w', newline='') as file:
            file.write(code)
        logger.info(f"Code successfully saved to {filepath}")
        if verbose:
            print(colored(f"Code saved to {filepath}", 'green'))
    except Exception as e:
        logger.error(f"Error saving code to {filepath}: {e}")
        if verbose:
            print(colored(f"Error saving code to {filepath}: {e}", 'red'))
    
    # Verify the saved content
    try:
        with open(filepath, 'r') as file:
            saved_content = file.read()
        logger.debug(f"Verified saved content:\n{repr(saved_content)}")
        if saved_content != code:
            logger.warning("Saved content does not match original code!")
    except Exception as e:
        logger.error(f"Error verifying saved content: {e}")