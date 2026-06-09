import logging
import os
from datetime import datetime

from from_root import from_root

now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

log_file_name = f"my_app_{now}.log"

folder = "Logs_artifacts"

os.makedirs(folder,exist_ok=True)

print(from_root())

log_file_path = os.path.join(from_root(),f"Python-Logging/{folder}",log_file_name)

print(log_file_path)

logging.basicConfig(
        filename=f"{log_file_path}", 
        level=logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
        filemode = 'w'
        )