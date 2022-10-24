import logging

logging.basicConfig(filename='logs/etl.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger("elk")
