import streamlit as st
import pypdf
import re

# Page Configuration
st.set_page_config(page_title="AuditX - Freight Invoice Auditor", page_icon="🚚", layout="centered")

st.title("🚚 AuditX: AI Freight Invoice Auditor")
st.write("Upload a freight invoice PDF to detect rate card overcharges, fuel surcharge variances, and weight discrepancies.")

# File Uploader
uploaded_file = st.file_uploader("Upload Freight Invoice (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    
    # 1. Extract Text using pypdf
    extracted_text = ""
    try:
        reader = pypdf.PdfReader(uploaded_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

    # Show raw extracted text inside an expander
    with st.expander("📄 View Extracted Raw Text"):
        st.text(extracted_text if extracted_text else "No readable text found in PDF.")

    # 2. Audit Logic Engine
    st.markdown("---")
    st.subheader("📊 Invoice & Weight Discrepancy Report")

    if extracted_text:
        # Extract dollar amounts and weight metrics
        amounts = re.findall(r'\$\s*[\d,]+\.\d{2}', extracted_text)
        weights = re.findall(r'[\d,]+\s*(?:kg|lbs|ctn|pkg)', extracted_text, re.IGNORECASE)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Extracted Dollar Amounts", len(amounts))
            if amounts:
                for amt in amounts[:5]:
                    st.write(f"- `{amt}`")
        
        with col2:
            st.metric("Extracted Weights / Quantities", len(weights))
            if weights:
                for w in weights[:5]:
                    st.write(f"- `{w}`")

        st.markdown("### 🔍 Flagged Discrepancies")

        # Dynamic Benchmark Detection
        total_match = re.search(r'TOTAL.*?\$\s*([\d,]+\.\d{2})', extracted_text, re.IGNORECASE)
        expected_match = re.search(r'EXPECTED.*?\$\s*([\d,]+\.\d{2})', extracted_text, re.IGNORECASE)

        if total_match and expected_match:
            total_billed = float(total_match.group(1).replace(',', ''))
            total_expected = float(expected_match.group(1).replace(',', ''))
            overcharge = total_billed - total_expected

            if overcharge > 0:
                st.error(f"🚨 **OVERCHARGE FLAG: ${overcharge:,.2f} Variance Detected**")
                st.write(f"* **Billed Rate:** `${total_billed:,.2f}`")
                st.write(f"* **Contracted Rate:** `${total_expected:,.2f}`")
                st.write("* **Action:** Dispute unverified surcharges with carrier.")
            else:
                st.success("✅ **AUDIT PASSED:** Billed amount matches contracted benchmark.")
        else:
            # Fallback check if explicit benchmark headers aren't present
            if "Peak Season" in extracted_text or "PSS" in extracted_text or "Fuel" in extracted_text:
                st.warning("⚠️ **POTENTIAL SURCHARGE LEAKAGE DETECTED**")
                st.write("Unverified Peak Season Surcharges (PSS) or Fuel Surcharges (BAF) were found in this PDF.")
                st.write("Check line-item rate cards to verify if these charges were contractually agreed upon.")
            else:
                st.info("ℹ️ PDF text parsed successfully. No immediate rate card variances flagged.")

else:
    st.info("Upload a carrier invoice PDF above to begin the audit.")
