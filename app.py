import os
from google import genai

# Initialize free Gemini client (set GEMINI_API_KEY in your Streamlit secrets or environment)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def audit_any_invoice(pdf_text):
    system_prompt = """
    You are an expert enterprise financial auditor. Analyze the following invoice text.
    Follow these strict universal variable mapping rules:
    1. Identify the 'Vendor Name' (vendor_name).
    2. Identify the 'Invoice Number' (invoice_number).
    3. Identify the 'Purchase Order / Reference ID' (cross_reference_id).
    4. Identify the 'Gross Amount Billed' (gross_amount as a float).
    5. List any line-item discrepancies or tax/fee variances found.

    Return the extracted data in a clean, structured format.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',  # Free tier model
        contents=f"{system_prompt}\n\nInvoice Text:\n{pdf_text}"
    )
    return response.text
