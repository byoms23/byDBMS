import logging
import sys

LEVELS = {'-v': logging.DEBUG,
          'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


logger1 = logging.getLogger('byDBMS')    

if len(sys.argv) > 1:
    level_name = sys.argv[1]
    print level_name
    level = LEVELS.get(level_name, logging.NOTSET)
    print level_name, logging.NOTSET
    print level
    logger1.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler("data.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger1.addHandler(ch)
    logger1.addHandler(fh)


logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    filename='myapp.log',
                    filemode='w')

logger1.debug('A debug message')
logger1.info('Some information')
logger1.warning('A shot across the bows')

logger1.debug('This is a debug message')
logger1.info('This is an info message')
logger1.warning('This is a warning message')
logger1.error('This is an error message')
logger1.critical('This is a critical error message')

import Parser
