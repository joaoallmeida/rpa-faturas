import requests
import logging


class Brk:
    def __init__(self, email:str, password:str, logger:logging.Logger) -> None:
        self.host = "minhabrk.com.br"
        self.cdc = 18217
        self.user = email 
        self.password = password 
        self.logger = logger
        self.reqSession = requests.Session()
        self.authToken = None

    def authenticate(self):
        self.logger.info('Authenticating BRK user.')
        self._login()
        self._token()
        self.logger.info('BRK authentication completed.')

    def _login(self):
        try:
            url = f'https://{self.host}/api/auth/v2/login'
            header = { 
                "Content-Type": "application/json; charset=utf-8" 
            }
            body ={ 
                    "login": self.user,
                    "senha": self.password 
                }

            response = self.reqSession.post(url=url, json=body, headers=header)
            response.raise_for_status
            self.authToken = response.json()['accessToken']
            
        except Exception as e:
            self.logger.error(f'Error in brk login step: {e}')
            raise e
        
    def _token(self):
        try:
           self.reqSession.headers.update({ 'Authorization': f'Bearer {self.authToken}' })
        except Exception as e:
            self.logger.error(f'Error in brk token step: {e}')
            raise e
    
    def debitos(self) -> dict:
        try:
            
            url = f"https://{self.host}/api/conta/v3/debitos?codCdc={self.cdc}&cidade=3"
            response = self.reqSession.get(url=url)
            response.raise_for_status()

            content = response.json()['debitos']

        except Exception as e:
            self.logger.error(f'Error to get debts infos: {e}')
            raise e
        
        return content

    def consumo(self) -> dict:
        try:
            
            url = f"https://{self.host}/api/usuario/consumo?nrCDC={self.cdc}&idCidade=3&nrMeses=12"
            response = self.reqSession.get(url=url)
            response.raise_for_status()

            content = response.json()['debitos']

        except Exception as e:
            self.logger.error(f'Error to get consumption infos: {e}')
            raise e
        
        return content
    
    def detalheFatura(self, debitos:list) -> dict:
        try:
            data = list()
            for db in debitos:
                url = f"https://{self.host}/api/conta/v3/detalheFatura?codCdc={self.cdc}&cidade=3&idFatura={db['idFatura']}&ignorarCrm=false"
                response = self.reqSession.get(url=url)
                response.raise_for_status()

                content = response.json()
                data.append(content)

        except Exception as e:
            self.logger.error(f'Error to get details infos: {e}')
            raise e
        
        return data
    

    def contasPagas(self) -> dict:
        try:
            
            url = f"https://{self.host}/api/conta/contasPagas?codCdc={self.cdc}&cidade=3&nrMeses=12"
            response = self.reqSession.get(url=url)
            response.raise_for_status()

            content = response.json()['contasPagas']

        except Exception as e:
            self.logger.error(f'Error to get payment accounts infos: {e}')
            raise e
        
        return content



# if __name__=="__main__":

#     brk = BRK()
#     brk.authenticate()

#     debitos = brk.debitos()
#     pagos = brk.contasPagas()

#     print(json.dumps(debitos, indent=2))
#     print(json.dumps(pagos, indent=2))