# Invoice & Line Item Processor

This project allows you to:
- Load and process invoice and line item data from CSV files (in bulk)
- Automatically classify line items into categories (e.g., coaching, shipping, etc.)
- Insert data into a local SQLite database (`invoice_data.db`)
- Submit data via API endpoints for single or multiple records

---

## 1. Setup Instructions

### 📦 Create and Activate Virtual Environment

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

## 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

## 3. Run the Bulk Processing Script
Use this to load data from CSV files and insert into the database.

```bash
python main.py
```
What it does:

Loads invoices_test.csv and invoice_line_items_test.csv

Inserts invoice and line item data into SQLite

Automatically classifies each line item and stores the result

Saves a validation report to invoice_validation_results.csv

## 4. Run the API Server
Start the Flask API to insert data dynamically via HTTP:
```bash
python api.py
```
The server will run at:
```bash
http://localhost:5000
```

## 5. API Endpoints

### POST /invoices
Insert one or multiple invoices.

Example JSON (single invoice):
```bash
{
  "invoice_id": 1001,
  "date_created": "2025-05-15",
  "sale_description": "Advanced Coaching Program",
  "brand_name": "Coaching Inc",
  "coach": "Jane Smith",
  "invoice_status_str": "paid",
  "total": 2250.00,
  "invoice_date": "2025-06-01"
}
```
Or an array of multiple invoices:
```bash
[
  {
    "invoice_id": 1002,
    "date_created": "2025-05-16",
    "sale_description": "Shipping & Handling",
    "brand_name": "LogiCorp",
    "coach": "N/A",
    "invoice_status_str": "sent",
    "total": 150.00,
    "invoice_date": "2025-06-05"
  }
]

```
### POST /line_items
Insert one or multiple line items. Each line item is automatically classified and stored in both raw and transformed tables.

Example JSON (single line item):
```bash
{
  "id": 501,
  "invoice_id": 1001,
  "item_name": "Ambassador Coaching Program",
  "line_rate": 750,
  "line_quantity": 1,
  "created_at": "2025-05-15T09:00:00Z"
}
```
Multiple line items:
```bash
[
  {
    "id": 502,
    "invoice_id": 1001,
    "item_name": "Shipping Box",
    "line_rate": 30,
    "line_quantity": 2,
    "created_at": "2025-05-15T09:05:00Z"
  },
  {
    "id": 503,
    "invoice_id": 1001,
    "item_name": "Rollover Coaching Session",
    "line_rate": 300,
    "line_quantity": 1,
    "created_at": "2025-05-15T09:10:00Z"
  }
]

```