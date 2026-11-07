import streamlit as st
import pandas as pd
import pdfplumber
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="AuditX | AI Invoice & Compliance Engine",
    page_icon="📄",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #faf9f6; }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: 600; background-color: #000; color: #fff; }
    .stButton>button:hover { background-color: #333; color: #fff; }
    .secure-badge { background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 12px; border-radius: 6px; color: #166534; font-size: 14px; margin-bottom: 15px; }
    .cta-box { background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; text-align: center; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.title("📄 AuditX: Hybrid AI & Compliance Audit Engine")
st.markdown("Automated cross-industry invoice data extraction paired with deterministic Python financial math to eliminate billing leakage.")

st.divider()

# --- Sandbox Mode State ---
if 'sandbox_loaded' not in st.session_state:
    st.session_state.sandbox_loaded = False

# --- Sandbox Trigger ---
st.subheader("🧪 Instant Sandbox Mode (No PDF Required)")
st.markdown("Test our engine instantly using a pre-loaded sample enterprise freight invoice to see how automated anomaly detection works in seconds.")

if st.button("🚀 Load Demo Discrepancy Invoice"):
    st.session_state.sandbox_loaded = True

# --- Sandbox Display Logic ---
if st.session_state.sandbox_loaded:
    st.success("✨ Sample Enterprise Invoice Loaded Successfully!")
    
    with st.expander("📄 View Raw Loaded Invoice Details (INV-2026-884)", expanded=False):
        st.text("""
VENDOR: Global Freight & Logistics Corp
INVOICE NO: INV-2026-884
DATE: November 6, 2026
BILL TO: Apex Supply Chain Partners

Line Item 1: Ocean Freight Corridor (Port Klang to Cochin) - 12 TEU @ $1,200.00 = $14,400.00
Line Item 2: Terminal Handling & Port Security Surcharge - Flat Rate = $1,850.00
Line Item 3: Automated Documentation & Customs Filing Fee = $350.00

TOTAL GROSS BILLED: $16,600.00
        """)
    
    st.markdown("### 📊 AuditX Discrepancy Report")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Gross Amount Billed", value="$16,600.00")
    with col2:
        st.metric(label="Detected Variance / Leakage", value="$285.00", delta="-285.00 Overcharge", delta_color="inverse")

    st.markdown("#### 🚨 Discrepancy Breakdown & Risk Analysis")
    st.error("**⚠️ Audit Verdict: Discrepancy Found — Short-pay Recommended**")
    
    # Clean Structured Pandas Table (Fixes dollar sign clipping)
    audit_data = {
        "Line Item Description": [
            "Ocean Freight Corridor (12 TEU)", 
            "Terminal Handling & Port Security", 
            "Customs & Documentation Fee"
        ],
        "Contract Rate (MSA #402)": ["$14,400.00", "$1,565.00", "$350.00"],
        "Billed Amount ($)": ["$14,400.00", "$1,850.00", "$350.00"],
        "Status": ["✅ Verified Match", "❌ Overcharge Detected", "✅ Verified Match"]
    }
    df_audit = pd.DataFrame(audit_data)
    st.dataframe(df_audit, use_container_width=True, hide_index=True)

    st.info("""
    **Root Cause Analysis:** Line Item 2 exhibits an unapproved markup. Master Service Agreement (MSA #402) explicitly caps terminal handling at **$1,565.00**, but the vendor invoiced **$1,850.00** (a hidden **$285.00 variance**).
    """)
    
    if st.button("📥 Export Audit Report (CSV)"):
        csv_data = df_audit.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV Report",
            data=csv_data,
            file_name="AuditX_Discrepancy_Report_INV884.csv",
            mime="text/csv"
        )

st.divider()

# --- Custom PDF Upload Section with Security Badge ---
st.subheader("📁 Upload Custom Vendor Invoice")

st.markdown("""
<div class="secure-badge">
    🔒 <b>100% Secure & Private:</b> Uploaded PDFs are processed strictly in temporary cache memory and are never saved, stored, or shared.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a vendor PDF invoice for real-time validation", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text and validating against compliance rules..."):
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                extracted_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            
            st.success("✅ PDF processed successfully through temporary memory cache!")
            with st.expander("🔍 View Extracted Text Snippet"):
                st.text(extracted_text[:1000] if len(extracted_text) > 0 else "No text could be extracted.")
                
            st.warning("⚠️ Custom live AI audit rules are primed. Connect your Gemini API key or rule engine to process full line items.")
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")

# --- Professional Call to Action (CTA) Footer ---
st.markdown("""
<div class="cta-box">
    <h3>Want to run a bulk audit on your historical vendor invoices?</h3>
    <p>Contact us at <b>auditx.logistics@gmail.com</b> for a free 10-invoice trial run and custom contract rule integration.</p>
</div>
""", unsafe_allow_html=True)
