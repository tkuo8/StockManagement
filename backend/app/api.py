from flask import Blueprint, request, jsonify
from .service import create_stock, get_all_finance_data_dict, update_stock
from decimal import Decimal
import pdb
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
            Decimal(data["stopLossPrice"]),
        )
        return jsonify({"message": "Stock created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# READ
@bp.route("/stocks", methods=["GET"])
def get_all_stocks():
    # pdb.set_trace()
    try:
        finance_data = get_all_finance_data_dict()
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
    stop_loss_price = data["stopLossPrice"]

    try:
        updated_data_dict = update_stock(
            stock_id, purchase_price, quantity, stop_loss_price
        )
        return jsonify(convert_keys_to_camel_case(updated_data_dict)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
