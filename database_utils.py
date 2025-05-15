import sqlite3
import logging
import pandas as pd
from transformation_utils import classify_item

def create_tables(conn):
    logging.info("Creating tables in the database if they don't already exist.")

    cursor = conn.cursor()

    # Create invoices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY,
            date_created TEXT,
            sale_description TEXT,
            brand_name TEXT,
            coach TEXT,
            invoice_status_str TEXT,
            total REAL,
            invoice_date TEXT
        )
    """)

    # Create raw line items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_line_items (
            id INTEGER PRIMARY KEY,
            invoice_id INTEGER,
            item_name TEXT,
            line_rate REAL,
            line_quantity REAL,
            created_at TEXT,
            FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id)
        )
    """)

    # Create transformed line items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transformed_line_items (
            id INTEGER PRIMARY KEY,
            invoice_id INTEGER,
            item_name TEXT,
            line_rate REAL,
            line_quantity REAL,
            created_at TEXT,
            category TEXT,
            FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id)
        )
    """)

    conn.commit()
    logging.info("Table creation completed. Existing tables were preserved.")


def insert_invoices(conn, invoices_df):
    logging.info("Inserting invoices...")
    cursor = conn.cursor()
    success_count = 0

    for _, row in invoices_df.iterrows():
        try:
            row = row.fillna('')
            values = (
                int(row['invoice_id']),
                str(row['date_created']),
                str(row['sale_description']),
                str(row['brand_name']),
                str(row['coach']),
                str(row['invoice_status_str']),
                float(row['total']) if row['total'] != '' else None,
                str(row['invoice_date']),
            )
            cursor.execute("""
                INSERT OR IGNORE INTO invoices (
                    invoice_id, date_created, sale_description, brand_name,
                    coach, invoice_status_str, total, invoice_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, values)
            if cursor.rowcount > 0:
                success_count += 1
        except Exception as e:
            logging.error(f"Error inserting invoice row: {row.to_dict()}")
            logging.exception(e)

    return success_count


from transformation_utils import classify_item

def insert_line_items(conn, line_items_df):
    logging.info("Inserting invoice line items (with transformation)...")
    cursor = conn.cursor()
    success_count = 0

    for _, row in line_items_df.iterrows():
        try:
            row = row.fillna('')

            # Prepare raw line item
            raw_values = (
                int(row['id']),
                int(row['invoice_id']),
                str(row['item_name']),
                float(row['line_rate']) if row['line_rate'] != '' else None,
                float(row['line_quantity']) if row['line_quantity'] != '' else None,
                str(row['created_at']),
            )

            cursor.execute("""
                INSERT OR IGNORE INTO invoice_line_items (
                    id, invoice_id, item_name, line_rate,
                    line_quantity, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, raw_values)

            # Insert into transformed line items
            category = classify_item(str(row['item_name']))
            transformed_values = raw_values + (category,)

            cursor.execute("""
                INSERT OR IGNORE INTO transformed_line_items (
                    id, invoice_id, item_name, line_rate,
                    line_quantity, created_at, category
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, transformed_values)

            if cursor.rowcount > 0:
                success_count += 1

        except Exception as e:
            logging.error(f"Error inserting line item row: {row.to_dict()}")
            logging.exception(e)

    return success_count
