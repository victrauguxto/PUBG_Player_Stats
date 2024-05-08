import pandas as pd
import gspread

gc = gspread.service_account(filename='credentials.json')

link = str(input("Digite seu link"))

dados = gc.open_by_url(link).worksheet("Sheet1")

colunas = dados.get_all_values().pop(0)

df = pd.DataFrame(data= dados.get_all_values(), columns=colunas )

print(df)