import logging
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='bot.log', level=logging.DEBUG, format=FORMAT)

def new_logger(name: str):
    print('create logger with name:' + name)
    return logging.getLogger(name)