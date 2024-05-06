from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Markup, send_from_directory, escape
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
        return render_template('upload2.html')
    else:
        return render_template('upload.html')




if __name__ == "__main__":
    app.run(debug=True)
