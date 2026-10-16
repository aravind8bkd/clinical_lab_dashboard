import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Clinical Lab Trends | Aravind Babu",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove default Streamlit padding and chrome for a clean full-bleed clinical dashboard
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            border: none !important;
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

HTML_CODE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Lab Trends | Aravind Babu</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .sticky-col-shadow { box-shadow: 4px 0 8px -2px rgba(0, 0, 0, 0.06); }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-12">

    <!-- Sticky Clinical Header -->
    <header class="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-3 sm:px-6 py-3">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                <div class="flex flex-wrap items-center gap-x-6 gap-y-1">
                    <div class="flex items-center gap-2.5">
                        <span class="h-3 w-3 rounded-full bg-emerald-600 animate-pulse"></span>
                        <h1 class="text-base sm:text-lg font-bold tracking-tight text-slate-900">ARAVIND BABU</h1>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">30Y / Male</span>
                    </div>
                    <div class="text-xs text-slate-500 mono">
                        IDs: <span class="text-slate-700 font-medium">ARAVM08129575 / 4025</span>
                    </div>
                    <div class="text-xs bg-amber-50 text-amber-900 border border-amber-200 px-2.5 py-1 rounded-md font-medium">
                        <span class="font-bold">Clinical Focus:</span> T2DM Remission (HbA1c 8.6% &rarr; 5.8%) &bull; Hypothyroidism Normalized &bull; Hypertriglyceridemia &amp; Transaminases (&uarr; ALT/AST)
                    </div>
                </div>
                <div class="flex items-center justify-between sm:justify-end gap-3 pt-2 md:pt-0 border-t md:border-t-0 border-slate-100">
                    <label class="inline-flex items-center cursor-pointer select-none bg-slate-100 hover:bg-slate-200/70 px-3 py-1.5 rounded-lg border border-slate-200 transition">
                        <input type="checkbox" id="abnormalToggle" class="sr-only peer">
                        <div class="relative w-9 h-5 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-rose-600"></div>
                        <span class="ms-2.5 text-xs font-semibold text-slate-800">Show Only Out-of-Range</span>
                    </label>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-2 sm:px-6 pt-4 space-y-5">

        <!-- Legend & Quick Summary Bar -->
        <div class="bg-white rounded-lg border border-slate-200 p-3 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-600 shadow-2xs">
            <div class="flex flex-wrap items-center gap-4">
                <span class="font-semibold text-slate-800">Flags:</span>
                <span class="inline-flex items-center gap-1.5"><span class="px-1.5 py-0.5 rounded bg-rose-50 text-rose-700 border border-rose-200 font-bold mono">H</span> High / Above Ref</span>
                <span class="inline-flex items-center gap-1.5"><span class="px-1.5 py-0.5 rounded bg-sky-50 text-sky-700 border border-sky-200 font-bold mono">L</span> Low / Below Ref</span>
                <span class="inline-flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-slate-300 inline-block"></span> Normal within Reference</span>
            </div>
            <div class="text-slate-400 italic hidden sm:block">Scroll tables horizontally on mobile &bull; Dates ordered Oldest &rarr; Newest</div>
        </div>

        <div id="panelsContainer" class="space-y-6"></div>

    </main>

    <script>
        const DATES = [
            { id: "2025-08-04", label: "04 Aug 25" },
            { id: "2025-09-07", label: "07 Sep 25" },
            { id: "2026-01-28", label: "28 Jan 26" },
            { id: "2026-05-15", label: "15 May 26" },
            { id: "2026-06-11", label: "11 Jun 26" },
            { id: "2026-07-21", label: "21 Jul 26" },
            { id: "2026-07-29", label: "29 Jul 26" },
            { id: "2026-07-30", label: "30 Jul 26" },
            { id: "2026-09-22", label: "22 Sep 26" }
        ];

        const LAB_PANELS = [
            {
                id: "glycemic",
                title: "Glycemic & Diabetes Control Panel",
                subtitle: "HbA1c, eAG, Fasting & Post-Prandial Glucose",
                tests: [
                    {
                        name: "HbA1c (Glycosylated Hb)",
                        unit: "%",
                        ref: "< 5.7 (Normal: 4.0-5.6)",
                        sparkline: true,
                        values: {
                            "2025-08-04": { v: 8.6, flag: "H" },
                            "2026-06-11": { v: 7.1, flag: "H" },
                            "2026-07-21": { v: 6.4, flag: "H" },
                            "2026-09-22": { v: 5.8, flag: "H" }
                        }
                    },
                    {
                        name: "Estimated Avg Glucose (eAG)",
                        unit: "mg/dL",
                        ref: "< 116.0",
                        sparkline: true,
                        values: {
                            "2025-08-04": { v: 200.1, flag: "H" },
                            "2026-06-11": { v: 157.1, flag: "H" },
                            "2026-07-21": { v: 137.0, flag: "H" },
                            "2026-09-22": { v: 119.8, flag: "H" }
                        }
                    },
                    {
                        name: "Glucose Fasting (FBS)",
                        unit: "mg/dL",
                        ref: "< 100 (Pre-DM: 100-125)",
                        sparkline: true,
                        values: {
                            "2025-08-04": { v: 181, flag: "H" },
                            "2025-09-07": { v: 141, flag: "H" },
                            "2026-01-28": { v: 103, flag: "H" },
                            "2026-05-15": { v: 140, flag: "H" },
                            "2026-06-11": { v: 131, flag: "H" },
                            "2026-07-21": { v: 114, flag: "H" },
                            "2026-09-22": { v: 114, flag: "H" }
                        }
                    },
                    {
                        name: "Glucose Post-Prandial (PPBS)",
                        unit: "mg/dL",
                        ref: "< 140 (Pre-DM: 140-199)",
                        sparkline: true,
                        values: {
                            "2025-08-04": { v: 229, flag: "H" },
                            "2026-01-28": { v: 115, flag: "N" },
                            "2026-05-15": { v: 225, flag: "H" },
                            "2026-06-11": { v: 254, flag: "H" },
                            "2026-07-21": { v: 152, flag: "H" },
                            "2026-09-22": { v: 138, flag: "N" }
                        }
                    }
                ]
            },
            {
                id: "lft",
                title: "Liver Function Profile (LFT)",
                subtitle: "Transaminases, Bilirubin, Proteins & Biliary Enzymes",
                tests: [
                    {
                        name: "ALT / SGPT",
                        unit: "U/L",
                        ref: "0 - 45",
                        sparkline: true,
                        values: {
                            "2025-08-04": { v: 66, flag: "H" },
                            "2026-07-21": { v: 100, flag: "H" },
                            "2026-09-22": { v: 107, flag: "H" }
                        }
                    },
                    {
                        name: "AST / SGOT",
                        unit: "U/L",
                        ref: "0 - 40",
                        sparkline: true,
                        values: {
                            "2025-08-04": { v: 41, flag: "H" },
                            "2026-07-21": { v: 43, flag: "H" },
                            "2026-09-22": { v: 50, flag: "H" }
                        }
                    },
                    {
                        name: "Gamma GT (GGT)",
                        unit: "U/L",
                        ref: "8 - 61",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 64, flag: "H" }
                        }
                    },
                    {
                        name: "Alkaline Phosphatase (ALP)",
                        unit: "U/L",
                        ref: "40 - 130",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 83, flag: "N" },
                            "2026-09-22": { v: 94, flag: "N" }
                        }
                    },
                    {
                        name: "Lactate Dehydrogenase (LDH)",
                        unit: "U/L",
                        ref: "135 - 225",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 190, flag: "N" }
                        }
                    },
                    {
                        name: "Bilirubin, Total",
                        unit: "mg/dL",
                        ref: "< 1.1",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 0.60, flag: "N" },
                            "2026-09-22": { v: 0.27, flag: "N" }
                        }
                    },
                    {
                        name: "Bilirubin, Direct",
                        unit: "mg/dL",
                        ref: "< 0.30",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 0.26, flag: "N" },
                            "2026-09-22": { v: 0.11, flag: "N" }
                        }
                    },
                    {
                        name: "Bilirubin, Indirect",
                        unit: "mg/dL",
                        ref: "< 0.85",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 0.34, flag: "N" },
                            "2026-09-22": { v: 0.16, flag: "N" }
                        }
                    },
                    {
                        name: "Total Protein",
                        unit: "g/dL",
                        ref: "6.4 - 8.3",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 8.1, flag: "N" },
                            "2026-09-22": { v: 8.4, flag: "H" }
                        }
                    },
                    {
                        name: "Albumin, Serum",
                        unit: "g/dL",
                        ref: "3.5 - 5.2 (Jul: 3.97-4.94)",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 5.1, flag: "H" },
                            "2026-09-22": { v: 4.7, flag: "N" }
                        }
                    },
                    {
                        name: "Globulin, Serum",
                        unit: "g/dL",
                        ref: "2.0 - 3.5",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 3.0, flag: "N" },
                            "2026-09-22": { v: 3.7, flag: "H" }
                        }
                    },
                    {
                        name: "Albumin/Globulin (A/G) Ratio",
                        unit: "Ratio",
                        ref: "1.1 - 2.5",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 1.7, flag: "N" },
                            "2026-09-22": { v: 1.3, flag: "N" }
                        }
                    }
                ]
            },
            {
                id: "lipid",
                title: "Lipid Profile",
                subtitle: "Cholesterol, Triglycerides & Lipoprotein Fractions (Note: Lipaemia++ on 22 Sep 26)",
                tests: [
                    {
                        name: "Triglycerides",
                        unit: "mg/dL",
                        ref: "< 150",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 307, flag: "H" },
                            "2026-09-22": { v: 433, flag: "H" }
                        }
                    },
                    {
                        name: "HDL Cholesterol",
                        unit: "mg/dL",
                        ref: "40 - 60",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 30, flag: "L" },
                            "2026-09-22": { v: 34, flag: "L" }
                        }
                    },
                    {
                        name: "Total Cholesterol",
                        unit: "mg/dL",
                        ref: "< 200",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 191, flag: "N" },
                            "2026-09-22": { v: 170, flag: "N" }
                        }
                    },
                    {
                        name: "LDL Cholesterol",
                        unit: "mg/dL",
                        ref: "< 100 (Above Opt: 100-129)",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 100, flag: "N" },
                            "2026-09-22": { v: 115, flag: "H" }
                        }
                    },
                    {
                        name: "Non-HDL Cholesterol",
                        unit: "mg/dL",
                        ref: "< 130 (Above Des: 130-159)",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 161, flag: "H" },
                            "2026-09-22": { v: 136, flag: "H" }
                        }
                    },
                    {
                        name: "VLDL Cholesterol",
                        unit: "mg/dL",
                        ref: "<= 30.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 61.4, flag: "H" },
                            "2026-09-22": { v: 86.6, flag: "H" }
                        }
                    },
                    {
                        name: "Total Chol / HDL Ratio",
                        unit: "Ratio",
                        ref: "< 5.0 (Low Risk: 3.3-4.4)",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 6.4, flag: "H" },
                            "2026-09-22": { v: 5.0, flag: "N" }
                        }
                    },
                    {
                        name: "LDL / HDL Ratio",
                        unit: "Ratio",
                        ref: "0.5 - 3.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 3.3, flag: "H" },
                            "2026-09-22": { v: 3.4, flag: "H" }
                        }
                    }
                ]
            },
            {
                id: "thyroid",
                title: "Thyroid Function Panel",
                subtitle: "TSH (Ultrasensitive), Total T3 & Total T4",
                tests: [
                    {
                        name: "TSH (Ultrasensitive)",
                        unit: "µIU/mL",
                        ref: "0.270 - 4.200",
                        sparkline: true,
                        values: {
                            "2025-08-04": { v: 8.61, flag: "H" },
                            "2026-01-28": { v: 8.64, flag: "H" },
                            "2026-07-21": { v: 2.78, flag: "N" },
                            "2026-09-22": { v: 1.53, flag: "N" }
                        }
                    },
                    {
                        name: "Total T3 (Triiodothyronine)",
                        unit: "ng/dL",
                        ref: "80.0 - 200.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 93.52, flag: "N" },
                            "2026-09-22": { v: 109.0, flag: "N" }
                        }
                    },
                    {
                        name: "Total T4 (Thyroxine)",
                        unit: "µg/dL",
                        ref: "4.5 - 12.1",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 8.71, flag: "N" },
                            "2026-09-22": { v: 9.49, flag: "N" }
                        }
                    }
                ]
            },
            {
                id: "kft",
                title: "Metabolic & Kidney Function (KFT)",
                subtitle: "Renal Markers, Uric Acid & Serum Electrolytes",
                tests: [
                    {
                        name: "Creatinine, Serum",
                        unit: "mg/dL",
                        ref: "0.90 - 1.30",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 1.19, flag: "N" },
                            "2026-09-22": { v: 0.91, flag: "N" }
                        }
                    },
                    {
                        name: "Uric Acid, Serum",
                        unit: "mg/dL",
                        ref: "3.4 - 7.0",
                        sparkline: true,
                        values: {
                            "2025-08-04": { v: 4.2, flag: "N" },
                            "2026-07-21": { v: 5.7, flag: "N" },
                            "2026-09-22": { v: 6.0, flag: "N" }
                        }
                    },
                    {
                        name: "Blood Urea Nitrogen (BUN)",
                        unit: "mg/dL",
                        ref: "6 - 20",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 11, flag: "N" }
                        }
                    },
                    {
                        name: "BUN / Creatinine Ratio",
                        unit: "Ratio",
                        ref: "5.0 - 15.0",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 9.24, flag: "N" }
                        }
                    },
                    {
                        name: "Calcium, Serum",
                        unit: "mg/dL",
                        ref: "8.4 - 10.2",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 9.9, flag: "N" }
                        }
                    },
                    {
                        name: "Sodium, Serum",
                        unit: "mmol/L",
                        ref: "135 - 145",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 142.0, flag: "N" }
                        }
                    },
                    {
                        name: "Potassium, Serum",
                        unit: "mmol/L",
                        ref: "3.5 - 5.5",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 4.19, flag: "N" }
                        }
                    },
                    {
                        name: "Chloride, Serum",
                        unit: "mmol/L",
                        ref: "96 - 106",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 103.6, flag: "N" }
                        }
                    }
                ]
            },
            {
                id: "cbc",
                title: "Complete Blood Count (CBC) & Hematology",
                subtitle: "serial Platelets, RBC/WBC Indices & Differential",
                tests: [
                    {
                        name: "Platelet Count",
                        unit: "thou/µL",
                        ref: "150 - 410",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 260, flag: "N" },
                            "2026-07-29": { v: 160, flag: "N" },
                            "2026-07-30": { v: 160, flag: "N" },
                            "2026-09-22": { v: 286, flag: "N" }
                        }
                    },
                    {
                        name: "Mean Platelet Volume (MPV)",
                        unit: "fL",
                        ref: "6.8 - 10.9",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 7.7, flag: "N" },
                            "2026-09-22": { v: 11.1, flag: "H" }
                        }
                    },
                    {
                        name: "Hemoglobin (Hb)",
                        unit: "g/dL",
                        ref: "13.0 - 17.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 16.8, flag: "N" },
                            "2026-09-22": { v: 15.2, flag: "N" }
                        }
                    },
                    {
                        name: "Red Blood Cell (RBC) Count",
                        unit: "mil/µL",
                        ref: "4.5 - 5.5",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 5.40, flag: "N" },
                            "2026-09-22": { v: 5.23, flag: "N" }
                        }
                    },
                    {
                        name: "Hematocrit (PCV)",
                        unit: "%",
                        ref: "40 - 50",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 47.9, flag: "N" },
                            "2026-09-22": { v: 45.9, flag: "N" }
                        }
                    },
                    {
                        name: "Mean Corpuscular Volume (MCV)",
                        unit: "fL",
                        ref: "83 - 101",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 89.0, flag: "N" },
                            "2026-09-22": { v: 87.7, flag: "N" }
                        }
                    },
                    {
                        name: "Mean Corpuscular Hb (MCH)",
                        unit: "pg",
                        ref: "27.0 - 32.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 31.0, flag: "N" },
                            "2026-09-22": { v: 29.2, flag: "N" }
                        }
                    },
                    {
                        name: "MCHC",
                        unit: "g/dL",
                        ref: "31.5 - 34.5",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 34.2, flag: "N" },
                            "2026-09-22": { v: 33.2, flag: "N" }
                        }
                    },
                    {
                        name: "Red Cell Dist. Width (RDW)",
                        unit: "%",
                        ref: "11.6 - 14.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 13.4, flag: "N" },
                            "2026-09-22": { v: 12.7, flag: "N" }
                        }
                    },
                    {
                        name: "White Blood Cell (WBC) Count",
                        unit: "thou/µL",
                        ref: "4.0 - 10.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 7.90, flag: "N" },
                            "2026-09-22": { v: 8.40, flag: "N" }
                        }
                    },
                    {
                        name: "Neutrophils",
                        unit: "%",
                        ref: "40 - 80",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 51, flag: "N" },
                            "2026-09-22": { v: 54, flag: "N" }
                        }
                    },
                    {
                        name: "Lymphocytes",
                        unit: "%",
                        ref: "20 - 40",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 38, flag: "N" },
                            "2026-09-22": { v: 44, flag: "H" }
                        }
                    },
                    {
                        name: "Monocytes",
                        unit: "%",
                        ref: "2 - 10",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 7, flag: "N" },
                            "2026-09-22": { v: 1, flag: "L" }
                        }
                    },
                    {
                        name: "Eosinophils",
                        unit: "%",
                        ref: "1 - 6",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 3, flag: "N" },
                            "2026-09-22": { v: 1, flag: "N" }
                        }
                    },
                    {
                        name: "Basophils",
                        unit: "%",
                        ref: "0 - 2",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 1, flag: "N" }
                        }
                    },
                    {
                        name: "Absolute Neutrophil Count",
                        unit: "thou/µL",
                        ref: "2.0 - 7.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 4.03, flag: "N" },
                            "2026-09-22": { v: 4.54, flag: "N" }
                        }
                    },
                    {
                        name: "Absolute Lymphocyte Count",
                        unit: "thou/µL",
                        ref: "1.0 - 3.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 3.00, flag: "N" },
                            "2026-09-22": { v: 3.70, flag: "H" }
                        }
                    },
                    {
                        name: "Absolute Monocyte Count",
                        unit: "thou/µL",
                        ref: "0.2 - 1.0",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 0.55, flag: "N" },
                            "2026-09-22": { v: 0.08, flag: "L" }
                        }
                    },
                    {
                        name: "Absolute Eosinophil Count",
                        unit: "thou/µL",
                        ref: "0.02 - 0.50",
                        sparkline: true,
                        values: {
                            "2026-07-21": { v: 0.24, flag: "N" },
                            "2026-09-22": { v: 0.08, flag: "N" }
                        }
                    },
                    {
                        name: "ESR (1 hr)",
                        unit: "mm/hr",
                        ref: "0 - 10",
                        sparkline: false,
                        values: {
                            "2026-09-22": { v: 9, flag: "N" }
                        }
                    }
                ]
            },
            {
                id: "misc",
                title: "Urinalysis & Miscellaneous",
                subtitle: "Complete Urine Examination (21 Jul 2026)",
                tests: [
                    {
                        name: "Urine Glucose (Benedict's)",
                        unit: "Qual",
                        ref: "Not Detected",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: "Detected (+)", flag: "H" }
                        }
                    },
                    {
                        name: "Urine Protein / Ketones / Blood",
                        unit: "Qual",
                        ref: "Not Detected",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: "Not Detected", flag: "N" }
                        }
                    },
                    {
                        name: "Urine pH",
                        unit: "pH",
                        ref: "4.7 - 7.5",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 5.0, flag: "N" }
                        }
                    },
                    {
                        name: "Urine Specific Gravity",
                        unit: "SG",
                        ref: "1.003 - 1.035",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: 1.020, flag: "N" }
                        }
                    },
                    {
                        name: "Urine Pus Cells (WBCs)",
                        unit: "/HPF",
                        ref: "0 - 5",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: "2 - 3", flag: "N" }
                        }
                    },
                    {
                        name: "Urine Epithelial Cells",
                        unit: "/HPF",
                        ref: "0 - 5",
                        sparkline: false,
                        values: {
                            "2026-07-21": { v: "1 - 2", flag: "N" }
                        }
                    }
                ]
            }
        ];

        function createSparklineSVG(test) {
            if (!test.sparkline) return '<span class="text-slate-300 text-xs">&mdash;</span>';
            const pts = [];
            DATES.forEach((d, idx) => {
                const entry = test.values[d.id];
                if (entry && typeof entry.v === 'number') {
                    pts.push({ xIdx: idx, val: entry.v, flag: entry.flag });
                }
            });
            if (pts.length < 2) return '<span class="text-slate-300 text-xs">&mdash;</span>';

            const w = 76, h = 24, pad = 4;
            const minV = Math.min(...pts.map(p => p.val));
            const maxV = Math.max(...pts.map(p => p.val));
            const minX = pts[0].xIdx;
            const maxX = pts[pts.length - 1].xIdx;

            const coords = pts.map(p => {
                const x = maxX === minX ? w / 2 : pad + ((p.xIdx - minX) / (maxX - minX)) * (w - pad * 2);
                const y = maxV === minV ? h / 2 : (h - pad) - ((p.val - minV) / (maxV - minV)) * (h - pad * 2);
                return { x: x.toFixed(1), y: y.toFixed(1), flag: p.flag };
            });

            const polyPoints = coords.map(c => `${c.x},${c.y}`).join(' ');
            const lastPt = coords[coords.length - 1];
            const strokeColor = lastPt.flag === 'H' ? '#e11d48' : (lastPt.flag === 'L' ? '#0284c7' : '#10b981');

            const circles = coords.map(c => {
                const fill = c.flag === 'H' ? '#e11d48' : (c.flag === 'L' ? '#0284c7' : '#64748b');
                return `<circle cx="${c.x}" cy="${c.y}" r="2.2" fill="${fill}" />`;
            }).join('');

            return `
                <svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" class="overflow-visible inline-block">
                    <polyline fill="none" stroke="${strokeColor}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" points="${polyPoints}" />
                    ${circles}
                </svg>
            `;
        }

        function formatCell(entry) {
            if (!entry) return `<span class="text-slate-300 mono text-xs">&mdash;</span>`;
            if (entry.flag === "H") {
                return `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-rose-50 text-rose-700 border border-rose-200 font-semibold mono text-xs shadow-2xs">${entry.v}<span class="text-[10px] font-bold bg-rose-200/80 text-rose-900 px-1 rounded">H</span></span>`;
            }
            if (entry.flag === "L") {
                return `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-sky-50 text-sky-700 border border-sky-200 font-semibold mono text-xs shadow-2xs">${entry.v}<span class="text-[10px] font-bold bg-sky-200/80 text-sky-900 px-1 rounded">L</span></span>`;
            }
            return `<span class="text-slate-700 mono text-xs font-medium">${entry.v}</span>`;
        }

        function renderDashboard(onlyAbnormal = false) {
            const container = document.getElementById('panelsContainer');
            container.innerHTML = '';

            LAB_PANELS.forEach(panel => {
                const activeDates = DATES.filter(d =>
                    panel.tests.some(t => t.values[d.id] !== undefined)
                );

                const filteredTests = panel.tests.filter(test => {
                    if (!onlyAbnormal) return true;
                    return Object.values(test.values).some(v => v.flag === 'H' || v.flag === 'L');
                });

                if (filteredTests.length === 0) return;

                const section = document.createElement('section');
                section.className = "bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden";

                const rowsHTML = filteredTests.map(test => {
                    const hasAbnormal = Object.values(test.values).some(v => v.flag === 'H' || v.flag === 'L');
                    const dateCells = activeDates.map(d => {
                        const entry = test.values[d.id];
                        return `<td class="px-3 py-2.5 text-center whitespace-nowrap border-b border-slate-100">${formatCell(entry)}</td>`;
                    }).join('');

                    return `
                        <tr class="hover:bg-slate-50/80 transition-colors group">
                            <td class="sticky left-0 z-10 bg-white group-hover:bg-slate-50 px-3.5 py-2.5 border-b border-r border-slate-200 sticky-col-shadow min-w-[170px] max-w-[220px]">
                                <div class="font-semibold text-xs sm:text-sm text-slate-800 flex items-center gap-1.5">
                                    ${hasAbnormal ? '<span class="w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0"></span>' : ''}
                                    <span class="truncate" title="${test.name}">${test.name}</span>
                                </div>
                                <div class="text-[11px] text-slate-400 mono md:hidden">Ref: ${test.ref} ${test.unit}</div>
                            </td>
                            <td class="hidden md:table-cell px-3 py-2.5 text-xs text-slate-500 mono whitespace-nowrap border-b border-slate-100">
                                ${test.ref} <span class="text-slate-400">${test.unit}</span>
                            </td>
                            <td class="px-2 py-2.5 text-center whitespace-nowrap border-b border-r border-slate-100 bg-slate-50/40">
                                ${createSparklineSVG(test)}
                            </td>
                            ${dateCells}
                        </tr>
                    `;
                }).join('');

                const dateHeaders = activeDates.map(d => `
                    <th class="px-3 py-2.5 text-center text-xs font-semibold text-slate-700 uppercase tracking-wider whitespace-nowrap bg-slate-100/80 border-b border-slate-200 mono">
                        ${d.label}
                    </th>
                `).join('');

                section.innerHTML = `
                    <div class="px-4 py-3 bg-slate-800 text-white flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                        <div>
                            <h2 class="text-sm sm:text-base font-bold tracking-tight">${panel.title}</h2>
                            <p class="text-xs text-slate-300">${panel.subtitle}</p>
                        </div>
                        <span class="text-[11px] mono bg-slate-700 text-slate-200 px-2 py-0.5 rounded self-start sm:self-center">
                            ${filteredTests.length} Parameter${filteredTests.length > 1 ? 's' : ''}
                        </span>
                    </div>
                    <div class="overflow-x-auto no-scrollbar">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr>
                                    <th class="sticky left-0 z-20 bg-slate-100 px-3.5 py-2.5 text-xs font-bold text-slate-700 uppercase tracking-wider border-b border-r border-slate-200 sticky-col-shadow">
                                        Biomarker
                                    </th>
                                    <th class="hidden md:table-cell px-3 py-2.5 text-xs font-semibold text-slate-600 uppercase tracking-wider bg-slate-100/80 border-b border-slate-200">
                                        Reference Range
                                    </th>
                                    <th class="px-2 py-2.5 text-center text-xs font-semibold text-slate-600 uppercase tracking-wider bg-slate-100/80 border-b border-r border-slate-200">
                                        Trend
                                    </th>
                                    ${dateHeaders}
                                </tr>
                            </thead>
                            <tbody>
                                ${rowsHTML}
                            </tbody>
                        </table>
                    </div>
                `;

                container.appendChild(section);
            });
        }

        document.getElementById('abnormalToggle').addEventListener('change', (e) => {
            renderDashboard(e.target.checked);
        });

        renderDashboard(false);
    </script>
</body>
</html>
"""

components.html(HTML_CODE, height=2800, scrolling=True)
