import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# Configure Streamlit page
st.set_page_config(
    page_title="EMR Dashboard by Aravind",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove default Streamlit padding and chrome
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

# Read data from data/data.csv
@st.cache_data
def load_lab_data():
    df = pd.read_csv("data/data.csv")
    return df

df = load_lab_data()

# Extract date columns (all columns after 'Reference Range')
date_columns = [col for col in df.columns if col not in ['Panel', 'Test Name', 'Unit', 'Reference Range']]

# Group tests by Panel and format into the JSON structure expected by the frontend
panels_map = {}
for _, row in df.iterrows():
    panel_name = row['Panel']
    if panel_name not in panels_map:
        panels_map[panel_name] = []
    
    test_name = row['Test Name']
    unit = row['Unit']
    ref = row['Reference Range']
    
    test_data = {}
    for d in date_columns:
        val_str = str(row[d]).strip()
        if val_str == '-' or pd.isna(row[d]):
            test_data[d] = None
        else:
            if '(' in val_str and ')' in val_str:
                parts = val_str.replace(')', '').split('(')
                try:
                    val = float(parts[0].strip())
                    flag = parts[1].strip()
                except:
                    val = val_str
                    flag = 'N'
            else:
                try:
                    val = float(val_str)
                    flag = 'N'
                except:
                    val = val_str
                    flag = 'N'
            test_data[d] = {"val": val, "flag": flag}
            
    panels_map[panel_name].append({
        "name": test_name,
        "ref": ref,
        "unit": unit,
        "data": test_data
    })

clinical_panels_js = []
panel_titles_mapping = {
    "Endocrine": "Glycemic Control & Thyroid (Endocrine)",
    "Endocrine / Thyroid": "Glycemic Control & Thyroid (Endocrine)",
    "Lipid Profile": "Lipid Profile (Cardiovascular & Metabolic)",
    "Liver Function": "Liver Function Test (LFT)",
    "Complete Blood Count": "Complete Blood Count (CBC)",
    "Renal & Misc": "Renal Function & Miscellaneous",
    "Vitamins & Nutritional": "Vitamins & Nutritional",
    "Miscellaneous": "Renal Function & Miscellaneous"
}

for p_name, tests in panels_map.items():
    title = panel_titles_mapping.get(p_name, p_name)
    clinical_panels_js.append({
        "title": title,
        "tests": tests
    })

lab_dates_json = json.dumps(date_columns)
clinical_panels_json = json.dumps(clinical_panels_js)

html_template = """<!DOCTYPE html>
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

    <!-- FIXED HEADER -->
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
            
            <div class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
                <label class="flex items-center gap-2 cursor-pointer bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors">
                    <input type="checkbox" id="outOfRangeToggle" class="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4" onchange="toggleOutOfRange()">
                    <span class="text-slate-700 font-semibold">Show Only Out-of-Range</span>
                </label>
                <div class="text-right hidden lg:block">
                    <div class="text-xs font-semibold text-slate-500">DataSource</div>
                    # <div class="text-xs font-bold text-indigo-600">Loaded from data/data.csv</div>
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
                        HbA1c improved from peak <strong>8.6% (Aug 2025)</strong> (7.6% in Nov 2025 Visit Smart) down to normal <strong>5.8% by Sep 2026</strong>. Persistent hypertriglyceridemia and mild hepatocellular enzyme elevation require continued monitoring. TSH normalized from 8.61 to 1.53 µIU/mL.</code>.
                    </p>
                </div>
            </div>
        </section>

        <!-- PANELS CONTAINER -->
        <div id="panelsContainer" class="space-y-8"></div>
    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        EMR Dashboard by Aravind &bull; Generated for Dr. Review &bull; Patient ID: ARAVM0812954025 / 14653457
    </footer>

<script>
    const labDates = __LAB_DATES_JSON__;
    const clinicalPanels = __CLINICAL_PANELS_JSON__;

    function generateSparkline(dataObj) {
        const values = labDates.map(d => dataObj[d] ? dataObj[d].val : null).filter(v => v !== null && typeof v === 'number');
        if (values.length < 2) return '<span class="text-xs text-slate-400 italic">Single point</span>';

        const min = Math.min(...values);
        const max = Math.max(...values);
        const range = max - min === 0 ? 1 : max - min;
        const width = 80;
        const height = 24;

        const points = labDates.map((d, index) => {
            const item = dataObj[d];
            if (!item || typeof item.val !== 'number') return null;
            const x = (index / (labDates.length - 1)) * width;
            const y = height - ((item.val - min) / range) * (height - 6) - 3;
            return `${x},${y}`;
        }).filter(p => p !== null).join(' ');

        return `
            <svg width="${width}" height="${height}" class="inline-block overflow-visible">
                <polyline fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" points="${points}" />
                ${labDates.map((d, index) => {
                    const item = dataObj[d];
                    if (!item || typeof item.val !== 'number') return '';
                    const x = (index / (labDates.length - 1)) * width;
                    const y = height - ((item.val - min) / range) * (height - 6) - 3;
                    const color = item.flag === 'H' ? '#ef4444' : (item.flag === 'L' ? '#3b82f6' : '#10b981');
                    return `<circle cx="${x}" cy="${y}" r="3" fill="${color}" />`;
                }).join('')}
            </svg>
        `;
    }

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

html_code = html_template.replace("__LAB_DATES_JSON__", lab_dates_json).replace("__CLINICAL_PANELS_JSON__", clinical_panels_json)
components.html(html_code, height=1950, scrolling=True)
