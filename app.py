from flask import Flask, render_template, url_for, request, redirect
import sqlite3, os.path
from flask_mysqldb import MySQL

app = Flask(__name__)
DATABASE = 'database.db'

mysql = MySQL(app)
app.config['SECRET_KEY'] = 'muitodificil'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_connection()
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.commit() 
    conn.close()
    return render_template('pages/index.html', usuarios=usuarios)

@app.route('/create', methods=['GET','POST'])
def create_user():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_connection()
        conn.execute("INSERT INTO usuarios(nome) VALUES(?)", (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('pages/create-user.html')

@app.route('/createevento', methods=['GET','POST'])
def create_evento():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_connection()
        conn.execute("INSERT INTO evento(nome) VALUES(?)", (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('pages/create-evento.html')

@app.route('/ver')
def ver_user():
    conn = get_connection()
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.commit()
    conn.close()
    return render_template('pages/ver-user.html', usuarios=usuarios)

@app.route('/<int:id>/info', methods=['POST', 'GET'])
def ver(id):

    # obter informação do usuário
    conn = get_connection()
    user = conn.execute('SELECT id, nome FROM usuarios WHERE id == ?', (str(id))).fetchone()
    
    return render_template('pages/user-ver.html', user=user)