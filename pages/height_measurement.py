# import streamlit as st
# import fitz
# from PIL import Image
# import io
# from streamlit_sortables import sort_items
# import os
# # os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
# from height_utils import process_single_video, process_single_image

# st.set_page_config(page_title="Height Measurement", layout="wide",initial_sidebar_state="collapsed")

# st.title("📄 Height Measurement Tool")


# IMAGE_PATH = '/Height/abi_height_img.png'
# # IMAGE_PATH = 'test2.jpeg'
# # Marker Details
# DISTANCE_FROM_GROUND = 20
# DISTANCE_BETWEEN_MARKERS = 70
# ORIENTATION = "blank_left"
# NUM_MARKERS = 3



# import cv2
# import matplotlib.pyplot as plt
# input_image_path = IMAGE_PATH

# input_image_frame = cv2.imread(input_image_path)


# processed_image, top_pixel, pred_height, angle = process_single_image(input_image_path,
#                                                                       input_image_frame,
#                                                                       output_image_dir='',
#                                                                       output_filename='test1_output.png',
#                                                                       num_markers=NUM_MARKERS,
#                                                                       marker_distance_from_ground=DISTANCE_FROM_GROUND,
#                                                                       marker_orientation=ORIENTATION,
#                                                                       distance_between_markers=DISTANCE_BETWEEN_MARKERS
#                                                                       )

# # print("Output video can be found at: {}".format(processed_image))
# print("Predicted Height is: {:.1f}".format(pred_height))


# plt.imshow(processed_image), top_pixel, angle
