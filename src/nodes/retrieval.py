from typing import Dict, Any, Tuple

def execute_retrieval_node(
    order_id: str, 
    crm_db: Dict[str, Dict[str, Any]], 
    policy_path: str = "data/refund_policy.txt"
) -> Tuple[Dict[str, Any], str]:
    
    user_data = {}
    if order_id and order_id in crm_db:
        user_data = crm_db[order_id]
        
    try:
        with open(policy_path, "r", encoding="utf-8") as f:
            policy_text = f.read()
    except FileNotFoundError:
        policy_text = "ERROR: Policy document not found."
        
    return user_data, policy_text