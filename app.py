// Example fix in your JS/Python backend for AuditX
function processInvoice(extractedText) {
    // 1. Dynamic Regex to parse total amount and weight correctly
    const totalBilled = parseCurrency(extractedText.match(/TOTAL AMOUNT DUE:\s*\$([\d,]+\.\d{2})/i)[1]);
    const grossWeight = parseFloat(extractedText.match(/Gross Weight:\s*([\d,]+\.\d{2})/i)[1].replace(',', ''));
    
    // 2. Fetch expected rate card benchmark from your DB
    const contractBenchmark = 4299.84; // From Rate Card DB
    
    // 3. Compute real dynamic leakage
    const leakage = totalBilled - contractBenchmark; // $5049.84 - $4299.84 = $750.00
    
    return {
        billedAmount: totalBilled,
        contractBenchmark: contractBenchmark,
        overchargeLeakage: leakage,
        extractedWeight: grossWeight
    };
}

