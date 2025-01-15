import streamlit as st

st.set_page_config(page_title="AI Tools Hub", page_icon="🛠", layout="centered",initial_sidebar_state="collapsed")

st.title("🚀 AI Tools Hub")
st.subheader("Effortlessly Trim Videos & Manipulate PDFs with AI-powered tools!")

st.markdown("---")

st.header("📌 Available Tools")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎬 Open Video Trimmer App"):
        st.session_state["page"] = "video_trimmer"

with col2:
    if st.button("📄 Open PDF Editor App"):
        st.session_state["page"] = "pdf_editor"

# Navigate based on session state
if "page" in st.session_state:
    if st.session_state["page"] == "video_trimmer":
        st.switch_page("pages/video_trimmer.py")
    elif st.session_state["page"] == "pdf_editor":
        st.switch_page("pages/pdf_editor.py")
