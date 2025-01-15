import streamlit as st
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import tempfile
import cv2

# Function to trim video
def trim_video(input_path, output_path, start_time, end_time):
    ffmpeg_extract_subclip(input_path, start_time, end_time, targetname=output_path)

# Page Layout
st.set_page_config(page_title="Video Trimmer", layout="wide")
st.title("🎥 Video Trimmer")
st.markdown("---")

# File Upload Section
with st.container():
    st.header("📂 Upload Video")
    uploaded_video = st.file_uploader("📤 Upload your video (MP4, AVI)", type=['mp4', 'avi'])
    
if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_video.read())
        temp_video_path = temp_video.name
    
    # Display Video
    st.video(temp_video_path)
    
    # Get video duration
    cap = cv2.VideoCapture(temp_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    cap.release()

    # Video Trimming Section
    st.header("✂ Trim Video Clips")
    num_clips = st.slider("🎬 How many clips to create?", min_value=1, max_value=10, value=3)
    
    clip_times = []
    for i in range(num_clips):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            start_time_str = st.text_input(f"🎬 Clip {i+1} Start (MM:SS)", "00:00", key=f"start_{i}")
        with col2:
            end_time_str = st.text_input(f"🎬 Clip {i+1} End (MM:SS)", "00:05", key=f"end_{i}")

        start_match = re.match(r'(\d{2}):(\d{2})', start_time_str)
        end_match = re.match(r'(\d{2}):(\d{2})', end_time_str)
        
        if start_match and end_match:
            start_minutes, start_seconds = map(int, start_match.groups())
            end_minutes, end_seconds = map(int, end_match.groups())
            
            start_time = start_minutes * 60 + start_seconds
            end_time = end_minutes * 60 + end_seconds

            if start_time < end_time <= duration:
                clip_times.append((start_time, end_time))
            else:
                st.error(f"⚠ Invalid timing for Clip {i+1}. Check start & end times.")
        else:
            st.error(f"⚠ Incorrect format for Clip {i+1}. Use MM:SS.")

    if st.button("🎬 Generate Clips"):
        trimmed_videos = []
        for idx, (start, end) in enumerate(clip_times):
            output_clip_path = f"{temp_video_path}_clip_{idx+1}.mp4"
            trim_video(temp_video_path, output_clip_path, start, end)
            trimmed_videos.append(output_clip_path)
            
        st.success("✅ Clips created successfully!")
        
        # Download buttons
        for idx, clip in enumerate(trimmed_videos):
            with open(clip, "rb") as file:
                st.download_button(label=f"📥 Download Clip {idx+1}", data=file, file_name=f"trimmed_clip_{idx+1}.mp4", mime="video/mp4")
