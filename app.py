import os
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="AuditX - Freight Invoice Auditor",
    page_icon="🔍",
    layout="centered"
)

# 1. Fetch OpenRouter API Key safely from Secrets or Environment Variables
api_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")

# Title and description
st.title("🔍 AuditX: AI Freight Invoice Auditor")
st.write("Upload your carrier invoice PDF to automatically check for rate errors and overcharges.")

# Fallback check if API key is missing in Streamlit Secrets dashboard
if not api_key:
    st.error("⚠️ System Configuration Alert: OpenRouter API key is missing from Streamlit Secrets. Please add OPENROUTER_API_KEY in the Secrets panel.")

# File uploader widget
uploaded_file = st.file_uploader("Upload Freight Invoice (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    
    if st.button("Run Audit"):
        if not api_key:
            st.error("Cannot proceed without a configured API Key in Streamlit Secrets.")
        else:
            with st.spinner("Analyzing line items, fuel surcharges, and contract rates..."):
                # Insert your PDF parsing and LLM audit logic here
                # Example:
                # result = run_invoice_audit(uploaded_file, api_key)
                
                st.subheader("Audit Results Summary")
                st.success("Audit Complete!")
                st.write("Average discrepancy detected: **$285.00** in unverified fuel surcharges.")

