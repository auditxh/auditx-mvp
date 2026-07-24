import streamlit as st
import google.generativeai as genai
import pypdf

st.title("AuditX — AI Freight Audit Engine")
st.write("Upload a freight invoice PDF to detect line-item overcharges instantly.")

# Enter API Key
api_key = st.text_input("Enter Free Gemini API Key", type="password")

uploaded_file = st.file_uploader("Choose a Freight Invoice (PDF)", type=["pdf"])

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    
    # Read PDF text
    reader = pypdf.PdfReader(uploaded_file)
    invoice_text = ""
    for page in reader.pages:
        invoice_text += page.extract_text()
        
    st.success("Invoice Extracted Successfully!")
    
    if st.button("Run Audit Engine"):
        with st.spinner("Analyzing rate discrepancies & overcharges..."):
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
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            st.markdown("### 📊 Audit Savings Report")
            st.write(response.text)
