import logging,os
from datetime import datetime

def log_user_info(u):
    logger.info(f'{u.effective_user.username} said {u.message.text}')  

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,  
    filename=f'log/{datetime.now().strftime("%Y_%m_%d")}.log'
)

logger = logging.getLogger(__name__)

def load_from_same_dir(name:str):
    return os.path.join(os.getcwd(),name)