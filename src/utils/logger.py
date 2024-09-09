import logging as logger


logger.basicConfig(
    format='%(asctime)s:%(levelname)s [%(filename)s:%(lineno)s] %(message)s',
    handlers=[logger.FileHandler('errors.log')],
    level=logger.ERROR,
)