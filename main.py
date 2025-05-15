import pandas as pd
import sqlite3
import logging
from database_utils import *
from validator_utils import *

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("Starting main script.")

    # Load data
    invoices_df = pd.read_csv("invoices_test.csv")
    line_items_df = pd.read_csv("invoice_line_items_test.csv")

    # logging.info("\n===== Invoices Data Preview =====\n%s", invoices_df.head().to_string(index=False))
    # logging.info("\n===== Line Items Data Preview =====\n%s", line_items_df.head().to_string(index=False))

    # Setup DB
    conn = sqlite3.connect("invoice_data.db")
    create_tables(conn)
    invoices_count = insert_invoices(conn, invoices_df)
    line_items_count = insert_line_items(conn, line_items_df)

    logging.info(f"{invoices_count} record inserted in invoices table")
    logging.info(f"{line_items_count} record inserted in line_items table")
 
    conn.commit()
    conn.close()

    # Validate
    validation_results = validate_invoice_totals(invoices_df, line_items_df)
    validation_results.to_csv("invoice_validation_results.csv", index=False)
    logging.info("Validation results written to CSV.")
    logging.info("Script completed.")


if __name__ == "__main__":
    main()
