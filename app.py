# app.py
from flask import Flask
from flask_mysqldb import MySQL
from config.config import Config
from auth.routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
