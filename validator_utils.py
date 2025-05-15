import numpy as np
import pandas as pd
import logging


def validate_invoice_totals(invoices_df, line_items_df):

    logging.info("Validating invoice totals.")

    # Step 1: Calculate line total
    line_items_df['line_total'] = line_items_df['line_rate'] * line_items_df['line_quantity']

    # Step 2: Aggregate total per invoice
    totals = line_items_df.groupby('invoice_id')['line_total'].sum().reset_index()

    # Step 3: Merge with invoice-level declared totals
    merged = pd.merge(invoices_df, totals, on='invoice_id', how='left')

    # Step 4: Compare totals
    merged['is_total_matching'] = np.isclose(merged['total'], merged['line_total'], atol=0.01)

    # Step 5: Separate matched and mismatched
    mismatches = merged[~merged['is_total_matching']]
    matches = merged[merged['is_total_matching']]

    # Step 6: Logging + Printing
    logging.info(f"Validation completed: {len(matches)} matched, {len(mismatches)} mismatched.")

    # if not matches.empty:
    #     print("\nMatched Invoices:")
    #     print(matches[['invoice_id', 'total', 'line_total']].to_string(index=False))

    # if not mismatches.empty:
    #     print("\nMismatched Invoices:")
    #     print(mismatches[['invoice_id', 'total', 'line_total']].to_string(index=False))

    return merged[['invoice_id', 'total', 'line_total', 'is_total_matching']]
