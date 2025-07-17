import logging  
import os
from datetime import datetime

LOG_FILE = f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.log'

logs_path = os.path.join(os.getcwd(), "logs")
#makes the path to logs folder in current directory eg /apple/project/logs
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
#join the path i.e /apple/project/logs and log file i.e 16_07_2025_11_29_01.log


logging.basicConfig(
        filename=LOG_FILE_PATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s  " , # d means it is integer whereas s means it is a string  
        level=logging.INFO,
)


if __name__=="__main__":
    logging.info("Logging has started")