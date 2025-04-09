import streamlit as st

st.set_page_config(page_title="AI Tools Hub", page_icon="🛠", layout="centered",initial_sidebar_state="collapsed")

st.title("🚀 AI Tools Hub")
st.subheader("Effortlessly Trim Videos & Manipulate PDFs with AI-powered tools!")

st.markdown("---")

st.header("📌 Available Tools")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎬 Open Video Trimmer App"):
        st.session_state["page"] = "video_trimmer"
    
    if st.button("🏏 Generate Batting Reports"):
        st.session_state["page"] = "batting_reports"

with col2:
    if st.button("📄 Open PDF Editor App"):
        st.session_state["page"] = "pdf_editor"

with col3:
    if st.button("🥎Open Ball Coords Tracking Tool"):
        st.session_state['page'] = "ball_coords_tool"


# Navigate based on session state
if "page" in st.session_state:
    if st.session_state["page"] == "video_trimmer":
        st.switch_page("pages/video_trimmer.py")
    elif st.session_state["page"] == "pdf_editor":
        st.switch_page("pages/pdf_editor.py")
    elif st.session_state["page"] == "ball_coords_tool":
        st.switch_page("pages/ball_coords_tool.py")
    elif st.session_state["page"] == "batting_reports":
        st.switch_page("pages/batting_reports.py")