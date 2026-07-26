import streamlit as st
from openai import OpenAI
import pypdf

st.title("AuditX — AI Freight Audit Engine")
st.write("Upload a freight invoice PDF to detect line-item overcharges instantly.")

api_key = st.text_input("Enter Free OpenRouter API Key", type="password")
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
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=clean_api_key,
                )
                
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
                
                completion = client.chat.completions.create(
                    model="meta-llama/llama-3.3-70b-instruct:free",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                )
                
                st.markdown("### 📊 Audit Savings Report")
                st.write(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error running audit: {e}")
