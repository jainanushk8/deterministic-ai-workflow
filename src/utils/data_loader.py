import csv
from typing import Dict, Any

def load_crm_data_from_csv(file_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Loads customer support tickets from the Kaggle dataset.
    Generates a synthetic Order ID and amount_paid for pipeline validation.
    """
    crm_db = {}
    
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for index, row in enumerate(reader, start=1):
                order_id = f"ORD-{index:04d}"
                
                crm_db[order_id] = {
                    "customer_name": row.get('Customer Name', 'Unknown'),
                    "customer_email": row.get('Customer Email', 'Unknown'),
                    "product_purchased": row.get('Product Purchased', 'Unknown'),
                    "date_of_purchase": row.get('Date of Purchase', '2026-01-01'),
                    "ticket_description": row.get('Ticket Description', 'No description provided.'),
                    "amount_paid": 299.99 
                }
        return crm_db
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found at path: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error parsing CSV dataset: {str(e)}")