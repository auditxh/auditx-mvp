import streamlit as st
import requests

st.title("🚛 AuditX: Freight Invoice Audit Engine")

# 1. File Uploader Widget
uploaded_file = st.file_uploader("Upload Freight Invoice (PDF)", type=["pdf"])

if uploaded_file is not None:
    # 2. Display a loading spinner while processing
    with st.spinner("Analyzing PDF for discrepancies..."):
        
        # 3. Send PDF directly to your FastAPI backend
        files = {"invoice_pdf": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post("https://auditxhridya.pythonanywhere.com/v1/verify", files=files)
        
        if response.status_code == 200:
            data = response.json()
            
            # 4. DYNAMIC DISPLAY (Pulling live numbers from backend response)
            st.markdown("### 🚨 Audit & Discrepancy Breakdown Report")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Billed Amount", f"${data.get('billed_amount', 0.0):,.2f}")
            col2.metric("Contract Benchmark", f"${data.get('contract_benchmark', 0.0):,.2f}")
            col3.metric("Overcharge / Leakage", f"${data.get('leakage_amount', 0.0):,.2f}", delta=f"-${data.get('leakage_amount', 0.0):,.2f}", delta_color="inverse")
            col4.metric("Extracted Weight", f"{data.get('extracted_weight', 0):,.2f} kg")
            
            st.markdown("---")
            st.markdown("### 📋 Audit Summary")
            
            leakage = data.get('leakage_amount', 0.0)
            if leakage > 0:
                st.error(f"DISCREPANCY DETECTED: ${leakage:,.2f} Overcharge")
                for discrepancy in data.get("discrepancies", []):
                    st.write(f"• **Invoice Discrepancy:** {discrepancy}")
            else:
                st.success("INVOICE VERIFIED: Clean invoice with no discrepancies detected.")
        else:
            st.error("Error communicating with backend API.")
