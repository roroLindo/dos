from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secreta_chave'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogs.db'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
app.config['MAX_CONTENT_PATH'] = 1024 * 1024  # 1 MB

db = SQLAlchemy(app)

# Garantir que o diretório de upload existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(10))
    porte = db.Column(db.String(20))
    caracteristicas = db.Column(db.String(200))
    local_resgate = db.Column(db.String(100))
    abrigo_atual = db.Column(db.String(100))
    imagem = db.Column(db.String(100))
    raca = db.Column(db.String(50), nullable=True)
    cor = db.Column(db.String(50), nullable=True)
    idade = db.Column(db.String(20), nullable=True)
    data_resgate = db.Column(db.String(20), nullable=True)
    status_adocao = db.Column(db.String(50), nullable=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_dog', methods=['GET', 'POST'])
def add_dog():
    if request.method == 'POST':
        genero = request.form['genero']
        porte = request.form['porte']
        caracteristicas = request.form['caracteristicas']
        local_resgate = request.form['local_resgate']
        abrigo_atual = request.form['abrigo_atual']
        raca = request.form.get('raca')
        cor = request.form.get('cor')
        idade = request.form.get('idade')
        data_resgate = request.form.get('data_resgate')
        status_adocao = request.form.get('status_adocao')

        file = request.files['imagem']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_dog = Dog(
                genero=genero, porte=porte, caracteristicas=caracteristicas, local_resgate=local_resgate,
                abrigo_atual=abrigo_atual, imagem=filename, raca=raca, cor=cor, idade=idade,
                data_resgate=data_resgate, status_adocao=status_adocao
            )
            db.session.add(new_dog)
            db.session.commit()

            return redirect(url_for('view_dogs'))

    return render_template('add_dog.html')


@app.route('/view_dogs', methods=['GET'])
def view_dogs():
    genero = request.args.get('genero')
    porte = request.args.get('porte')
    raca = request.args.get('raca')
    cor = request.args.get('cor')
    idade = request.args.get('idade')
    data_resgate = request.args.get('data_resgate')
    status_adocao = request.args.get('status_adocao')
    local_resgate = request.args.get('local_resgate')

    query = Dog.query

    if genero:
        query = query.filter_by(genero=genero)
    if porte:
        query = query.filter_by(porte=porte)
    if raca:
        query = query.filter_by(raca=raca)
    if cor:
        query = query.filter_by(cor=cor)
    if idade:
        query = query.filter_by(idade=idade)
    if data_resgate:
        query = query.filter_by(data_resgate=data_resgate)
    if status_adocao:
        query = query.filter_by(status_adocao=status_adocao)
    if local_resgate:
        query = query.filter_by(local_resgate=local_resgate)

    dogs = query.all()
    return render_template('view_dogs.html', dogs=dogs)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
