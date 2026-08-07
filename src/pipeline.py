
from typing import Dict, Any
from src.schemas.state import PipelineState
from src.nodes.triage import execute_triage_node
from src.nodes.retrieval import execute_retrieval_node
from src.nodes.solver import execute_solver_node
from src.nodes.guardrail import execute_guardrail_node

class CustomerActionPipeline:
    def __init__(self, crm_db: Dict[str, Dict[str, Any]], policy_path: str = "data/refund_policy.txt"):
        self.crm_db = crm_db
        self.policy_path = policy_path

    def run(self, customer_email: str) -> PipelineState:
        state = PipelineState(customer_email=customer_email)
        
        # Node 1: Triage
        state.intent = execute_triage_node(state.customer_email)
        
        # Node 2: Retrieval
        order_id = state.intent.order_id if state.intent.order_id else ""
        state.user_data, state.retrieved_policy = execute_retrieval_node(
            order_id=order_id,
            crm_db=self.crm_db,
            policy_path=self.policy_path
        )
        
        # Node 3: Solver
        state.action = execute_solver_node(
            customer_email=state.customer_email,
            intent=state.intent,
            user_data=state.user_data,
            policy_text=state.retrieved_policy
        )
        
        # Node 4: Guardrail Validation
        state.is_valid, state.validation_error = execute_guardrail_node(state)
        
        # Deterministic Fallback Mechanism
        if not state.is_valid:
            state.action.action_type = "escalate_to_human"
            state.action.refund_amount = 0.0
            state.action.email_draft = (
                "Internal System Error: Your request has been flagged for human review. "
                "An agent will be with you shortly."
            )
        
        return state