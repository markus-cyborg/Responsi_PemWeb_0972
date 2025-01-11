import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfigurasi database MariaDB dengan kredensial baru
hostname = "2vgwh.h.filess.io"
database = "Responsi_scaredyard"
port = "3305"
username = "Responsi_scaredyard"
password = "b659a8bd3ea2b44fd40a57b3e51d85bbabc7ebc4"

# Konfigurasi SQLAlchemy untuk Flask
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if not title:
        return redirect(url_for('index'))
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Task.query.get_or_404(id)
    task.title = request.form.get('title')
    if not task.title:
        return redirect(url_for('index'))
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Test koneksi ke database menggunakan mysql.connector
    try:
        connection = mysql.connector.connect(
            host=hostname, database=database, user=username, password=password, port=port
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MariaDB Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Error as e:
        print("Error while connecting to MariaDB", e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MariaDB connection is closed")

    # Membuat tabel jika belum ada
    with app.app_context():
        db.create_all()

    # Menjalankan aplikasi Flask
    app.run(debug=True)
