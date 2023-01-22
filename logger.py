import sys
import logging

# File log
assistant_handler = logging.FileHandler('general.log')

# stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)

# configuration
logging.basicConfig(
    level=logging.DEBUG,
    # ( %(name)s ,  %(filename)s )',
    format='[%(asctime)s] : %(levelname)s : %(message)s ',
    handlers=[assistant_handler, stdout_handler]
)

# global logger
logger = logging.getLogger('')
