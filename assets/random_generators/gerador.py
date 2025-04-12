import pandas as pd
import random
from datetime import datetime, timedelta
from modelos.clientes import Cliente

def horario_aleatorio():
    hora = random.randint(10, 22)
    minuto = random.randint(0, 59)
    return f'{hora:2d}:{minuto:2d}'


file_path = './assets/base_de_clientes.xlsx'
df= pd.read_excel(file_path)

clientes=[]
vendas = []
vendedores = ['Eduarda Felipa Bittencourt', 'Lorelai Rodrigues', 'Gisele Castro', 'Abel Marques', 'Rosalia Vila', 'Raul Alexandre']

for _, row in df.iterrows():
    cliente = Cliente(row['nome'],row['cpf'],row['idade'],row['sexo'])
    clientes.append(vars(cliente))

# Gerando dados para 90 dias
for _ in range(90*30):
    nome_cliente_dict = random.choice(clientes)
    nome_cliente = nome_cliente_dict['nome']
    cpf_cliente = nome_cliente_dict['cpf']
    idade_cliente = nome_cliente_dict['idade']
    sexo_cliente = nome_cliente_dict['sexo']
    quantidade_pecas = random.choices(range(1, 16), weights=[10]*4+[5]+[1]*10, k=1)[0]
    valor_compra = round(random.uniform(100, 1500) * quantidade_pecas, 2)
    desconto_compra = random.randint(1,10)
    nome_vendedor = random.choice(vendedores)
    data_compra = (datetime.now() - timedelta(days=random.randint(0, 90))).date()
    horario_compra = horario_aleatorio()
    vendas.append([nome_cliente, cpf_cliente, idade_cliente, sexo_cliente, quantidade_pecas, valor_compra,desconto_compra, nome_vendedor, data_compra, horario_compra])

df1  = pd.DataFrame(vendas, columns=['Nome do Cliente', 'CPF do Cliente', 'Idade do Cliente', 'Sexo do Cliente', 'Quantidade de Peças', 'Valor da Compra','Desconto (%)', 'Nome do Vendedor', 'Data da Compra', 'Horário da Compra'])

with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='vendas')

