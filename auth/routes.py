from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from models.user import create_user, get_user_by_email
from config.config import Config
from flask_mysqldb import MySQL

auth_bp = Blueprint('auth', __name__)

mysql = MySQL()


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    hashed_password = generate_password_hash(password)

    existing_user = get_user_by_email(mysql, email)
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    create_user(mysql, username, email, hashed_password)

    return jsonify({'message': 'User registered successfully ✅'}), 201


# Login endpoint
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = get_user_by_email(mysql, email)

    if user and check_password_hash(user[2], password):
        # JWT token generation
        token = jwt.encode({
            'user_id': user[0],  # user id in the payload
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expiration time of 1 hour
        }, Config.JWT_SECRET_KEY, algorithm='HS256')

        return jsonify({
            'message': 'Login successful ✅',
            'token': token  # return the token to the client
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials ❌'}), 401
