from src.schemas.state import PipelineState, PipelineAction
from src.nodes.guardrail import execute_guardrail_node

def test_guardrail_blocks_excessive_refund():
    state = PipelineState(
        customer_email="Please refund my order.",
        user_data={"amount_paid": 100.00},
        action=PipelineAction(
            action_type="issue_refund",
            refund_amount=500.00,
            email_draft="We have refunded $500 to your account.",
            confidence_score=0.9
        )
    )
    
    is_valid, error_msg = execute_guardrail_node(state)
    
    assert is_valid is False
    assert "exceeds amount paid" in error_msg

def test_guardrail_passes_valid_refund():
    state = PipelineState(
        customer_email="Please refund my order.",
        user_data={"amount_paid": 100.00},
        action=PipelineAction(
            action_type="issue_refund",
            refund_amount=100.00,
            email_draft="We have refunded $100 to your account.",
            confidence_score=0.95
        )
    )
    
    is_valid, error_msg = execute_guardrail_node(state)
    
    assert is_valid is True
    assert error_msg == ""

def test_guardrail_blocks_refund_on_reply_action():
    state = PipelineState(
        customer_email="Where is my order?",
        user_data={"amount_paid": 100.00},
        action=PipelineAction(
            action_type="reply_only",
            refund_amount=50.00,
            email_draft="Your order is on the way.",
            confidence_score=0.9
        )
    )
    
    is_valid, error_msg = execute_guardrail_node(state)
    
    assert is_valid is False
    assert "Logic error" in error_msg