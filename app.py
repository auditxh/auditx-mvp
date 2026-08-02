import streamlit as st
import re
import pdfplumber

# Set Page Config
st.set_page_config(
    page_title="AuditX - Freight Audit Engine",
    page_icon="🚚",
    layout="wide"
)

# App Header
st.title("🚚 AuditX: Freight Invoice Audit Report")
st.caption("Upload your carrier invoice PDF to generate an automated discrepancy & leakage breakdown.")

# File Uploader Component
uploaded_file = st.file_uploader("Upload Freight Invoice (PDF)", type=["pdf"])

# Master Contract Rate Cards Database (Simulated Database)
CONTRACT_RATE_CARDS = {
    "HL-ASIA-2026": {
        "base_rate": 3800.00,
        "contracted_baf": 350.00,
        "contracted_thc": 149.84,
        "contracted_pss": 0.00,
        "max_allowable_weight_per_ctn": 195.00  # Baseline target
    },
    "DEFAULT": {
        "base_rate": 1800.00,
        "contracted_baf": 300.00,
        "contracted_thc": 142.38,
        "contracted_pss": 0.00,
        "max_allowable_weight_per_ctn": 192.10
    }
}

# Master Manifest Database (Simulated Baseline Manifest Data)
BASELINE_MANIFESTS = {
    "HLCUTPE260621422": {
        "baseline_bol": "HLCUTPE260593585",
        "expected_total_weight": 17289.00,
        "expected_unit_weight": 192.10,
        "package_count": 90
    }
}


def extract_pdf_data(pdf_file):
    """Extracts raw text and dynamically parses invoice metadata, weight, and financial charges."""
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    # Dynamic Regex Extractors
    
    # 1. Extract BOL / Contract / Invoice ID
    bol_match = re.search(r"(?:Bill of Lading|BOL
