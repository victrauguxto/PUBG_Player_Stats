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



if __name__ == "__main__":
    app.run(debug=True)
