import streamlit as st
import streamlit.components.v1 as components

# Configure Streamlit page
st.set_page_config(
    page_title="EMR Dashboard made by Aravind",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove default Streamlit padding and chrome so the dashboard looks identical to standalone HTML
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        header[data-testid="stHeader"] {
            display: none;
        }
        footer {
            display: none;
        }
        iframe {
            border: none;
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EMR Dashboard by Aravind</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .sticky-col {
            position: sticky;
            left: 0;
            z-index: 20;
            background-color: white;
        }
        .dark .sticky-col {
            background-color: #1f2937;
        }
        /* Custom scrollbar for clean table navigation */
        .table-container::-webkit-scrollbar {
            height: 8px;
        }
        .table-container::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        .table-container::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col antialiased">

    <!-- FIXED HEADER: Patient Metadata (Doctor-Friendly Summary) -->
    <header class="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
            <div>
                <div class="flex items-center gap-3">
                    <h1 class="text-xl font-bold text-slate-900 tracking-tight">EMR Dashboard by Aravind</h1>
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-800">Aravind Babu</span>
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800">30 Years / Male</span>
                    <span class="hidden sm:inline-block px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">DDRC Agilus & Visit Smart Verified</span>
                </div>
                <p class="text-xs text-slate-500 mt-0.5">
                    <strong class="text-slate-700">Primary Concerns:</strong> Type 2 Diabetes Mellitus, Dyslipidemia (Hypertriglyceridemia), Subclinical Hypothyroidism, Elevated ALT/AST.
                </p>
            </div>
            
            <!-- Interactive Controls & Quick Stats -->
            <div class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
                <label class="flex items-center gap-2 cursor-pointer bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors">
                    <input type="checkbox" id="outOfRangeToggle" class="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4" onchange="toggleOutOfRange()">
                    <span class="text-slate-700 font-semibold">Show Only Out-of-Range</span>
                </label>
                <div class="text-right hidden lg:block">
                    <div class="text-xs font-semibold text-slate-500">Longitudinal Span</div>
                    <div class="text-xs font-bold text-indigo-600">Aug 2025 – Sep 2026 (12 Mos)</div>
                </div>
            </div>
        </div>
    </header>

    <!-- MAIN DASHBOARD CONTAINER -->
    <main class="max-w-7xl mx-auto px-4 py-6 flex-grow space-y-8 w-full">

        <!-- CLINICAL ALERTS / SUMMARY BANNER -->
        <section class="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-xl shadow-sm">
            <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <div>
                    <h2 class="text-sm font-bold text-amber-900">Clinical Review Note (60-Second Snapshot)</h2>
                    <p class="text-xs text-amber-800 mt-1 leading-relaxed">
                        HbA1c improved from peak <strong>8.6% (Aug 2025)</strong> (7.6% in Nov 2025) down to normal <strong>5.8% by Sep 2026</strong>. Persistent hypertriglyceridemia (Triglycerides up to 433 mg/dL) and mild hepatocellular enzyme elevation (ALT peak 116 U/L in Nov 2025, 107 U/L in Sep 2026) require continued monitoring. TSH normalized from 8.61 to 1.53 µIU/mL.
                    </p>
                </div>
            </div>
        </section>

        <!-- DASHBOARD PANELS (Rendered Dynamically via JS) -->
        <div id="panelsContainer" class="space-y-8">
            <!-- Panels injected by script below -->
        </div>
    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        Standalone Clinical Informatics Report &bull; Generated for Dr. Review &bull; Patient ID: ARAVM0812954025 / 14653457
    </footer>

<script>
    // Comprehensive Longitudinal Lab Data Extraction (Aug 2025 to Sep 2026, including 26/11/2025 Visit Smart Report)
    const labDates = [
        '04/08/2025', 
        '07/09/2025', 
        '26/11/2025',
        '28/01/2026', 
        '11/06/2026', 
        '21/07/2026', 
        '22/07/2026', 
        '29/07/2026', 
        '30/07/2026', 
        '22/09/2026'
    ];

    const clinicalPanels = [
        {
            title: "Glycemic Control & Thyroid (Endocrine)",
            tests: [
                {
                    name: "HbA1c",
                    ref: "< 5.7 (Normal)",
                    unit: "%",
                    data: { '04/08/2025': { val: 8.6, flag: 'H' }, '07/09/2025': null, '26/11/2025': { val: 7.6, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 7.1, flag: 'H' }, '21/07/2026': { val: 6.4, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 5.8, flag: 'N' } }
                },
                {
                    name: "Estimated Avg Glucose (eAG)",
                    ref: "< 116",
                    unit: "mg/dL",
                    data: { '04/08/2025': { val: 200.1, flag: 'H' }, '07/09/2025': null, '26/11/2025': { val: 171.42, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 157.1, flag: 'H' }, '21/07/2026': { val: 137.0, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 119.8, flag: 'H' } }
                },
                {
                    name: "Glucose Fasting (FBS)",
                    ref: "70 - 99",
                    unit: "mg/dL",
                    data: { '04/08/2025': { val: 181, flag: 'H' }, '07/09/2025': { val: 141, flag: 'H' }, '26/11/2025': { val: 121, flag: 'H' }, '28/01/2026': { val: 103, flag: 'H' }, '11/06/2026': { val: 131, flag: 'H' }, '21/07/2026': { val: 114, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 114, flag: 'H' } }
                },
                {
                    name: "Glucose Post-Prandial (PPBS)",
                    ref: "< 140",
                    unit: "mg/dL",
                    data: { '04/08/2025': { val: 229, flag: 'H' }, '07/09/2025': null, '26/11/2025': null, '28/01/2026': { val: 115, flag: 'N' }, '11/06/2026': { val: 254, flag: 'H' }, '21/07/2026': { val: 152, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 138, flag: 'N' } }
                },
                {
                    name: "TSH (Ultrasensitive)",
                    ref: "0.27 - 4.20",
                    unit: "µIU/mL",
                    data: { '04/08/2025': { val: 8.61, flag: 'H' }, '07/09/2025': null, '26/11/2025': { val: 5.72, flag: 'H' }, '28/01/2026': { val: 8.64, flag: 'H' }, '11/06/2026': null, '21/07/2026': { val: 2.78, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 1.53, flag: 'N' } }
                }
            ]
        },
        {
            title: "Lipid Profile (Cardiovascular & Metabolic)",
            tests: [
                {
                    name: "Total Cholesterol",
                    ref: "< 200",
                    unit: "mg/dL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 232, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 191, flag: 'N' }, '21/07/2026': { val: 191, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 170, flag: 'N' } }
                },
                {
                    name: "Triglycerides",
                    ref: "< 150",
                    unit: "mg/dL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 351, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 307, flag: 'H' }, '21/07/2026': { val: 307, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 433, flag: 'H' } }
                },
                {
                    name: "HDL Cholesterol",
                    ref: "40 - 60",
                    unit: "mg/dL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 37, flag: 'L' }, '28/01/2026': null, '11/06/2026': { val: 30, flag: 'L' }, '21/07/2026': { val: 30, flag: 'L' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 34, flag: 'L' } }
                },
                {
                    name: "LDL Cholesterol",
                    ref: "< 100",
                    unit: "mg/dL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 124.8, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 100, flag: 'N' }, '21/07/2026': { val: 100, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 115, flag: 'H' } }
                },
                {
                    name: "Non-HDL Cholesterol",
                    ref: "< 130",
                    unit: "mg/dL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 195, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 161, flag: 'H' }, '21/07/2026': { val: 161, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 136, flag: 'H' } }
                }
            ]
        },
        {
            title: "Liver Function Test (LFT)",
            tests: [
                {
                    name: "ALT (SGPT)",
                    ref: "0 - 41",
                    unit: "U/L",
                    data: { '04/08/2025': { val: 66, flag: 'H' }, '07/09/2025': null, '26/11/2025': { val: 116, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 100, flag: 'H' }, '21/07/2026': { val: 100, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 107, flag: 'H' } }
                },
                {
                    name: "AST (SGOT)",
                    ref: "0 - 40",
                    unit: "U/L",
                    data: { '04/08/2025': { val: 41, flag: 'H' }, '07/09/2025': null, '26/11/2025': { val: 67, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 43, flag: 'H' }, '21/07/2026': { val: 43, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 50, flag: 'H' } }
                },
                {
                    name: "Alkaline Phosphatase (ALP)",
                    ref: "40 - 130",
                    unit: "U/L",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 89, flag: 'N' }, '28/01/2026': null, '11/06/2026': { val: 83, flag: 'N' }, '21/07/2026': { val: 83, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 94, flag: 'N' } }
                },
                {
                    name: "Total Bilirubin",
                    ref: "< 1.2",
                    unit: "mg/dL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 0.50, flag: 'N' }, '28/01/2026': null, '11/06/2026': { val: 0.6, flag: 'N' }, '21/07/2026': { val: 0.6, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 0.27, flag: 'N' } }
                },
                {
                    name: "Gamma GT (GGT)",
                    ref: "8 - 61",
                    unit: "U/L",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 70, flag: 'H' }, '28/01/2026': null, '11/06/2026': { val: 64, flag: 'H' }, '21/07/2026': { val: 64, flag: 'H' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': null }
                }
            ]
        },
        {
            title: "Complete Blood Count (CBC)",
            tests: [
                {
                    name: "Hemoglobin (Hb)",
                    ref: "13.0 - 17.0",
                    unit: "g/dL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 16.2, flag: 'N' }, '28/01/2026': null, '11/06/2026': null, '21/07/2026': { val: 16.8, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 15.2, flag: 'N' } }
                },
                {
                    name: "Total Leukocyte Count (WBC)",
                    ref: "4.0 - 10.0",
                    unit: "thou/µL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 7.3, flag: 'N' }, '28/01/2026': null, '11/06/2026': null, '21/07/2026': { val: 7.9, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 8.4, flag: 'N' } }
                },
                {
                    name: "Platelet Count",
                    ref: "150 - 410",
                    unit: "thou/µL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 292, flag: 'N' }, '28/01/2026': null, '11/06/2026': null, '21/07/2026': { val: 260, flag: 'N' }, '22/07/2026': null, '29/07/2026': { val: 160, flag: 'N' }, '30/07/2026': { val: 160, flag: 'N' }, '22/09/2026': { val: 286, flag: 'N' } }
                },
                {
                    name: "Mean Corpuscular Volume (MCV)",
                    ref: "83 - 101",
                    unit: "fL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 88.7, flag: 'N' }, '28/01/2026': null, '11/06/2026': null, '21/07/2026': { val: 89.0, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 87.7, flag: 'N' } }
                }
            ]
        },
        {
            title: "Renal Function & Miscellaneous",
            tests: [
                {
                    name: "Serum Creatinine",
                    ref: "0.90 - 1.30",
                    unit: "mg/dL",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 0.94, flag: 'N' }, '28/01/2026': null, '11/06/2026': { val: 1.19, flag: 'N' }, '21/07/2026': { val: 1.19, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 0.91, flag: 'N' } }
                },
                {
                    name: "Serum Uric Acid",
                    ref: "3.4 - 7.0",
                    unit: "mg/dL",
                    data: { '04/08/2025': { val: 4.2, flag: 'N' }, '07/09/2025': null, '26/11/2025': { val: 4.9, flag: 'N' }, '28/01/2026': null, '11/06/2026': { val: 5.7, flag: 'N' }, '21/07/2026': { val: 5.7, flag: 'N' }, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 6.0, flag: 'N' } }
                },
                {
                    name: "Erythrocyte Sedimentation Rate (ESR)",
                    ref: "0 - 10",
                    unit: "mm/hr",
                    data: { '04/08/2025': null, '07/09/2025': null, '26/11/2025': { val: 5, flag: 'N' }, '28/01/2026': null, '11/06/2026': null, '21/07/2026': null, '22/07/2026': null, '29/07/2026': null, '30/07/2026': null, '22/09/2026': { val: 9, flag: 'N' } }
                }
            ]
        }
    ];

    // Helper to generate inline Sparkline SVG
    function generateSparkline(dataObj) {
        const values = labDates.map(d => dataObj[d] ? dataObj[d].val : null).filter(v => v !== null);
        if (values.length < 2) return '<span class="text-xs text-slate-400 italic">Single point</span>';

        const min = Math.min(...values);
        const max = Math.max(...values);
        const range = max - min === 0 ? 1 : max - min;
        const width = 80;
        const height = 24;

        // Map values to SVG coordinates
        const points = labDates.map((d, index) => {
            const val = dataObj[d] ? dataObj[d].val : null;
            if (val === null) return null;
            const x = (index / (labDates.length - 1)) * width;
            const y = height - ((val - min) / range) * (height - 6) - 3;
            return `${x},${y}`;
        }).filter(p => p !== null).join(' ');

        return `
            <svg width="${width}" height="${height}" class="inline-block overflow-visible">
                <polyline fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" points="${points}" />
                ${labDates.map((d, index) => {
                    const item = dataObj[d];
                    if (!item) return '';
                    const x = (index / (labDates.length - 1)) * width;
                    const y = height - ((item.val - min) / range) * (height - 6) - 3;
                    const color = item.flag === 'H' ? '#ef4444' : (item.flag === 'L' ? '#3b82f6' : '#10b981');
                    return `<circle cx="${x}" cy="${y}" r="3" fill="${color}" />`;
                }).join('')}
            </svg>
        `;
    }

    // Render Dashboard Tables
    function renderDashboard() {
        const container = document.getElementById('panelsContainer');
        container.innerHTML = '';

        clinicalPanels.forEach(panel => {
            let panelHtml = `
                <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-6">
                    <div class="bg-slate-50 px-5 py-3 border-b border-slate-200 flex justify-between items-center">
                        <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider">${panel.title}</h3>
                        <span class="text-xs text-slate-500 font-medium">${panel.tests.length} Parameters Tracked</span>
                    </div>
                    <div class="table-container overflow-x-auto relative">
                        <table class="w-full text-left border-collapse text-xs">
                            <thead>
                                <tr class="bg-slate-100/70 text-slate-600 font-semibold border-b border-slate-200">
                                    <th class="py-3 px-4 sticky-col bg-slate-100 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.05)] min-w-[220px]">Test Name & Units</th>
                                    <th class="py-3 px-3 min-w-[110px] text-center">Reference Range</th>
                                    <th class="py-3 px-3 min-w-[100px] text-center">Trend (12M)</th>
                                    ${labDates.map(date => `<th class="py-3 px-3 text-center min-w-[90px] font-normal text-slate-600">${date}</th>`).join('')}
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
            `;

            panel.tests.forEach(test => {
                panelHtml += `
                    <tr class="test-row hover:bg-slate-50/80 transition-colors" data-has-abnormal="${Object.values(test.data).some(d => d && d.flag !== 'N')}">
                        <td class="py-3 px-4 sticky-col font-medium text-slate-900 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.05)]">
                            ${test.name} <span class="text-slate-400 font-normal">(${test.unit})</span>
                        </td>
                        <td class="py-3 px-3 text-center text-slate-500 font-mono">${test.ref}</td>
                        <td class="py-3 px-3 text-center">${generateSparkline(test.data)}</td>
                `;

                labDates.forEach(date => {
                    const res = test.data[date];
                    if (!res) {
                        panelHtml += `<td class="py-3 px-3 text-center text-slate-300">-</td>`;
                    } else {
                        let pillClass = "text-slate-700 font-normal";
                        let badge = "";
                        if (res.flag === 'H') {
                            pillClass = "bg-red-50 text-red-700 font-bold px-2 py-0.5 rounded-md border border-red-200";
                            badge = `<span class="ml-1 text-[10px] bg-red-600 text-white px-1 rounded">H</span>`;
                        } else if (res.flag === 'L') {
                            pillClass = "bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded-md border border-blue-200";
                            badge = `<span class="ml-1 text-[10px] bg-blue-600 text-white px-1 rounded">L</span>`;
                        }
                        panelHtml += `<td class="py-3 px-3 text-center font-mono ${pillClass}">${res.val}${badge}</td>`;
                    }
                });

                panelHtml += `</tr>`;
            });

            panelHtml += `
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
            container.innerHTML += panelHtml;
        });
    }

    // Interactive Toggle for Out-of-Range filter
    function toggleOutOfRange() {
        const onlyAbnormal = document.getElementById('outOfRangeToggle').checked;
        const rows = document.querySelectorAll('.test-row');
        
        rows.forEach(row => {
            const isAbnormal = row.getAttribute('data-has-abnormal') === 'true';
            if (onlyAbnormal && !isAbnormal) {
                row.style.display = 'none';
            } else {
                row.style.display = '';
            }
        });
    }

    window.onload = renderDashboard;
</script>
</body>
</html>
"""

# Render the full HTML dashboard seamlessly
components.html(html_code, height=1950, scrolling=True)