from flask import Flask, request, render_template, redirect
import pandas as pd
import os
from werkzeug.utils import secure_filename

upload_folder = os.path.join(os.getcwd(), 'upload')

app = Flask(__name__)


# Criando a home
@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/articles")
def articles():
    return render_template('artigos.html')

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['planilha_dados']
        savepath = os.path.join(upload_folder, secure_filename(file.filename))
        file.save(savepath)
        files = os.listdir(upload_folder)
        return render_template('upload2.html', files=files)
    else:
        return render_template('upload.html')

@app.route('/home_logado')
def home_logado():
    return render_template("homepage_logado.html")

@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('username')
    senha = request.form.get('password')

    if nome == "admin" and senha == "123456":
        return render_template('homepage_logado.html', username = nome)
    else:
        return "Usuário Não Encontrado"


if __name__ == "__main__":
    app.run(debug=True)
