#######################################################################################################################################
##########################################################  LIB's  ####################################################################
#######################################################################################################################################

import pandas as pd
from pathlib import Path
import sqlite3

#######################################################################################################################################
########################################################  Caminhos  ###################################################################
#######################################################################################################################################

project_path = Path.cwd() # Pasta do projeto
database = f'{project_path}\\data\\database.db' # Pasta banco de dados
bases = f'{project_path}\\data\\bases.xlsx' # Planilha com relatórios

#######################################################################################################################################
################################################### lendo base de dados  ##############################################################
#######################################################################################################################################

previsto = pd.read_excel(bases, sheet_name='previsao')
aReceber = pd.read_excel(bases, sheet_name='aReceber')
recebido = pd.read_excel(bases, sheet_name='recebido')
vendas = pd.read_excel(bases, sheet_name='vendas')
cancelamentos = pd.read_excel(bases, sheet_name='cancelamentos')

#######################################################################################################################################
##################################################### Tratando dados ##################################################################
#######################################################################################################################################


previsto = previsto.groupby(['empresa', 'dataPrevista']).sum().reset_index()

aReceber.drop(columns=['idContrato'], inplace=True)
aReceber = aReceber.groupby(['empresa', 'dataVencimento', 'statusParcela']).sum().reset_index()

recebido.drop(columns=['idContrato', 'dataVencimento'], inplace=True)
recebido = recebido.groupby(['empresa', 'dataRecebimento', 'statusRecebimento']).sum().reset_index()

vendas = vendas.groupby(['empresa', 'dataVenda']).sum().reset_index()

cancelamentos = cancelamentos.groupby(['empresa', 'dataCancelamento', 'motivoCancelamento']).count().reset_index()
cancelamentos.rename(columns={'idContrato': 'qtdeCancelada'}, inplace=True)

#######################################################################################################################################
##################################################### Salvando dados ##################################################################
#######################################################################################################################################

db = sqlite3.connect(database=database) #Abrindo conexão com database

previsto.to_sql('previsto', db, index=False, if_exists='replace') # Escrevendo dados no banco de dados
aReceber.to_sql('aReceber', db, index=False, if_exists='replace') # Escrevendo dados no banco de dados
recebido.to_sql('recebido', db, index=False, if_exists='replace') # Escrevendo dados no banco de dados
vendas.to_sql('vendas', db, index=False, if_exists='replace') # Escrevendo dados no banco de dados
cancelamentos.to_sql('cancelamentos', db, index=False, if_exists='replace') # Escrevendo dados no banco de dados

db.close() # Fechando conexão com o banco de dados
