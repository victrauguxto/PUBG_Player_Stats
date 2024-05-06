from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import os

app = Flask(__name__)


# Criando a home
@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/articles")
def articles():
    return "Bem vindo à página de artigos"


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Seu código de processamento de upload aqui
        return 'Arquivo enviado com sucesso'
    else:
        # Se necessário, tratar outros métodos HTTP
        return 'Método não permitido'


    pd.readexcel(file)
    # Por exemplo, gerar um gráfico a partir dos dados
    # Aqui estamos apenas exibindo os primeiros registros do DataFrame
    return df.head().to_html()


if __name__ == "__main__":
    app.run(debug=True)
