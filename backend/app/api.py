from flask import Blueprint, request, jsonify
from .service import create_stock, get_finance_data_dict, update_stock
from decimal import Decimal
import pdb
from .model import StockStatus
from .util import model_to_dict, convert_keys_to_camel_case

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


# UPDATE
@bp.route("/stocks/<int:stock_id>", methods=["PUT"])
def put_stock(stock_id):
    # pdb.set_trace()
    data = request.json

    purchase_price = data["purchasePrice"]
    quantity = data["quantity"]
    target_price = data["targetPrice"]
    stop_loss_price = data["stopLossPrice"]

    try:
        updated_data = update_stock(
            stock_id, purchase_price, quantity, target_price, stop_loss_price
        )
        return jsonify(convert_keys_to_camel_case(model_to_dict(updated_data))), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# # DELETE
# @main.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
#     mysql.connection.commit()
#     cursor.close()

#     return jsonify({'message': 'User deleted successfully'}), 200
