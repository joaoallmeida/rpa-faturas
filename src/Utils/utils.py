import logging
import requests
from datetime import datetime

def configLogger():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -> %(message)s')
    logger = logging.getLogger(__name__)

    return logger


def sendMessage(message:str) -> int:
    
    from urllib import parse
    
    message = parse.quote(message)

    url = f'https://api.callmebot.com/whatsapp.php?phone=5511969537543&text={message}&apikey=3643807'

    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            logging.info('Mensagem enviado com sucesso!')
            
    except Exception as e:
        raise e
    
def checkStatus(dtVencimento:str) -> str:
   dtVencimento = datetime.strptime(dtVencimento, '%Y-%m-%d').date()
   dtNow=datetime.now().date()

   if dtNow > dtVencimento:
       return "*Pago*"
   else:
       return "*Pendente*"