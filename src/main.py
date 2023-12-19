from Brk.brk import Brk
from Enel.enel import Enel
from Utils.utils import *
from datetime import datetime

import pandas as pd
import os

logger = configLogger()

def faturaBrk(user:str, password:str) -> dict:
    try:
        brk = Brk(user, password, logger)
        brk.authenticate()

        debitos = brk.debitos()
        
        if debitos:

            if debitos['emAberto']:
                fatura = brk.detalheFatura(debitos['emAberto'])

                dfBrk = pd.DataFrame(fatura)
                dfBrk = dfBrk[['competenciaMes','vencimento','status','valorTotal','codBoleto']]
                dfBrk['vencimento'] = pd.to_datetime(dfBrk['vencimento']).dt.strftime('%Y-%d-%m')
                dfBrk['status'] = dfBrk['status'].str.title()

                record = dfBrk.to_dict(orient='records')
            
            else:
                fatura = brk.detalheFatura(debitos['atrasada'])

                dfBrk = pd.DataFrame(fatura)
                dfBrk = dfBrk[['competenciaMes','vencimento','status','valorTotal','codBoleto']]
                dfBrk['vencimento'] = pd.to_datetime(dfBrk['vencimento']).dt.strftime('%Y-%d-%m')
                dfBrk['status'] = dfBrk['status'].str.title()

                record = dfBrk.to_dict(orient='records')
            
            return record
        
        else:
            logger.info('Sem faturas!')

    except Exception as e:
        raise e
    

def faturasEnel(user:str, password:str, key:str) -> dict:
    try:
        enel = Enel(user, password, key, logger)
        enel.authenticate()

        dfEnel = pd.DataFrame(enel.contas())
        dfEnel = dfEnel[["ANO_MES_REF",'SITUACAO','VENCIMENTO','O_DT_PAGTO','MONTANTE','O_COD_BARRAS']]
        dfEnel['VENCIMENTO'] = pd.to_datetime(dfEnel['VENCIMENTO']).astype(str)
        dfEnel['O_DT_PAGTO'] = pd.to_datetime(dfEnel['O_DT_PAGTO'], errors='coerce', format='%Y-%m-%d').astype(str)
        dfEnel = dfEnel.rename({
                        "ANO_MES_REF":"competenciaMesRef",
                        "SITUACAO":"status",
                        "VENCIMENTO":"vencimento",
                        "O_DT_PAGTO":"dtPagamento",
                        "MONTANTE":"valorTotal",
                        "O_COD_BARRAS":"codBoleto",
                    }, axis=1)

        dfFilter = dfEnel[dfEnel['status'] != 'Paga']

        if len(dfFilter.index) > 0:
            record = dfFilter.to_dict(orient='records')
            return record
        else:
            logger.info('Sem faturas!')

    except Exception as e:
        raise e

def main():

    logger.info('Starting Invoices Robot...')
    try:
        currentMonth = datetime.now().month

        brkUser = os.environ['BRK_USER']
        brkPassword = os.environ['BRK_PASSWORD']
        brkRecords= faturaBrk(brkUser, brkPassword)

        enelUser = os.environ['ENEL_USER']
        enelPassword = os.environ['ENEL_PASSWORD']
        enelKey = os.environ['ENEL_KEY']
        enelRecords = faturasEnel(enelUser, enelPassword, enelKey)

        message = ""
        message += "Olá Mestre. 🤖\nSegue seu resumo das cobranças a serem feitas nesse mês!\n\n"

        for record in brkRecords:
            message +=  f"*Brk* 💧\nValor: *R${record['valorTotal']}* \nTipo Pagamento: *Manual* \nVencimento: *{record['vencimento']}* \nStatus: {record['status']} \nBoleto: {record['codBoleto']}\n\n"

        for record in enelRecords:
            message += f"*Enel* 💡\nValor: *R${record['valorTotal']}* \nTipo Pagamento: *Debito Automatico* \nVencimento: *{record['vencimento']}* \nStatus: {record['status']} \nBoleto: {record['codBoleto']}\n\n"

        message += f"*Gympass* 💪\nValor: *R$79,90* \nTipo Pagamento: *Debito Automatico* \nData Cobrança: *2023-{currentMonth}-20*\n\n"
        message += f"*Xbox Gamepass* 🎮\nValor: *R$29,99* \nTipo Pagamento: *Debito Automatico* \nData Cobrança: *2023-{currentMonth}-23*\n\n"
        message += f"*YouTube* ▶\nValor: *R$25,00* \nTipo Pagamento: *Debito Automatico* \nData Cobrança: *2023-{currentMonth}-05*" 
                
        sendMessage(message)

        logger.info('Completed successfully.')

    except Exception as e:
        logger.error(f'Failure Invoices Robot: {e}')
        raise e

    logger.info('Finalizing Invoice Robot.')

if __name__=="__main__":
    main()