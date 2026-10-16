import os
import streamlit as st
import pdfplumber
from google import genai

# Page Config
st.set_page_config(page_title="AuditX: AI Invoice Audit Engine", page_icon="📄", layout="centered")

# UI Header - Updated for Universal B2B
st.title("📄 AuditX: AI Invoice Audit Engine")
st.markdown("Automated financial data validation and discrepancy detection for enterprise invoices across any industry.")

# File Uploader
uploaded_file = st.file_uploader("Upload Any Vendor Invoice (PDF)", type=["pdf"])

# Initialize GenAI Client securely using Streamlit Secrets or Environment Variable
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

if uploaded_file is not None:
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY is missing! Please add it to your Streamlit App Secrets.")
    else:
        with st.spinner("AI is analyzing invoice and cross-referencing discrepancies..."):
            # Extract text from PDF using pdfplumber
            extracted_text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text() or ""
            
            # Call Free Gemini Flash API
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an expert enterprise financial auditor. Analyze this invoice text and identify any pricing discrepancies, unauthorized tax, or line-item variances.
            Return the output cleanly with:
            - Vendor Name
            - Invoice Number
            - Purchase Order (PO) Number
            - Gross Amount Billed
            - Discrepancy Breakdown / Variances Found
            
            Invoice Text:
            {extracted_text}
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            st.success("Invoice Audit Complete!")
            st.subheader("📊 Audit & Discrepancy Breakdown Report")
            st.write(response.text)
