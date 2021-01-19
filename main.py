from flask import Flask, render_template, flash, redirect, request, url_for
from services import summary
import os
import secrets
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'documentos/resumos'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
  filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():

  return render_template('index.html')

@app.route('/upload', methods=["GET","POST"])
def upload():

  if 'file' not in request.files:
    flash('Erro no upload', 'alert-danger')
    return redirect(request.url)
  file = request.files['file']

  if file.filename == '':
    flash('Nenhum arquivo selecionado', 'alert-danger')
    return redirect(request.url)
  
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    resumo = summary(path, request.form.get('paragraphs'))
    os.remove(path)
    

    return render_template('resumo.html', resumo=resumo, filename=filename)

if __name__ == '__main__':
  app.run()