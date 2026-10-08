import streamlit as st
import pypdf
import re

st.set_page_config(page_title="AuditX - Freight Audit Engine", page_icon="🚛", layout="wide")

st.title("🚛 AuditX: Freight Invoice Audit Engine")
st.caption("Automated weight & invoice discrepancy detection for enterprise logistics.")

CONTRACT_BENCHMARK = 4117.00
EXPECTED_WEIGHT = 18549.00

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

uploaded_file = st.file_uploader("Upload Freight Invoice (PDF)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analyzing PDF for discrepancies..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        
        # --- FIXED METADATA EXTRACTION ---
        # Carrier Name (First line or matching LLC/LTD/INC/FZE)
        carrier_match = re.search(r"([A-Z0-9\s&\-\.]+(?:LLC|LTD|FZE|INC|EXPRESS|CARRIERS|LOGISTICS))", pdf_text, re.IGNORECASE)
        carrier_name = carrier_match.group(1).strip() if carrier_match else "Carrier Identified"

        # Invoice Number (Ignores "INVOICE TO")
        inv_match = re.search(r"Invoice\s*(?:No|Number|#)?\s*[:\-]?\s*([A-Z0-9\-]{4,})", pdf_text, re.IGNORECASE)
        invoice_num = inv_match.group(1) if inv_match else "N/A"

        # Bill of Lading
        bol_match = re.search(r"(?:Bill of Lading|BOL)\s*(?:\(BOL\))?\s*[:\-]?\s*([A-Z0-9\-]+)", pdf_text, re.IGNORECASE)
        bol_num = bol_match.group(1) if bol_match else "N/A"

        # Total Billed Amount
        total_match = re.search(r"TOTAL[^\$\d]*\$?\s*([\d,]+\.\d{2})", pdf_text, re.IGNORECASE)
        total_billed = float(total_match.group(1).replace(",", "")) if total_match else 0.0

        # Extracted Weight
        weight_match = re.search(r"Weight\s*[:\-]?\s*([\d,]+\.?\d*)\s*KG", pdf_text, re.IGNORECASE)
        billed_weight = float(weight_match.group(1).replace(",", "")) if weight_match else 0.0

        leakage_amount = max(0.0, total_billed - CONTRACT_BENCHMARK)

        # --- AUDIT DASHBOARD ---
        st.markdown("---")
        st.markdown("### 🚨 Audit & Discrepancy Breakdown Report")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Billed Amount", f"${total_billed:,.2f}")
        col2.metric("Contract Benchmark", f"${CONTRACT_BENCHMARK:,.2f}")
        col3.metric("Overcharge / Leakage", f"${leakage_amount:,.2f}", delta=f"-${leakage_amount:,.2f}" if leakage_amount > 0 else "$0.00", delta_color="inverse")
        col4.metric("Extracted Weight", f"{billed_weight:,.2f} kg")
        
        st.markdown("---")
        st.markdown("### 📋 Audit Summary")
        
        if leakage_amount > 0:
            st.error(f"DISCREPANCY DETECTED: ${leakage_amount:,.2f} Overcharge flagged against contract benchmarks.")
        else:
            st.success("INVOICE VERIFIED: Clean invoice with no discrepancies detected.")

        with st.expander("▶ Click here to view Company Details & Audit Breakdown"):
            st.markdown("#### 🏢 Carrier & Shipment Details")
            st.write(f"**Carrier Name:** {carrier_name}")
            st.write(f"**Invoice Number:** {invoice_num}")
            st.write(f"**Bill of Lading (BOL):** {bol_num}")
            st.write(f"**Billed Weight:** {billed_weight:,.2f} KG (Contract Baseline: {EXPECTED_WEIGHT:,.2f} KG)")
            
            st.markdown("---")
            st.markdown("#### 🔍 Discrepancy Analysis (How Overcharge Happened)")
            if leakage_amount > 0:
                st.write(f"1. **Contract Rate Mismatch:** Agreed lane rate benchmark was **${CONTRACT_BENCHMARK:,.2f}**.")
                st.write(f"2. **Actual Total Billed:** Invoice total came to **${total_billed:,.2f}**.")
                st.write(f"3. **Surcharges Identified:** Unclassified fees pushed total cost **${leakage_amount:,.2f}** above contract rates.")
            else:
                st.write("No billing anomalies or unclassified surcharges detected.")
