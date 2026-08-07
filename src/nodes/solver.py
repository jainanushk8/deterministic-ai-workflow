from datetime import datetime
from typing import Dict, Any
from src.schemas.state import PipelineAction, CustomerIntent
from src.llm.provider import llm_provider

def execute_solver_node(
    customer_email: str,
    intent: CustomerIntent,
    user_data: Dict[str, Any],
    policy_text: str
) -> PipelineAction:
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    system_prompt = (
        "You are an enterprise customer support decision engine. "
        "Your job is to determine the correct action for a customer request "
        "based STRICTLY on the provided Company Policy and the User CRM Data. "
        f"Today's date is {current_date}. Use this to calculate eligibility windows.\n\n"
        "Rules:\n"
        "1. Never authorize a refund exceeding the 'amount_paid' in the CRM data.\n"
        "2. If the user is outside the refund window, you must decline the refund "
        "and select 'reply_only', explaining why based on the policy.\n"
        "3. If the user data is missing or mismatched, select 'escalate_to_human'.\n\n"
        f"Company Policy:\n{policy_text}\n\n"
        f"User CRM Data:\n{user_data}\n"
    )
    
    user_prompt = (
        f"Customer Email: {customer_email}\n"
        f"Intent Summary: {intent.summary}\n"
        "Determine the action and draft the response email."
    )
    
    return llm_provider.generate_structured_output(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_model=PipelineAction
    )