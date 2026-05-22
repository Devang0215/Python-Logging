from logger import logging
import my_lib

logger = logging.getLogger(__name__)

def main():
    logger.info('Started')
    my_lib.do_something()
    logger.info('Finished')

if __name__ == "__main__":
    main()


