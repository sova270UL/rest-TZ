from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://post:12345@localhost:5432/TZ_test'
db = SQLAlchemy(app)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(120), nullable=False)
    boolean = db.Column(db.Boolean(), nullable=False)

    def __init__(self, email, password, login, boolean):
        self.email = email
        self.password = password
        self.login = login
        self.boolean = boolean

    def to_json(self):
        return{"email":self.email, "password":self.password, 
               "login": self.login, "boolean": self.boolean}

@app.route('/users', methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    login = request.json['login']
    boolean = request.json['boolean']
    new_user = User(email, password, login, boolean)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_json())

@app.route('/users/id/<id>', methods=['GET'])
def read(id):
    try:
        user = User.query.get(id)
        return jsonify(user.to_json())
    except:
        return jsonify({'message': 'User not found'})
    
@app.route('/users/email/<email>', methods=['GET'])
def read_email(email):
    try:
        user = User.query.filter_by(email = email).first()
        return jsonify(user.to_json())
    except:
        return jsonify({'message': 'User not found'})
    
@app.route('/users', methods=['GET'])
def read_all():
    users = User.query.all()
    return jsonify([e.to_json() for e in users])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
