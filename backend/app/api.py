from flask import Blueprint, request, jsonify
from .service import (
    create_stock,
    get_all_finance_data_dict,
    update_stock,
    get_paginated_finance_data_dict,
    get_total_count,
)
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
        )
        return jsonify({"message": "Stock created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# READ
@bp.route("/stocks", methods=["GET"])
def get_financial_data():
    # pdb.set_trace()
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    total_count = get_total_count()
    total_pages = (total_count + page_size - 1) // page_size
    try:
        finance_data = get_paginated_finance_data_dict(page, page_size)
        json_data = jsonify(
            convert_keys_to_camel_case(
                {
                    "finance_data": finance_data,
                    "current_page": page,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_count": total_count,
                }
            )
        )
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

    try:
        updated_data_dict = update_stock(stock_id, purchase_price, quantity)
        return jsonify(convert_keys_to_camel_case(updated_data_dict)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
