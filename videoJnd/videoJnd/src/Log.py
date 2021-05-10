import logging

logging.basicConfig(level = logging.INFO
                    , filename = "log.log"
                    , datefmt = '%Y-%m-%d %H:%M:%S'
                    , format = '%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
