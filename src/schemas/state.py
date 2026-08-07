
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any

class CustomerIntent(BaseModel):
    category: Literal["refund", "technical_support", "general_inquiry"] = Field(
        description="The category of the customer request."
    )
    order_id: Optional[str] = Field(
        default=None, 
        description="The order ID if mentioned in the email."
    )
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="Overall sentiment of the customer."
    )
    summary: str = Field(
        description="A concise one-sentence summary of the request."
    )

class PipelineAction(BaseModel):
    action_type: Literal["issue_refund", "escalate_to_human", "reply_only"] = Field(
        description="The deterministic action the pipeline should execute."
    )
    refund_amount: float = Field(
        default=0.0, 
        description="The exact monetary amount to refund, if applicable."
    )
    email_draft: str = Field(
        description="The draft response to send to the customer."
    )
    confidence_score: float = Field(
        description="Confidence in the chosen action from 0.0 to 1.0."
    )

class PipelineState(BaseModel):
    customer_email: str
    intent: Optional[CustomerIntent] = None
    retrieved_policy: str = ""
    user_data: Dict[str, Any] = Field(default_factory=dict)
    action: Optional[PipelineAction] = None
    is_valid: bool = False
    validation_error: Optional[str] = None