from faker import Faker
from modelos.clientes import Cliente
import random
import pandas as pd

fake = Faker ('pt_BR')
clientes=[]

for i in range (50):
     nome= fake.name()
     cpf= fake.cpf()
     idade = random.randint(18, 70)
     sexo = random.choice(['Masculino', 'Feminino'])
     cliente = Cliente(nome,cpf,idade,sexo)
     clientes.append(vars(cliente))
     print(clientes)
     
df=pd.DataFrame(clientes)
print (df)

with pd.ExcelWriter('base_de_clientes.xlsx') as writer:
    df.to_excel(writer, sheet_name='Clientes')
