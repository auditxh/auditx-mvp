import streamlit as st
import pypdf
import re

# Page Configuration
st.set_page_config(page_title="AuditX - Freight Audit Engine", page_icon="🚛", layout="wide")

st.title("🚛 AuditX: Freight Invoice Audit Engine")
st.caption("Automated weight & invoice discrepancy detection for enterprise logistics.")

# 1. Baseline Rules / Contract Cards
AGREED_WEIGHT_KG = 850.0  # Agreed gross weight baseline
AGREED_RATE_PER_KG = 2.50 # Agreed contract rate baseline

# 2. PDF Text Extraction Function
def extract_text_from_pdf(pdf_file):
    try:
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""

# 3. File Uploader
uploaded_file = st.file_uploader("Upload Freight Invoice (PDF)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analyzing PDF for discrepancies..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        
        # --- Parsing Logic ---
        # Search for billed weight (e.g., "1,200 kg" or "1200 kg")
        weight_match = re.search(r"(\d+[\d,]*)\s*kg", pdf_text, re.IGNORECASE)
        billed_weight = float(weight_match.group(1).replace(",", "")) if weight_match else AGREED_WEIGHT_KG

        # Search for total billed amount
        total_match = re.search(r"TOTAL DUE:\s*\$?([\d,]+\.\d{2})", pdf_text, re.IGNORECASE)
        total_billed = float(total_match.group(1).replace(",", "")) if total_match else 0.0

        # Calculate Benchmarks & Discrepancies
        expected_total = AGREED_WEIGHT_KG * AGREED_RATE_PER_KG
        
        discrepancies = []
        phantom_weight = billed_weight - AGREED_WEIGHT_KG
        
        if phantom_weight > 0:
            weight_overcharge = phantom_weight * AGREED_RATE_PER_KG
            discrepancies.append(f"Phantom Weight: Invoice billed {billed_weight:,.2f} kg instead of agreed {AGREED_WEIGHT_KG:,.2f} kg (Overcharge: ${weight_overcharge:,.2f}).")

        leakage_amount = max(0.0, total_billed - expected_total)

        # --- Dynamic Output Display ---
        st.markdown("---")
        st.markdown("### 🚨 Audit & Discrepancy Breakdown Report")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Billed Amount", f"${total_billed:,.2f}")
        col2.metric("Contract Benchmark", f"${expected_total:,.2f}")
        col3.metric("Overcharge / Leakage", f"${leakage_amount:,.2f}", delta=f"-${leakage_amount:,.2f}" if leakage_amount > 0 else "0", delta_color="inverse")
        col4.metric("Extracted Weight", f"{billed_weight:,.2f} kg")
        
        st.markdown("---")
        st.markdown("### 📋 Audit Summary")
        
        if leakage_amount > 0 or len(discrepancies) > 0:
            st.error(f"DISCREPANCY DETECTED: ${leakage_amount:,.2f} Total Leakage")
            for d in discrepancies:
                st.write(f"• {d}")
        else:
            st.success("INVOICE VERIFIED: Clean invoice with no discrepancies detected.")
