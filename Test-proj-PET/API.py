from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from jose import jwt

SECRET_KEY = "thisissecret"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://post:12345@localhost:5432/TZ_test'
db = SQLAlchemy(app)
token = ''


class User(db.Model):
    password = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(120), primary_key=True)

    def __init__(self, password, username):
        self.password = password
        self.username = username

@app.route('/register', methods=['POST'])
def register():
    '''{"username": "string", "password": "string"}'''
    password = request.json['password']
    username = request.json['username']
    if username in User.query.all():
        return jsonify({'message': 'User already exists'})
    else:
        hash_password = pbkdf2_sha256.hash(password)
        new_user = User(hash_password, username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"})
    
@app.route('/login', methods=['POST'])
def login():
    '''{"username": "string", "password": "string"}'''
    global token
    password = request.json['password']
    username = request.json['username']
    if User.query.filter_by(username = username).first() != None:
        user = User.query.filter_by(username = username).first()
        if pbkdf2_sha256.verify(password, user.password):
            token = jwt.encode({"username": username}, SECRET_KEY, algorithm='HS256')
            return jsonify({"access_token": "string","token_type": "bearer"})
        else:
            return jsonify({'message': 'Wrong password'})
    else: return jsonify({'message':"Invalid username or password"})
        
@app.route('/users/me', methods=['GET'])
def me():
    global token
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
