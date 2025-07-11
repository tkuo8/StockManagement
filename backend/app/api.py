from flask import Blueprint, request, jsonify
from .service import (
    create_stock,
    get_all_finance_data_dict,
    update_stock,
    get_target_finance_data_dict,
    get_total_count,
    get_filtered_query,
    update_all_stock_data,
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
    page_size = int(request.args.get("pageSize", 10))
    status = request.args.get("status", "")
    possession = request.args.get("possession", "")
    search_symbol = request.args.get("searchSymbol")

    total_count = get_total_count(get_filtered_query(status, possession, search_symbol))
    total_pages = (total_count + page_size - 1) // page_size

    try:
        finance_data = get_target_finance_data_dict(
            page, status, possession, search_symbol, page_size
        )
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


# UPDATE STOCKS DATA
@bp.route("/stocks/update_all", methods=["GET"])
def update_all_stocks_data():
    # pdb.set_trace()
    try:
        update_all_stock_data()
        return jsonify("update all stocks data is completed."), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
