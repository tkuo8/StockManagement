from flask import Blueprint, request, jsonify
from .service import (
    create_stock,
    get_finance_data_dict,
)
from decimal import Decimal
import pdb
from .model import StockStatus
from .util import convert_keys_to_camel_case

bp = Blueprint("main", __name__, url_prefix="/api")


# CREATE
@bp.route("/stocks", methods=["POST"])
def register_stock():

    # pdb.set_trace()

    # HTTPリクエストから値を取得
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json

    try:
        create_stock(
            data["symbol"],
            Decimal(data["purchasePrice"]),
            int(data["quantity"]),
            Decimal(data["targetPrice"]),
            Decimal(data["stopLossPrice"]),
            StockStatus(data["status"]),
        )
        return jsonify({"message": "Stock created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# READ
@bp.route("/stocks", methods=["GET"])
def get_all_stocks():
    # pdb.set_trace()
    try:
        finance_data = get_finance_data_dict()
        json_data = jsonify(convert_keys_to_camel_case(finance_data))
        return json_data, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 個別株グラフデータ
# @bp.route("/stocks/individual_graph", methods=["GET"])
# def get_individual_graph_data():
#     try:
#         ohlc_data = get_individual_stock_graph_dataframe("7203")
#         json_data = ohlc_data.reset_index().to_json(orient="records")
#         return jsonify(json_data), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400


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
