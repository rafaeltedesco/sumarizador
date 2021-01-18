from flask import Flask, render_template, flash, redirect, request, url_for
from services import summary
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'documentos/resumos'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcajsdjalksd'

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
    

    return render_template('resumo.html', resumo=resumo, filename=filename)

app.run(debug=True, host='0.0.0.0')