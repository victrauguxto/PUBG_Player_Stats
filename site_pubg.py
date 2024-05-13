
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import gspread
import plotly.express as px
import re


gc = gspread.service_account(filename='upload/credentials.json')

app = Flask(__name__)

# Lista de planilhas já importadas
planilhas_importadas = []

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/articles")
def articles():

    return render_template('artigos.html')


@app.route("/read_sheets", methods=['GET', 'POST'])
def read_sheets():
    global planilhas_importadas
    if request.method == 'POST':
        link = request.form['sheet_link']
        pagina = request.form['pagina']
        try:
            # Abre a planilha do Google Sheets
            dados = gc.open_by_url(link).worksheet(pagina)
            colunas = dados.get_all_values().pop(0)
            df = pd.DataFrame(data=dados.get_all_values(), columns=colunas)
            df = df.drop(df.index[0])
            # Substituir pontos e vírgulas por nada, converter as colunas para float e tratar valores vazios como 0
            df['Damage Dealt'] = df['Damage Dealt'].str.replace('.', '').str.replace(',', '.').apply(
                lambda x: float(x) if x != '' else 0)
            df['Kills'] = df['Kills'].apply(lambda x: 0 if x == '' else float(x))

            df['Effectiveness'] = df['Damage Dealt'] / df['Kills']
            df_top5 = df.sort_values(by='TWR', ascending=False).head(5)
            df_top5_stats_table = df_top5[['Player','TWR', 'Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']].copy()
            df_top5_stats_table['Damage Dealt'] = df_top5_stats_table['Damage Dealt'] * 1000
            # Selecionar apenas as colunas relevantes para os dois jogadores com mais kills
            df_top5_stats = df_top5[['Player', 'Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']].copy()
            df_top5_stats['Damage Dealt'] = df_top5_stats['Damage Dealt'] * 5
            df_top5_stats['Damage Dealt (normalized)'] = df_top5_stats['Damage Dealt'] / 5

            # Converter as colunas para strings, substituir vírgulas por pontos e converter para float
            for col in ['Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']:
                df_top5_stats[col] = df_top5_stats[col].astype(str).str.replace(',', '.').astype(float)

            # Categorias para as estatísticas
            categories = ['Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']
            # Receber a cor personalizada do formulário
            cor = request.form.get('cor')
            # Verificar se a cor está vazia ou não é uma cor hexadecimal válida
            if not cor or not re.match("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", cor):
                # Cor padrão
                cor = "#ffffff"  # Branco

            # gerar gráficos de barras com cor personalizada
            # Gerar gráficos de barras com cor personalizada
            bargraph = px.bar(df_top5, x='Player', y='Kills', title='Top 5 Kills', color_discrete_sequence=[cor])
            bargraph_DMG = px.bar(df_top5, x='Player', y='Damage Dealt', title='Top 5 DMG', color_discrete_sequence=[cor])
            bargraph_Knocks = px.bar(df_top5, x='Player', y='Knocks', title='Top 5 Knocks', color_discrete_sequence=[cor])
            bargraph_Knocks.update_yaxes(type='linear')

            return render_template('data.html', bargraph=bargraph.to_html(),bargraph_Knocks=bargraph_Knocks.to_html(),bargraph_DMG=bargraph_DMG.to_html(), df_top5_stats_table=df_top5_stats_table, cor=cor)
        except gspread.exceptions.APIError:
            return "Erro ao acessar a planilha. Verifique se o link está correto e se a planilha é compartilhada corretamente."

    return render_template('upload.html', planilhas_importadas=planilhas_importadas)

@app.route('/home_logado')
def home_logado():
    return render_template("homepage_logado.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    nome = request.form.get('username')
    senha = request.form.get('password')

    if nome == "admin" and senha == "123456":
        return render_template('homepage_logado.html', username=nome)
    else:
        return "Usuário Não Encontrado"

@app.route("/How_it_works")
def How_it_works():
    return render_template('How_it_works.html')
@app.route("/privacypolicy")
def privacypolicy():
    return render_template('privacypolicy.html')


if __name__ == "__main__":
    app.run(debug=True)
