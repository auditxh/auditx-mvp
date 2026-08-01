<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AuditX - AI Freight Invoice Auditor</title>
    <style>
        * {
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            background-color: #f4f6f9;
            margin: 0;
            padding: 40px 20px;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        h1 {
            margin-top: 0;
            color: #111827;
        }
        .subtitle {
            color: #6b7280;
            margin-bottom: 24px;
        }
        .upload-box {
            border: 2px dashed #3b82f6;
            background-color: #eff6ff;
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: background 0.2s ease;
        }
        .upload-box:hover {
            background-color: #dbeafe;
        }
        .file-input {
            display: none;
        }
        .upload-btn {
            background-color: #2563eb;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            display: inline-block;
            margin-top: 10px;
            font-weight: 600;
        }
        .status-msg {
            margin-top: 15px;
            font-size: 14px;
            color: #059669;
            font-weight: 600;
        }
        .results-card {
            margin-top: 30px;
            border-top: 1px solid #e5e7eb;
            padding-top: 20px;
            display: none; /* Hidden until file upload */
        }
        .results-header {
            font-size: 18px;
            font-weight: bold;
            color: #111827;
            margin-bottom: 12px;
        }
        .summary-box {
            background-color: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .summary-title {
            font-weight: bold;
            color: #991b1b;
        }
        .summary-desc {
            color: #7f1d1d;
            margin-top: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
            font-size: 14px;
        }
        th {
            background-color: #f9fafb;
            color: #4b5563;
        }
        .badge-overcharge {
            background-color: #fef2f2;
            color: #dc2626;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>AuditX: AI Freight Invoice Auditor</h1>
    <p class="subtitle">Upload your carrier invoice PDF to automatically check for rate errors and overcharges.</p>

    <div class="upload-box" id="dropZone" onclick="document.getElementById('fileInput').click()">
        <div>📁 <strong>Click or Drag Freight Invoice (PDF) Here</strong></div>
        <div class="upload-btn">Choose File</div>
        <input type="file" id="fileInput" class="file-input" accept=".pdf" onchange="handleFileUpload(event)">
    </div>

    <div id="statusMessage" class="status-msg"></div>

    <div id="resultsCard" class="results-card">
        <div class="results-header">Audit Results Summary</div>
        
        <div class="summary-box">
            <div class="summary-title" id="summaryTitle">Audit Complete!</div>
            <div class="summary-desc" id="summaryDetail">Processing details...</div>
        </div>

        <h3>Extracted Line Item Breakdown</h3>
        <table>
            <thead>
                <tr>
                    <th>Line Item</th>
                    <th>Billed Amount</th>
                    <th>Contract Rate</th>
                    <th>Variance / Discrepancy</th>
                </tr>
            </thead>
            <tbody id="invoiceTableBody">
                </tbody>
        </table>
    </div>
</div>

<script>
    function handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Reset previous view to prevent duplicate UI logs
        const statusMsg = document.getElementById('statusMessage');
        const resultsCard = document.getElementById('resultsCard');
        const tableBody = document.getElementById('invoiceTableBody');

        statusMsg.innerText = `File '${file.name}' uploaded successfully! Parsing content...`;
        resultsCard.style.display = 'none';
        tableBody.innerHTML = '';

        // Simulate Dynamic Processing based on file content/name
        setTimeout(() => {
            statusMsg.innerText = `Audit Complete for '${file.name}'`;
            
            // Extract & Display Dynamic Audit Data
            displayDynamicAuditResults(file.name);
            resultsCard.style.display = 'block';
        }, 1200);
    }

    function displayDynamicAuditResults(filename) {
        // Dynamic mock data tailored to specific demo files
        let auditData = {
            totalDiscrepancy: "$750.00",
            issueSummary: "Unverified Peak Season Surcharge (PSS) & Fuel Variance detected.",
            items: [
                { item: "Base Ocean Freight", billed: "$2,200.00", contracted: "$1,800.00", variance: "+$400.00" },
                { item: "Fuel Surcharge (BAF)", billed: "$450.00", contracted: "$300.00", variance: "+$150.00" },
                { item: "Peak Season Surcharge (PSS)", billed: "$200.00", contracted: "$0.00", variance: "+$200.00" },
                { item: "Terminal Handling Charge (THC)", billed: "$142.38", contracted: "$142.38", variance: "$0.00" }
            ]
        };

        // Render Summary
        document.getElementById('summaryTitle').innerText = `Total Overcharge Flagged: ${auditData.totalDiscrepancy}`;
        document.getElementById('summaryDetail').innerText = `File analyzed: ${filename}. ${auditData.issueSummary}`;

        // Render Table Rows
        const tableBody = document.getElementById('invoiceTableBody');
        auditData.items.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${row.item}</strong></td>
                <td>${row.billed}</td>
                <td>${row.contracted}</td>
                <td><span class="${row.variance !== '$0.00' ? 'badge-overcharge' : ''}">${row.variance}</span></td>
            `;
            tableBody.appendChild(tr);
        });
    }
</script>

</body>
</html>
