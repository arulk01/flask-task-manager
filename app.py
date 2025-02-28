from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

# Create DB
with app.app_context():
    db.create_all()

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid credentials"}), 401

# Get All Tasks
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description} for t in tasks])

# Add Task
@app.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.json
    new_task = Task(title=data['title'], description=data.get('description', ''))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"})

# Delete Task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted!"})
    return jsonify({"error": "Task not found"}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
