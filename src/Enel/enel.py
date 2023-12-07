import requests
import logging
from requests.exceptions import *

class Enel:
    def __init__(self, email:str, password:str, enelKey:str, logger:logging.Logger) -> None:
        self.reqSession = requests.Session()
        self.logger = logger
        self.host = 'portalhome.eneldistribuicaosp.com.br'
        self.email = email
        self.password = password
        self.key = enelKey
        self.bearer = None
        self.authToken = None
        self.refreshToken = None
        self.tokenId = None

    def authenticate(self):
        self.logger.info('Authenticating Enel user.')
        self._login()
        self._veryfyToken()
        self._token()
        self._login2()
        self._authorization()
        self.logger.info('Enel authentication completed.')

    def _login(self):
        try:
            url = f'https://{ self.host }/api/firebase/login'
            header = { 
                "Content-Type": "application/json", 
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
            }
            body = {
                "I_CANAL": "ZINT",
                "I_EMAIL": self.email,
                "I_PASSWORD": self.password
            }

            response = self.reqSession.post(url=url, json=body, headers=header)
            response.raise_for_status()
            
            self.authToken = response.json()['token']
            
        except Exception as e:
            self.logger.error(f'Error in enel login step: {e}')
            raise e

    def _veryfyToken(self):
        try:
            url = f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={self.key}'
            header = { 
                "Content-Type": "application/json" 
            }
            body = {
                "token": self.authToken,
                "returnSecureToken": True
            }

            response = self.reqSession.post(url=url, json=body, headers=header)
            response.raise_for_status()

            self.refreshToken = response.json()['refreshToken']

        except Exception as e:
            self.logger.error(f'Error in enel veryfy token step: {e}')
            raise e 

    def _token(self):
        try:
           
            url = f'https://securetoken.googleapis.com/v1/token?key={self.key}'
            header = { "Content-Type": "application/x-www-form-urlencoded" }
            body = { "grant_type":"refresh_token", "refresh_token": self.refreshToken }

            response = self.reqSession.post(url=url, data=body, headers=header)
            response.raise_for_status()

            self.tokenId = response.json()['id_token']
           
        except HTTPError as e:
            self.logger.error(f'HTTP error in enel token step: {e}')
            raise e
        except Exception as e:
            self.logger.error(f'Error in enel token step: {e}')
            raise e

    def _login2(self):
        try:
           
            url = f'https://{ self.host }/api/sap/getloginv2'
            header = {
               "Content-Type": "application/json"
            }
            body = {
                "I_CANAL":"ZINT",
                "I_COBRADORA":"",
                "I_CPF":"",
                "I_CNPJ":"",
                "I_ANLAGE":"",
                "I_COD_SERV":"TC",
                "I_LISTA_INST":"X",
                "I_BANDEIRA":"X",
                "I_FBIDTOKEN":self.tokenId,
                "I_VERTRAG":"",
                "I_PARTNER":"",
                "I_RESPOSTA_01":"",
                "I_RESPOSTA_02":"",
                "I_EXEC_LOGIN":"X",
                "I_AMBIENTE":"PRD"
            }

            response = self.reqSession.post(url=url, json=body, headers=header)
            response.raise_for_status()

            self.bearer = response.headers['Authorization']
           
        except Exception as e:
            self.logger.error(f'Error in enel login2 step: {e}')
            raise e
        
    def _authorization(self):
        try:
            self.reqSession.headers.update({ 'Authorization': self.bearer })
        except Exception as e:
            self.logger.error(f'Error in enel authorization step: {e}')
            raise e
        
    def contas(self) -> dict:
        try:
            url = f'https://{self.host}/api/sap/portalinfo'
            header = { "Content-Type": "application/json" }
            body = {
                "I_CANAL":"ZINT",
                "I_COD_SERV":"TC",
                "I_SSO_GUID":""
            }

            response = self.reqSession.post(url=url, json=body, headers=header)
            response.raise_for_status()

            content = response.json()['ET_CONTAS']

        except Exception as e:
            self.logger.error(f'Error in get enel accounts: {e}')
            raise e
        
        return content

# if __name__=="__main__":

#     enel = Enel()
#     enel.authenticate()

#     print(json.dumps(enel.contas(),indent=2))
