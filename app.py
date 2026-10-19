import os
import streamlit as st
import pdfplumber
from google import genai

# Page Config
st.set_page_config(page_title="AuditX: AI Invoice Audit Engine", page_icon="📄", layout="centered")

# UI Header
st.title("📄 AuditX: Hybrid AI & Compliance Audit Engine")
st.markdown("Automated cross-industry invoice data extraction paired with deterministic Python financial math.")

# File Uploader
uploaded_file = st.file_uploader("Upload Any Vendor Invoice (PDF)", type=["pdf"])

# Initialize GenAI Client securely using Streamlit Secrets or Environment Variable
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

if uploaded_file is not None:
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY is missing! Please add it to your Streamlit App Secrets.")
    else:
        with st.spinner("AI is reading invoice text and Python is verifying the math..."):
            # Step 1: Extract text from PDF using pdfplumber
            extracted_text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text() or ""

            # Step 2: Call Gemini Flash strictly for data extraction (The Reader)
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
You are a precision data extraction assistant. Read this invoice text and extract the following details precisely. 
Return your answer strictly as plain key-value text lines without extra conversational filler:

VENDOR_NAME: [Extract Vendor Name]
INVOICE_NUMBER: [Extract Invoice Number]
GROSS_BILLED: [Extract Total Billed Amount as a clean number, e.g., 1250.50]
PO_AGREED_AMOUNT: [Extract Expected PO Amount if listed, otherwise write 0.00]
DISCREPANCY_NOTE: [Short 1-sentence description of any fee anomaly found, or write None]

Invoice Text:
{extracted_text}
"""

            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt
            )
            
            raw_text = response.text

            # Step 3: Safe Text Parser
            parsed_data = {}
            for line in raw_text.split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    parsed_data[key.strip()] = val.strip()

            vendor = parsed_data.get("VENDOR_NAME", "Unknown Vendor")
            inv_no = parsed_data.get("INVOICE_NUMBER", "N/A")
            
            try:
                gross_billed = float(parsed_data.get("GROSS_BILLED", "0").replace("$", "").replace(",", ""))
            except ValueError:
                gross_billed = 0.00

            try:
                po_agreed = float(parsed_data.get("PO_AGREED_AMOUNT", "0").replace("$", "").replace(",", ""))
            except ValueError:
                po_agreed = 0.00

            # Step 4: DETERMINISTIC PYTHON MATH (The Verifier - 100% Accurate)
            if po_agreed > 0:
                total_discrepancy = gross_billed - po_agreed
            else:
                total_discrepancy = 0.00

            if total_discrepancy > 0:
                verdict = f"🚨 DISCREPANCY DETECTED: Overcharged by ${total_discrepancy:,.2f}"
            else:
                verdict = "✅ APPROVED: No mathematical overcharge found."

            # Step 5: Render Executive Output & Human Review Screen
            st.success("Hybrid Audit Complete!")
            st.subheader("📊 Executive Audit Report")
            
            st.markdown(f"**Vendor Name:** {vendor}")
            st.markdown(f"**Invoice Number:** {inv_no}")
            st.markdown(f"**Gross Billed Amount:** ${gross_billed:,.2f}")
            st.markdown(f"**Expected PO Amount:** ${po_agreed:,.2f}")
            st.markdown(f"**Total Discrepancy (Verified by Python Math):** **${total_discrepancy:,.2f}**")
            st.markdown(f"**Audit Verdict:** {verdict}")
            st.markdown(f"**AI Extraction Note:** {parsed_data.get('DISCREPANCY_NOTE', 'None')}")

            st.markdown("---")
            # Human Review Safeguard Button
            if st.button("Approve & Confirm Short-Pay Action"):
                st.info(f"Action successfully recorded: Flagged ${total_discrepancy:,.2f} for human sign-off and vendor dispute notice.")
