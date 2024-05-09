
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import gspread
import plotly.express as px
import plotly.graph_objects as go

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
            df_top5 = df.sort_values(by='Kills', ascending=False).head(5)
            bargraph = px.bar(df_top5, x='Player', y='Kills', title='Top 5 Jogadores com Mais Kills')
            # Selecionar apenas as colunas relevantes para os dois jogadores com mais kills
            df_top2_stats = df[['Player', 'Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']].head(2).copy()

            # Converter as colunas para números
            for col in ['Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']:
                df_top2_stats[col] = pd.to_numeric(df_top2_stats[col], errors='coerce')

            # Categorias para as estatísticas
            categories = ['Kills', 'Knocks', 'Assists', 'Damage Dealt', 'Revives']

            # Criar o gráfico de radar
            fig = go.Figure()

            # Adicionar traços para cada jogador
            for index, row in df_top2_stats.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=row.values[1:].tolist(),
                    theta=categories,
                    fill='toself',
                    name=row['Player']  # Usar o nome do jogador como nome na legenda
                ))

            # Configurações do layout
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, df_top2_stats.iloc[:, 1:].max().max()]
                        # Usar iloc para excluir a coluna 'Player' ao calcular o máximo
                    )
                ),
                showlegend=True
            )

            return render_template('data.html', bargraph=bargraph.to_html(), fig=fig.to_html())
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




if __name__ == "__main__":
    app.run(debug=True)
