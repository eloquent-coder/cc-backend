from flask import Flask, request, jsonify
import pandas as pd
import sqlite3
import logging
from database_utils import insert_invoices, insert_line_items

app = Flask(__name__)
DATABASE = "invoice_data.db"

# Setup logging
logging.basicConfig(level=logging.INFO)

def get_db_connection():
    return sqlite3.connect(DATABASE)


@app.route("/invoices", methods=["POST"])
def add_invoices():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    # Support both single and multiple invoices
    if isinstance(data, dict):
        data = [data]

    try:
        df = pd.DataFrame(data)
        conn = get_db_connection()
        inserted_count = insert_invoices(conn, df)
        conn.commit()
        conn.close()

        if inserted_count == 0:
            return jsonify({"warning": "No invoices inserted. Data may be invalid or already exist."}), 400

        return jsonify({"message": f"{inserted_count} invoice(s) inserted successfully."}), 201

    except Exception as e:
        logging.exception("Failed to insert invoice(s)")
        return jsonify({"error": str(e)}), 500


@app.route("/line_items", methods=["POST"])
def add_line_items():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    if isinstance(data, dict):
        data = [data]

    try:
        df = pd.DataFrame(data)
        conn = get_db_connection()
        inserted_count = insert_line_items(conn, df)
        conn.commit()
        conn.close()

        if inserted_count == 0:
            return jsonify({"warning": "No line items inserted. Data may be invalid or already exist."}), 400

        return jsonify({"message": f"{inserted_count} line item(s) inserted successfully (and transformed)."}), 201

    except Exception as e:
        logging.exception("Failed to insert line item(s)")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


if __name__ == "__main__":
    app.run(debug=True)
