import streamlit as st
from batting_reports_generation import generate_report
import time

st.set_page_config(
    page_title="Batting Reports",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# Custom CSS styling
st.markdown("""
    <style>
        .main {padding: 30px 15px;}
        .report-title {color: #2B3467; text-align: center;}
        .stButton button {width: 100%; background-color: #2B3467; color: white;}
        .stDownloadButton button {background-color: #009E8F !important;}
        .success-box {padding: 20px; background-color: #E8F3EA; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="report-title">🏏 Batting Performance Analysis Report</h1>', unsafe_allow_html=True)

# Main content container
with st.container():
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form(key='report_form'):
            st.subheader("🔍 Report Generation")
            assessment_id = st.text_input(
                "Assessment ID:",
                placeholder="Enter your unique assessment ID",
                help="Please provide the assessment ID received after your batting evaluation"
            )
            
            submit_btn = st.form_submit_button(
                "🚀 Generate Performance Report",
                use_container_width=True
            )

        if submit_btn:
            if not assessment_id.strip():
                st.warning("⚠️ Please enter a valid Assessment ID")
            else:
                try:
                    with st.spinner("📊 Analyzing swing metrics and generating report..."):
                        progress_bar = st.progress(0)
                        
                        # Simulated progress updates
                        for percent_complete in range(0, 101, 10):
                            progress_bar.progress(percent_complete)
                            # Replace this sleep with actual generation steps
                            time.sleep(0.1)
                        
                        report_path = generate_report(int(assessment_id))
                        progress_bar.empty()

                    if report_path:
                        st.markdown("---")
                        with st.container():
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.success("✅ Report Successfully Generated!")
                            
                            with open(report_path, "rb") as f:
                                pdf_bytes = f.read()
                            
                            file_name = report_path.split("/")[-1]
                            st.markdown(f"**Assessment ID:** `{assessment_id}`")
                            
                            st.download_button(
                                label="📥 Download Full Analysis Report",
                                data=pdf_bytes,
                                file_name=file_name,
                                mime="application/pdf",
                                use_container_width=True
                            )
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("❌ Report generation failed. Please check the Assessment ID and try again.")

                except ValueError:
                    st.error("🛑 Invalid Assessment ID format. Please enter a numeric ID.")
                except Exception as e:
                    st.error(f"⚠️ An error occurred: {str(e)}")

# st.markdown("---")
# st.markdown("""
#     <div style="text-align: center; color: #666;">
#         Need help? Contact support@battinganalysis.com | 
#         © 2024 Batting Performance Analytics
#     </div>
#     """, unsafe_allow_html=True)