from flask import Blueprint, request, jsonify
from .extensions import mysql

main = Blueprint('main', __name__)

# CREATE
@main.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'User created successfully'}), 201

# READ
@main.route('/users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    
    return jsonify(users), 200

# UPDATE
@main.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        (name, email, user_id)
    )
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'User updated successfully'}), 200

# DELETE
@main.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'User deleted successfully'}), 200
