from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import gspread

gc = gspread.service_account(filename='upload/credentials.json')

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/articles")
def articles():
    return render_template('artigos.html')

@app.route("/read_sheets", methods=['GET', 'POST'])
def read_sheets():
    if request.method == 'POST':
        link = request.form['sheet_link']
        try:
            # Abre a planilha do Google Sheets
            dados = gc.open_by_url(link).worksheet("Sheet1")
            colunas = dados.get_all_values().pop(0)
            df = pd.DataFrame(data=dados.get_all_values(), columns=colunas)
            df = df.drop(df.index[0])

            # Convert DataFrame para formato de tabela HTML
            html_table = df.to_html(index=False, header=True)


            return render_template('data.html', table_data=html_table)
        except gspread.exceptions.APIError:
            return "Erro ao acessar a planilha. Verifique se o link está correto e se a planilha é compartilhada corretamente."

    return render_template('upload.html')




@app.route('/home_logado')
def home_logado():
    return render_template("homepage_logado.html")

@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('username')
    senha = request.form.get('password')

    if nome == "admin" and senha == "123456":
        return render_template('homepage_logado.html', username=nome)
    else:
        return "Usuário Não Encontrado"

if __name__ == "__main__":
    app.run(debug=True)
