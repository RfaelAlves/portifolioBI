#######################################################################################################################################
##########################################################  LIB's  ####################################################################
#######################################################################################################################################

import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3
import random

#######################################################################################################################################
########################################################  Caminhos  ###################################################################
#######################################################################################################################################

project_path = Path.cwd() # Pasta do projeto
database = f'{project_path}\\data\\database.db' # Pasta banco de dados

#######################################################################################################################################
#####################################################  Gerando dados  #################################################################
#######################################################################################################################################

tamanho_dataSet = 10001 #Definindo quantidade de linhas do dataSet

data_inicio = pd.to_datetime('2023-01-01') # Inicio do periodo das datas aleatórias
data_fim = pd.to_datetime('2024-12-31') # Fim do periodo das datas aleatorias
intervalo = (data_fim - data_inicio).total_seconds() #Diferença das datas convertidas em segundos

# Gerando lista de datas aleatórias
datas_aleatorias = [
    data_inicio + pd.Timedelta(seconds=random.randint(0, int(intervalo)))
    for _ in range(tamanho_dataSet)
]

# Criando tabela de dados
dados_dataSet = {
    'vencimento': datas_aleatorias,
    'empresa': np.random.choice(['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'], tamanho_dataSet),
    'tipoContrato': np.random.randint(1, 3, tamanho_dataSet),
    'Valor': np.random.randint(100, 1000, tamanho_dataSet)
    }

df = pd.DataFrame(dados_dataSet) # Criando dataFarme

db = sqlite3.connect(database=database) #Abrindo conexão com database
df.to_sql('contas_a_receber', db, index=False, if_exists='replace') # Escrevendo dados no banco de dados
db.close() # Fechando conexão com o banco de dados
