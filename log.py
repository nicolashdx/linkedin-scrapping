import logging
from datetime import datetime

class Log:
    def __init__(self, lvl, msg):
        current_time = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
        self.level = lvl
        self.message = msg
        
        if self.level == 'detail':
            text = f"{current_time}: \t\t{self.message}"
            logging.info(text)
        
        elif self.level == 'debug':
            text = f"{current_time}: \t{self.message}"
            logging.info(text)
        
        elif self.level == 'info':
            text = f"{current_time}: {self.message}"
            logging.info(text)
            
        elif self.level == 'warning':
            text = f"{current_time}: * {self.message}"
            logging.warning(text)
        
        elif self.level == 'error':
            text = f"{current_time}: ERRO: {self.message.upper()}"
            logging.error(text)
        
        elif self.level == 'critical':
            text = f"{current_time}: ERRO CRÍTICO: {self.message.upper()}"
            logging.critical(text)
        
        else:
            logging.info(self.message)

    @classmethod
    def Init(self):
        current_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        log_filename = f'LOG_{current_time}.log'
        
        logging.getLogger('requests').setLevel(logging.CRITICAL)
        logging.getLogger('duckduckgo_search').setLevel(logging.CRITICAL)
        logging.getLogger('google.generativeai').setLevel(logging.CRITICAL)

        logging.basicConfig(
            level=logging.INFO,
            format='%(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )