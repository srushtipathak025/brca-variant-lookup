# BRCA Variant Lookup

A web app that looks up BRCA gene variants in the NIH ClinVar database and returns a plain-English summary of what the variant means clinically.

## What it does
- Takes a ClinVar ID as input
- Queries the NCBI ClinVar API in real time
- Returns the gene, DNA change, protein change, condition, and clinical classification
- Color-codes results by significance (Pathogenic, Likely pathogenic, Uncertain, Benign)
- Explains each classification in plain English

## Why I built this
As a pre-med student, I wanted to understand how genetic variant data is stored and interpreted clinically. This tool makes ClinVar data accessible without needing a bioinformatics background.

## How to run it
1. Install dependencies: `pip install streamlit requests`
2. Run the app: `python -m streamlit run app.py`
3. Enter a ClinVar ID (e.g. 4845222) and click Look up variant

## Built with
- Python
- Streamlit
- NCBI ClinVar API (free, no key required)