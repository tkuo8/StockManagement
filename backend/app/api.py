from flask import Blueprint, request, jsonify
from app.service import create_stock
from decimal import Decimal
import pdb

bp = Blueprint('main', __name__, url_prefix='/api')

# CREATE
@bp.route('/stocks', methods=['POST'])
def register_stock():
    
    # pdb.set_trace()
    
    # HTTPリクエストから値を取得
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.json
    
    # if not symbol or not purchase_price or not quantity or not target_price or not cutloss_price:
    #     return jsonify({'error': 'All are required'}), 400

    try:
        create_stock(data['symbol'], Decimal(data['purchasePrice']), int(data['quantity']), Decimal(data['targetPrice']), Decimal(data['cutlossPrice']))
        return jsonify({'message': 'Stock created successfully'}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
# READ
# @main.route('/users', methods=['GET'])
# def get_users():
#     cursor = mysql.connection.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM users")
#     users = cursor.fetchall()
#     cursor.close()
    
#     return jsonify(users), 200

# # UPDATE
# @main.route('/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     data = request.json
#     name = data.get('name')
#     email = data.get('email')
    
#     cursor = mysql.connection.cursor()
#     cursor.execute(
#         "UPDATE users SET name = %s, email = %s WHERE id = %s",
#         (name, email, user_id)
#     )
#     mysql.connection.commit()
#     cursor.close()
    
#     return jsonify({'message': 'User updated successfully'}), 200

# # DELETE
# @main.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
#     mysql.connection.commit()
#     cursor.close()
    
#     return jsonify({'message': 'User deleted successfully'}), 200
