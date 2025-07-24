import os
from moviepy.config import change_settings

# On Streamlit Community Cloud (Linux), ImageMagick is usually in /usr/bin/convert
# You might also need to use 'magick' instead of 'convert' for newer ImageMagick versions
# Let's try 'convert' first as it's a common symlink/binary.

# Check if 'convert' or 'magick' exists in common paths
imagemagick_path = None
if os.path.exists("/usr/bin/convert"):
    imagemagick_path = "/usr/bin/convert"
elif os.path.exists("/usr/bin/magick"):
    imagemagick_path = "/usr/bin/magick"

if imagemagick_path:
    change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
    print(f"MoviePy: ImageMagick binary set to {imagemagick_path}")
else:
    print("MoviePy: Could not find ImageMagick binary at expected paths.")
    # Handle this case, e.g., raise an error or inform the user

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
