from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Konfigurasi database MariaDB untuk SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://Responsi0972_rubberdark:209fd4754cb6b52c80b773bdb355fdaf320010f1'
    '@2wxsc.h.filess.io:3305/Responsi0972_rubberdark'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi SQLAlchemy
db = SQLAlchemy(app)

# Model database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# Fungsi untuk koneksi langsung menggunakan mysql.connector
def connect_directly():
    hostname = "2wxsc.h.filess.io"
    database = "Responsi0972_rubberdark"
    port = "3305"
    username = "Responsi0972_rubberdark"
    password = "209fd4754cb6b52c80b773bdb355fdaf320010f1"

    try:
        connection = mysql.connector.connect(
            host=hostname, database=database, user=username, password=password, port=port
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MariaDB Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Error as e:
        print("Error while connecting to MariaDB", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MariaDB connection is closed")

# Routes
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Task.query.get(id)
    task.title = request.form.get('title')
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Koneksi langsung ke MariaDB untuk pengujian
    connect_directly()

    # Inisialisasi tabel database melalui SQLAlchemy
    with app.app_context():
        db.create_all()

    # Jalankan aplikasi Flask
    app.run(debug=True)
