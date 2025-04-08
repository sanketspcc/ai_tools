# import cv2
# import streamlit as st
# from PIL import Image
# from streamlit_drawable_canvas import st_canvas
# import numpy as np


# st.set_page_config(page_title="Ball Coordinate Detector Tool",initial_sidebar_state="collapsed")

# # Streamlit app
# st.title("Ball Coordinate Detector Tool")

# # Upload video
# uploaded_video = st.file_uploader("Upload a video clip (2-4 seconds):", type=["mp4", "avi", "mov"])

# if uploaded_video is not None:
#     # Save the uploaded video temporarily
#     video_path = "temp_video.mp4"
#     with open(video_path, "wb") as f:
#         f.write(uploaded_video.read())
    
#     # Open the video with OpenCV
#     cap = cv2.VideoCapture(video_path)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     st.write(f"Total Frames: {total_frames}, FPS: {fps}")

#     # Initialize session state for selected frame
#     if "selected_frame" not in st.session_state:
#         st.session_state.selected_frame = 0

#     # Function to update session state when slider changes
#     def update_slider():
#         st.session_state.selected_frame = st.session_state.slider_frame

#     # Function to update session state when number input changes
#     def update_number():
#         st.session_state.selected_frame = st.session_state.number_frame

#     # Two-column layout for slider and manual input
#     col1, col2 = st.columns(2)

#     # Frame slider
#     with col1:
#         st.slider(
#             "Select a frame:",
#             0,
#             total_frames - 1,
#             value=st.session_state.selected_frame,
#             key="slider_frame",
#             on_change=update_slider,
#         )

#     # Manual frame number input
#     with col2:
#         st.number_input(
#             "Enter frame number:",
#             min_value=0,
#             max_value=total_frames - 1,
#             value=st.session_state.selected_frame,
#             step=1,
#             key="number_frame",
#             on_change=update_number,
#         )

#     # Read the selected frame
#     cap.set(cv2.CAP_PROP_POS_FRAMES, st.session_state.selected_frame)
#     ret, frame = cap.read()

#     if ret:
#         # Convert BGR to RGB
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Display the frame with a drawable canvas
#         st.write(f"Frame {st.session_state.selected_frame}")
#         canvas_result = st_canvas(
#             fill_color="rgba(0, 0, 0, 0)",  # Transparent fill
#             stroke_width=0,  # Disable drawing
#             stroke_color="#FFFFFF",
#             background_color="#FFFFFF",
#             background_image=Image.fromarray(frame_rgb),
#             update_streamlit=True,
#             height=frame.shape[0],
#             width=frame.shape[1],
#             drawing_mode="point",  # Enable clicking
#             key="canvas",
#         )

#         # Get click coordinates and draw marker on original frame
#         if canvas_result.json_data is not None:
#             objects = canvas_result.json_data["objects"]
#             if len(objects) > 0:
#                 # Get the last clicked coordinates
#                 x, y = objects[-1]["left"], objects[-1]["top"]
#                 x, y = int(x), int(y)

#                 # Draw a small circle at the clicked coordinates on the original frame
#                 cv2.circle(frame_rgb, (x, y), 5, (255, 0, 0), -1)  # Red marker

#                 # Display the updated frame with the marker directly
#                 st.image(frame_rgb, caption=f"Frame {st.session_state.selected_frame} with Marker")

#                 # Display clicked coordinates
#                 st.write(f"Clicked Coordinates: (x={x}, y={y})")
#     else:
#         st.error("Unable to read the frame. Please try again.")

#     cap.release()
