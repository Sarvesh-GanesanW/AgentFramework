import os
from datetime import datetime
from termcolor import colored

def save_code(code, filepath, verbose=False):
    if not code:
        print(colored("No code generated; skipping file saving.", 'red'))
        return
    
    # Ensure directory exists
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        if verbose:
            print(colored(f"Directory {directory} created.", 'yellow'))
    
    # Handle file conflicts with timestamped backups
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_filepath = f"{filepath}.{timestamp}.bak"
        os.rename(filepath, backup_filepath)
        if verbose:
            print(colored(f"Existing file {filepath} backed up as {backup_filepath}.", 'yellow'))
    
    try:
        with open(filepath, 'w') as file:
            file.write(code)
        print(colored(f"Code saved to {filepath}", 'green'))
    except Exception as e:
        print(colored(f"Error saving code to {filepath}: {e}", 'red'))
