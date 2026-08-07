from src.schemas.state import CustomerIntent
from src.llm.provider import llm_provider

def execute_triage_node(customer_email_text: str) -> CustomerIntent:
    system_prompt = (
        "You are a strict data extraction system for a customer support pipeline. "
        "Analyze the provided customer email and extract the intent, sentiment, "
        "summary, and any mentioned Order ID (formatted as ORD-XXXX). "
        "If no Order ID is found, return null for order_id."
    )
    
    return llm_provider.generate_structured_output(
        system_prompt=system_prompt,
        user_prompt=customer_email_text,
        response_model=CustomerIntent
    )