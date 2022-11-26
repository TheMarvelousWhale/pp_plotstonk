import logging
from datetime import datetime

def getDay()->str:
    return datetime.now().strftime("%Y_%m_%d")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,  
    filename=f'log/anya_{getDay()}.log'
)

logger = logging.getLogger(__name__)

def wrap3F(a)->str:
    return f"{a:.3f}"


    