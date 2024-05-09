import pandas as pd
import gspread

gc = gspread.service_account(filename='credentials.json')

link = str(input("Digite seu link"))

dados = gc.open_by_url(link).worksheet("Karla Cup")

colunas = dados.get_all_values().pop(0)

df = pd.DataFrame(data=dados.get_all_values(), columns=colunas)
df = df.drop(df.index[0])
# Substituir pontos e vírgulas por nada, converter as colunas para float e tratar valores vazios como 0
df['Damage Dealt'] = df['Damage Dealt'].str.replace('.', '').str.replace(',', '.').apply(
lambda x: float(x) if x != '' else 0)
df['Kills'] = df['Kills'].apply(lambda x: 0 if x == '' else float(x))

df['Effectiveness'] = df['Damage Dealt'] / df['Kills']
df_top5 = df.sort_values(by='Kills', ascending=False).head(5)
df_top2 = df.sort_values(by='TWR', ascending=False).head(2)
# Selecionar apenas as colunas relevantes para os dois jogadores com mais kills
df_top2_stats = df_top2[['Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']].copy()
# Categorias para as estatísticas

categories = ['Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']

print(df_top2_stats)