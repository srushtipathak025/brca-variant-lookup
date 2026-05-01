import streamlit as st
import requests

st.set_page_config(page_title="BRCA Variant Lookup", page_icon="🧬", layout="centered")

st.title("🧬 BRCA Variant Lookup")
st.write("Enter a ClinVar ID to get a plain-English summary of a BRCA gene variant.")

SIG_CONFIG = {
    "Pathogenic": {
        "color": "#A32D2D",
        "background": "#FCEBEB",
        "emoji": "⛔",
        "meaning": "This variant is disease-causing. It is strongly linked to increased breast or ovarian cancer risk based on substantial scientific evidence. Patients with this variant are typically referred for genetic counseling and enhanced screening."
    },
    "Likely pathogenic": {
        "color": "#854F0B",
        "background": "#FAEEDA",
        "emoji": "⚠️",
        "meaning": "This variant is probably disease-causing, though the evidence is not yet fully definitive. Most clinicians treat this similarly to Pathogenic. Genetic counseling is strongly recommended."
    },
    "Uncertain significance": {
        "color": "#5F5E5A",
        "background": "#F1EFE8",
        "emoji": "❓",
        "meaning": "It is currently unclear whether this variant affects cancer risk. This is one of the most common classifications — it does not mean the variant is dangerous, just that more research is needed. Reclassification often happens as more data is collected."
    },
    "Likely benign": {
        "color": "#185FA5",
        "background": "#E6F1FB",
        "emoji": "✅",
        "meaning": "This variant is probably harmless and unlikely to meaningfully affect cancer risk. It is generally not considered clinically actionable."
    },
    "Benign": {
        "color": "#3B6D11",
        "background": "#EAF3DE",
        "emoji": "✅",
        "meaning": "This variant is considered harmless and is not associated with increased cancer risk. It is a normal variation in the population."
    },
}

with st.form("lookup_form"):
    variant_id = st.text_input("ClinVar ID", placeholder="e.g. 4845222")
    st.caption("Not sure of your ClinVar ID? Try: 4845222, 4842662, or 4844791")
    submitted = st.form_submit_button("Look up variant")

if submitted and variant_id:
    with st.spinner("Looking up variant in ClinVar..."):
        try:
            response = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
                params={"db": "clinvar", "id": variant_id.strip(), "retmode": "json"}
            )
            data = response.json()
            v = data["result"][variant_id.strip()]

            gene = v["genes"][0]["symbol"] if v.get("genes") else "Unknown"
            dna = v["variation_set"][0]["cdna_change"] if v.get("variation_set") else "Unknown"
            protein = f"p.{v['protein_change']}" if v.get("protein_change") else "Not available"
            sig = v["germline_classification"]["description"] if v.get("germline_classification") else "Not classified"
            evidence = v["germline_classification"]["review_status"] if v.get("germline_classification") else "Unknown"
            trait_set = v["germline_classification"].get("trait_set", [])
            condition = trait_set[0]["trait_name"] if trait_set else "Unknown"
            consequences = ", ".join(v.get("molecular_consequence_list", [])) or "Not available"
            accession = v.get("accession", "N/A")

            config = SIG_CONFIG.get(sig, {
                "color": "#5F5E5A",
                "background": "#F1EFE8",
                "emoji": "❓",
                "meaning": f"Classification: {sig}. No additional interpretation available."
            })

            st.markdown("---")

            # Classification banner
            st.markdown(
                f"""
                <div style="background:{config['background']}; border-left: 5px solid {config['color']};
                padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1rem;">
                    <div style="font-size:13px; color:{config['color']}; font-weight:600; margin-bottom:4px;">
                        CLASSIFICATION
                    </div>
                    <div style="font-size:22px; font-weight:700; color:{config['color']};">
                        {config['emoji']} {sig}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Variant details grid
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Gene", gene)
                st.metric("DNA Change", dna)
                st.metric("Condition", condition)
            with col2:
                st.metric("Protein Change", protein)
                st.metric("Accession", accession)
                st.metric("Evidence Level", evidence)

            st.markdown("**Molecular consequence**")
            st.write(consequences)

            # Plain English meaning
            st.markdown("### What this means")
            st.info(config["meaning"])

            # Disclaimer
            st.caption("Data sourced from NCBI ClinVar. This tool is for educational purposes only and does not constitute medical advice. Always consult a genetic counselor or physician.")

        except Exception as e:
            st.error(f"Could not retrieve variant. Double-check the ClinVar ID and try again.\n\nError: {e}")