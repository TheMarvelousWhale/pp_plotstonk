import logging
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,  
    filename=f'log/anya_{datetime.now().strftime("%Y_%m_%d")}.log'
)

logger = logging.getLogger(__name__)



    