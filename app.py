import streamlit as st
from google import genai
import pypdf

st.title("AuditX — AI Freight Audit Engine")
st.write("Upload a freight invoice PDF to detect line-item overcharges instantly.")

api_key = st.text_input("Enter Free Gemini API Key", type="password")
uploaded_file = st.file_uploader("Choose a Freight Invoice (PDF)", type=["pdf"])

if uploaded_file and api_key:
    clean_api_key = api_key.strip()
    
    reader = pypdf.PdfReader(uploaded_file)
    invoice_text = ""
    for page in reader.pages:
        invoice_text += page.extract_text() or ""
        
    st.success("Invoice Extracted Successfully!")
    
    if st.button("Run Audit Engine"):
        with st.spinner("Analyzing rate discrepancies & overcharges..."):
            try:
                client = genai.Client(api_key=clean_api_key)
                
                prompt = f"""
                You are AuditX, an automated freight audit engine. Analyze this invoice text:
                
                {invoice_text}
                
                Perform the following checks:
                1. Extract Billed Weight vs Declared/Contract Weight.
                2. Extract Base Rate, Fuel Surcharge, and Accessorial Fees.
                3. Identify any rate discrepancies or overcharges.
                4. Output a clean Audit Savings Summary Report showing:
                   - Total Billed Amount
                   - Should-Be Billed Amount
                   - Total Savings Found ($)
                   - Line-by-Line Overcharge Explanations
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                st.markdown("### 📊 Audit Savings Report")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error running audit: {e}")
