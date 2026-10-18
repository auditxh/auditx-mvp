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
You are an elite enterprise financial auditor and freight contract compliance expert. Analyze this vendor invoice text and generate a professional, structured executive audit report.
Format your output strictly using clean headings, bold labels, and bullet points as follows:
### 📋 Executive Summary
- **Vendor Name:** [Extract Vendor Name]
- **Invoice Number:** [Extract Invoice Number]
- **Purchase Order (PO) Number:** [Extract PO Number or state MISSING]
- **Gross Amount Billed:** [Extract Total Billed Amount]
- **Audit Verdict:** [Approved / Disputed / Short-pay Recommended]

### 🚨 Discrepancy Breakdown & Risk Analysis
List each finding clearly with its financial impact:
- **[Discrepancy Name / Fee Category] ([Dollar Amount]):** 
  - **Issue:** [Clear 1-sentence explanation of why it violates standard terms]
  - **Auditor Finding:** [Operational or mathematical reasoning]

### 💡 Recommended Auditor Action
- **Short-pay / Hold Amount:** [Exact dollar amount to withhold]
- **Required Vendor Action:** [What documentation or correction the vendor must provide before final payout]

Invoice Text:
{extracted_text}
"""

            
            Invoice Text:
            {extracted_text}
            """
            
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt
            )
            
            st.success("Invoice Audit Complete!")
            st.subheader("📊 Audit & Discrepancy Breakdown Report")
            st.write(response.text)
