import streamlit as st
from src.utils.data_loader import load_crm_data_from_csv
from src.pipeline import CustomerActionPipeline

st.set_page_config(page_title="Agentic Pipeline Demo", layout="wide")

@st.cache_data
def load_data():
    return load_crm_data_from_csv("data/customer_support_tickets.csv")

def main():
    st.title("Zero-Hallucination Customer Action Pipeline")
    st.markdown("Enterprise-grade deterministic AI routing and response generation.")

    with st.spinner("Loading CRM Database..."):
        crm_db = load_data()
    
    st.sidebar.header("System Status")
    st.sidebar.text(f"CRM Records Loaded: {len(crm_db)}")
    st.sidebar.text("LLM Engine: Groq / Llama-3")
    st.sidebar.text("Guardrail: Deterministic Python")
    
    st.subheader("Incoming Customer Request")
    default_email = (
        "Hello, I purchased a product recently (Order ID: ORD-0001) but I am not satisfied "
        "with how it works. I would like to request a $500 refund immediately. "
        "Please let me know how to proceed."
    )
    
    customer_email = st.text_area("Customer Email payload", value=default_email, height=150)
    
    if st.button("Execute Pipeline", type="primary"):
        pipeline = CustomerActionPipeline(crm_db=crm_db)
        
        st.markdown("---")
        st.subheader("Execution State")
        
        with st.status("Running pipeline nodes...", expanded=True) as status:
            st.write("Executing Triage Node (Classification & Extraction)...")
            st.write("Executing Retrieval Node (CSV & Policy Lookup)...")
            st.write("Executing Solver Node (Reasoning Engine)...")
            st.write("Executing Guardrail Node (Deterministic Validation)...")
            
            final_state = pipeline.run(customer_email)
            status.update(label="Pipeline Execution Complete", state="complete", expanded=False)
        
        st.markdown("---")
        st.subheader("Execution Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            action_val = final_state.action.action_type if final_state.action else "None"
            st.metric(label="System Action Executed", value=action_val)
            
        with col2:
            refund_val = f"${final_state.action.refund_amount}" if final_state.action else "$0.0"
            st.metric(label="Authorized Refund", value=refund_val)
            
        with col3:
            guardrail_val = "Passed" if final_state.is_valid else "Failed"
            st.metric(label="Guardrail Status", value=guardrail_val)
            
        if not final_state.is_valid:
            st.error(f"Guardrail Intervention Triggered: {final_state.validation_error}")
        else:
            st.success("Guardrail check passed. No logic violations detected.")
        
        st.subheader("Generated Customer Communication")
        if final_state.action:
            st.info(final_state.action.email_draft)
        
        with st.expander("View Raw System State Pipeline Dump"):
            st.json(final_state.model_dump())

if __name__ == "__main__":
    main()