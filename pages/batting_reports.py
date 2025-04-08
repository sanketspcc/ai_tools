import streamlit as st
from batting_reports_generation import generate_report

st.set_page_config(page_title="Batting Reports", layout="wide", initial_sidebar_state="collapsed")

st.title("📄 Batting Reports Tool")
assessment_id = st.text_input("Enter Assessment Id:")
if st.button("Generate Report"):
    report_path = generate_report(int(assessment_id))  # This should return the full path to the generated PDF

    if report_path:
        with open(report_path, "rb") as f:
            pdf_bytes = f.read()

        file_name = report_path.split("/")[-1]  # Extract the filename from the path

        st.success("✅ Report generated successfully!")

        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf"
        )
    else:
        st.error("❌ Failed to generate the report.")
