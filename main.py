import json
from src.utils.data_loader import load_crm_data_from_csv
from src.pipeline import CustomerActionPipeline

def main():
    print("Loading CRM Dataset...")
    try:
        crm_db = load_crm_data_from_csv("data/customer_support_tickets.csv")
        print(f"Successfully loaded CRM data. Found {len(crm_db)} records.")
    except Exception as e:
        print(f"Initialization Error: {e}")
        return

    pipeline = CustomerActionPipeline(crm_db=crm_db)
    
    # We use ORD-0001, which maps to the first row of our Kaggle CSV dataset
    test_email = (
        "Hello, I purchased a product recently (Order ID: ORD-0001) but I am not satisfied "
        "with how it works. I would like to request a full refund immediately. "
        "Please let me know how to proceed."
    )
    
    print("\nExecuting Zero-Hallucination Pipeline...")
    print("-" * 40)
    
    final_state = pipeline.run(test_email)
    
    print("Execution Complete.\n")
    print("--- Pipeline State Dump ---")
    
    if final_state.intent:
        print(f"Extracted Intent Category : {final_state.intent.category}")
        print(f"Extracted Order ID      : {final_state.intent.order_id}")
    
    if final_state.action:
        print(f"Guardrail Passed        : {final_state.is_valid}")
        if not final_state.is_valid:
            print(f"Guardrail Failure Reason: {final_state.validation_error}")
            
        print(f"Final Action Selected   : {final_state.action.action_type}")
        print(f"Final Refund Amount     : ${final_state.action.refund_amount}")
        print(f"\nGenerated Email Draft:\n\n{final_state.action.email_draft}")

if __name__ == "__main__":
    main()