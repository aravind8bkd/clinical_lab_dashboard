# EMR Dashboard

A Streamlit-hosted dashboard for viewing an individual's clinical laboratory results over time. Results are grouped into panels and shown in date-based tables with reference ranges, high/low flags, and numeric trend sparklines.

## Run locally

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the app from the repository root:

   ```bash
   streamlit run streamlit_app.py
   ```

## Dashboard contents

The dashboard currently includes these panels:

- Glycemic and diabetes control
- Liver function
- Lipid profile
- Thyroid and vitamins
- Metabolic and kidney function
- Complete blood count and hematology
- Urinalysis and miscellaneous results

The dates and results currently encoded in the app span August 2025 through September 2026. Each panel shows only dates for which at least one of its tests has a recorded result.

### Reading the tables

- `H` and `L` mark results flagged high and low in the source data. `N` is displayed without an abnormal badge.
- Reference ranges and units are shown alongside each test.
- Tests are ordered by the number of recorded results, most frequent first, within each panel.
- **Show Only Out-of-Range** filters the table to tests that have at least one `H` or `L` result. It does not remove normal readings from those tests' histories.
- Trend sparklines are drawn only for numeric tests with at least two results.
- Tables can be scrolled horizontally on narrow screens.

Flags are explicitly entered in the data; the app does not calculate whether a result is outside its reference range.

## Updating the results

The current dashboard data is embedded in `streamlit_app.py`; the app does not load results from a database or CSV file.

1. Add or update a date in the `DATES` array, using an ISO date (`YYYY-MM-DD`) as its `id` and a matching display `label`. Keep the dates in chronological order.
2. Add or update each result under the matching date key in the relevant test's `values` object. Each result has a value (`v`) and a manually supplied flag (`H`, `L`, or `N`).
3. Check the test name, unit, reference range, and flag against the original lab report before publishing changes.

The `data/gdp_data.csv` file is leftover GDP-template data and is not used by the current dashboard.

## Implementation

- `streamlit_app.py` sets the Streamlit page configuration and embeds the dashboard as HTML, CSS, and JavaScript using `st.components.v1.html`.
- The tables, filter, and sparklines are rendered in the browser from the hard-coded data.
- Tailwind CSS and the Inter/JetBrains Mono fonts are loaded from external CDNs, so those styles and fonts require network access.
- `requirements.txt` currently lists Streamlit and pandas; the current dashboard does not use pandas.

## Privacy and intended use

This dashboard contains person-specific health information and identifying details in its source code. Review the data and confirm that repository visibility, deployment access controls, and sharing are appropriate before publishing or deploying it. Do not add identifiable patient data to a public repository without the necessary authorization.

This is a personal visualization, not a diagnostic or treatment tool. Results, flags, and reference ranges should be verified against the original laboratory reports and interpreted by a qualified healthcare professional.
