import logging, pandas as pd
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


def getUnix(x):
    if type(x[0]) == type(pd.Timestamp("2017-01-01")):
        x = [t.timestamp() for t in x]
    return x