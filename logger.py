import logging

logging.basicConfig(filename='bot.log', level=logging.DEBUG)

def new_logger(name: str):
    print('create logger with name:' + name)
    return logging.getLogger(name)