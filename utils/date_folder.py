import os
import datetime
from utils.logging_setup import auto_log

@auto_log

def create_today_folder(base="Pivot Table"):
    """
    Create a folder named with today's date (dd-mm-yyyy)
    inside the given base folder.
    
    Returns:
        str: Full path of the created/existing folder
    """
    today = datetime.datetime.now().strftime("%d-%m-%Y")

    # Base directory relative to project root
    base_dir = os.path.join(os.getcwd(), "..", base)
    target_dir = os.path.join(base_dir, today)

    # Ensure base and date folder exist
    os.makedirs(target_dir, exist_ok=True)

    return target_dir