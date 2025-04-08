# import cv2
# import numpy as np
# import mediapipe as mp
# import os

# from ultralytics import YOLO
# from tqdm import tqdm

# FRAMES_OUTPUT_BASE_DIR = "data/input_video_frames"
# PROCESSED_FRAMES_OUTPUT_BASE_DIR = "data/frames_with_markers"
# PROCESSED_VIDEO_PATH = "data/output_videos"


# # Load YOLOv8 model (pretrained on COCO dataset)
# yolo_model = YOLO('yolov8n.pt')  # You can use a different YOLOv8 model like 'yolov8m.pt'


# def validate_path(path_string):
#     if not os.path.exists(path_string):
#         os.makedirs(path_string)
#     return path_string


# # Function to detect ArUco markers and return their center pixel positions
# def detect_aruco_markers(image, VERBOSE=False):
#     # Define the dictionary for 4x4 ArUco markers
#     arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
#     arucoParams = cv2.aruco.DetectorParameters()
#     detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
#     (corners, ids, rejected) = detector.detectMarkers(image)

#     # (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
#     #                                                    parameters=arucoParams)

#     # Calculate the center of each detected marker
#     marker_centers = []
#     for marker_corners in corners:
        
#         if VERBOSE:
#             print("ArUco Marker Corner Co Ordinates:")
#             print(marker_corners[0][0])
#             print(marker_corners[0][1])
#             print(marker_corners[0][2])
#             print(marker_corners[0][3])
#         # Average the four corner coordinates to get the center
#         center_x = np.mean(marker_corners[0][:, 0])
#         center_y = np.mean(marker_corners[0][:, 1])
#         marker_centers.append((center_x, center_y))
#          # marker_centers.append(((marker_corners[0][0][0]+marker_corners[0][3][0])/2,(marker_corners[0][0][1]+marker_corners[0][3][1])/2))
#         # marker_centers.append(((marker_corners[0][2][0]+marker_corners[0][1][0])/2,(marker_corners[0][2][1]+marker_corners[0][1][1])/2))
#         marker_centers.append(((marker_corners[0][0][0]+marker_corners[0][1][0])/2,(marker_corners[0][0][1]+marker_corners[0][1][1])/2))
#         marker_centers.append(((marker_corners[0][2][0]+marker_corners[0][3][0])/2,(marker_corners[0][2][1]+marker_corners[0][3][1])/2))
    
#     if VERBOSE:
#         print("Marker Centers: ", marker_centers)

#     return marker_centers, ids


# # Function to detect person and return the top pixel point
# def detect_person_top_point_vYOLO(image, model):
#     results = model(image)

#     # Extract the bounding boxes and classes from the YOLO results
#     boxes = results[0].boxes.xyxy.cpu().numpy()  # Bounding boxes [x1, y1, x2, y2]
#     classes = results[0].boxes.cls.cpu().numpy()  # Class labels

#     # Iterate over all detections to find the person class
#     person_box = None
#     for box, class_name in zip(boxes, classes):
#         if class_name == 0:  # '0' is the class id for 'person' in COCO dataset
#             person_box = box  # This is the person's bounding box
#             break

#     if person_box is None:
#         print("Error: No person detected in the image.")
#         return None

#     # Extract the top pixel point (y1) of the bounding box
#     x1, y1, x2, y2 = person_box
#     top_pixel_point = (int((x1 + x2) / 2), int(y1))  # Middle of top edge
#     bottom_pixel_point = (int((x1 + x2) / 2), int(y2)) # Middl of bottom edge

#     return image, top_pixel_point, bottom_pixel_point


# def detect_person_top_point_vMP_v2(image):    
#     # Initialize mediapipe pose detection
#     mp_face_mesh = mp.solutions.face_mesh
#     mp_pose = mp.solutions.pose
    
#     pose = mp_pose.Pose()
#     face_mesh = mp_face_mesh.FaceMesh()
    
#     # Initialize drawing utilities for visualization
#     # mp_drawing = mp.solutions.drawing_utils
    
#     # Load the image
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # Perform face Detection
#     face_results = face_mesh.process(image_rgb)
    
#     # Perform pose detection
#     pose_results = pose.process(image_rgb)
    
#     top_pixel_coords = None
#     bottom_pixel_coords = None
    
#     print(face_results.multi_face_landmarks)
    
#     # Draw landmarks for Face Mesh
#     if face_results.multi_face_landmarks:
#         for face_landmarks in face_results.multi_face_landmarks:
#             # Get the top of the head (landmark index 10 is generally close to the top)
#             top_head = face_landmarks.landmark[10]
#             top_head_x = int(top_head.x * image.shape[1])
#             top_head_y = int(top_head.y * image.shape[0])

#             # Draw circle on the top of the head
#             top_pixel_coords = (top_head_x, top_head_y)
            
#     if pose_results.pose_landmarks:

#         # Get heel landmarks
#         left_heel = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL.value]
#         right_heel = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL.value]

#         # Get coordinates and ensure they are integers
#         left_heel_coords = (int(left_heel.x * image.shape[1]), int(left_heel.y * image.shape[0]))
#         right_heel_coords = (int(right_heel.x * image.shape[1]), int(right_heel.y * image.shape[0]))

#         bottom_pixel_coords = (int((left_heel_coords[0] + right_heel_coords[0])/2), 
#                                int((left_heel_coords[1] + right_heel_coords[1])/2))
        
#     return image, top_pixel_coords, bottom_pixel_coords

  
# def detect_person_top_point_vMP_v1(image):    
#     # Initialize mediapipe pose detection
#     mp_pose = mp.solutions.pose
    
#     pose = mp_pose.Pose()
    
#     # Initialize drawing utilities for visualization
#     # mp_drawing = mp.solutions.drawing_utils
    
#     # Load the image
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # Perform pose detection
#     pose_results = pose.process(image_rgb)
          
#     # Check if pose landmarks are detected
#     if pose_results.pose_landmarks:
#         # Get landmarks for nose, left eye, and right eye (to estimate the forehead)
#         landmarks = pose_results.pose_landmarks.landmark
    
#         nose = landmarks[mp_pose.PoseLandmark.NOSE]
#         left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
#         right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]
    
#         # Estimate forehead top point: midpoint between eyes and above the nose
#         forehead_x = int((left_eye.x + right_eye.x) / 2 * image.shape[1])
        
#         offset = int((nose.y * image.shape[0] - (left_eye.y * image.shape[0] + right_eye.y * image.shape[0])//2) * 3.5)

#         forehead_y = int(nose.y * image.shape[0]) - offset
        
#         # Draw the estimated forehead point on the image
#         cv2.circle(image, (forehead_x, forehead_y), 5, (0, 255, 0), -1)
        
#         left_heel = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
#         right_heel = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value]

#         # Get coordinates
#         left_foot_coords = (int(left_heel.x * image.shape[1]), int(left_heel.y * image.shape[0]))
#         right_foot_coords = (int(right_heel.x * image.shape[1]), int(right_heel.y * image.shape[0]))
        
#         # Draw pose landmarks for reference
#         # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
#         top_pixel_coords = (forehead_x, forehead_y)
#         bottom_pixel_coords = (int((left_foot_coords[0] + right_foot_coords[0])/2), 
#                                int((left_foot_coords[1] + right_foot_coords[1])/2))

#         return image, top_pixel_coords, bottom_pixel_coords

#     return None, None, None


# # Function to fit a polynomial curve between pixel positions and real-world distances
# def fit_polynomial(pixel_positions, real_world_distances, degree):
#     # Fit a polynomial to relate pixel positions to real-world distances

#     coefficients = np.polyfit(pixel_positions, real_world_distances, degree)
#     return coefficients


# # Function to convert pixel position to real-world distance using the polynomial
# def pixel_to_real_distance(pixel_position, coefficients):
#     return np.polyval(coefficients, pixel_position)


# def calculate_real_world_distances(distance_from_ground, num_markers, orientation, 
#                                    marker_height=10, between_markers=70):
#     if orientation == "blank_left":
#         border, other_border = 0.9, 2.1
#     elif orientation == "blank_right":
#         border, other_border = 2.1, 0.9
#     elif orientation == "blank_bottom":
#         border, other_border = 9.3, 2.4
#     elif orientation == "blank_top":
#         border, other_border = 2.4, 9.3
#     else:
#         print("Error: Orientation Not Supported")
#         return None
    
#     border, other_border = 0, 0

#     markers = []
    
#     if num_markers >= 1:
#         bottom_marker = [border, border + marker_height/2, border + marker_height]
        
#         markers += bottom_marker

#     if num_markers >= 2:
#         middle_marker_offset = border + marker_height + other_border + between_markers
#         middle_marker = [x + middle_marker_offset for x in bottom_marker]
        
#         markers += middle_marker

#     if num_markers >= 3:
#         top_marker_offset = middle_marker_offset * 2
#         top_marker = [x + top_marker_offset for x in bottom_marker]
        
#         markers += top_marker
    
#     distances = [x + distance_from_ground for x in markers]

#     print(distances)

#     return distances


# def predict_height(input_image, approach, real_world_distances, 
#                    num_markers, VERBOSE=True):
#     if input_image is None:
#         print("Error: Image not found or unable to open.")
#         return None
#     else:
#         image = input_image.copy()
        
#         # Step 1: Detect ArUco markers and their center pixel positions
#         marker_centers, marker_ids = detect_aruco_markers(image)
    
#         if len(marker_centers) < 3:
#             print("Error: Less than 3 ArUco markers detected.")
#             return None
#         else:
#             # Sort the markers based on y-coordinate (assuming markers are placed vertically)
#             marker_centers.sort(key=lambda x: x[1], reverse=True)
#             marker_centers = marker_centers[:num_markers*3]
    
#             # Extract the y-coordinates (pixel positions) of the detected marker centers
#             pixel_positions = [center[1] for center in marker_centers]
#             # pixel_positions.reverse()
    
#             # Step 3: Fit a polynomial between the pixel positions and real-world distances
#             degree = 5
#             coefficients = fit_polynomial(pixel_positions, real_world_distances, degree)
    
#             # Step 4: Detect the top pixel point of the person
#             if approach == "yolo":
#                 image, top_pixel_point, bottom_pixel_point = detect_person_top_point_vYOLO(image, yolo_model)
#             elif approach == "mediapipe":
#                 image, top_pixel_point, bottom_pixel_point = detect_person_top_point_vMP_v1(image)
#             else:
#                 print("Error: Approach Not Supported")
#                 return None
                
#             if VERBOSE:
#                 print("Marker Pixel Positions", pixel_positions)
#                 print("Real_world_distances: ", real_world_distances)
#                 print("Polynomial Coefficients", coefficients)
#                 print("Person Top Pixel Point:", top_pixel_point)
#                 print("Person Bottom Pixel Point:", bottom_pixel_point)
    
#             if (top_pixel_point is not None) and (bottom_pixel_point is not None):
#                 # Extract the y-coordinate of the top point (pixel position)
#                 top_pixel_y = top_pixel_point[1]

#                 print("TOP Pixel Y", top_pixel_y)
#                 print("Bottom Pixel Y", bottom_pixel_point)
    
#                 # Convert top pixel y-coordinate to real-world distance
#                 real_distance = pixel_to_real_distance(top_pixel_y, coefficients)

#                 print("Real Distance Y", real_distance)
                
#                 # Calculate the angle
#                 dx = bottom_pixel_point[0] - top_pixel_point[0]  # Change in x
#                 dy = bottom_pixel_point[1] - top_pixel_point[1]  # Change in y

#                 # Calculate the angle in degrees
#                 angle = np.degrees(np.arctan2(dy, dx))

#                 # Optionally, visualize the result (draw detected person's top pixel point and marker centers)
#                 cv2.circle(image, top_pixel_point, 5, (0, 255, 0), -1)  # Draw top point of person
#                 cv2.circle(image, bottom_pixel_point, 5, (0, 255, 0), -1)
                
#                 cv2.arrowedLine(image, top_pixel_point, bottom_pixel_point, (0, 0, 255), thickness=2, tipLength=0.05)  # Forward arrow
#                 cv2.arrowedLine(image, bottom_pixel_point, top_pixel_point, (0, 0, 255), thickness=2, tipLength=0.05)  # Backward arrow

#                 text_position = ((top_pixel_point[0] + bottom_pixel_point[0]) // 2, (top_pixel_point[1] + bottom_pixel_point[1]) // 2)

#                 # Add the length text
#                 cv2.putText(image, "Height: {:.1f} cm".format(real_distance), 
#                             text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, lineType=cv2.LINE_AA)

#                 # Draw Marker Centers
#                 for (center_x, center_y) in marker_centers:
#                     cv2.circle(image, (int(center_x), int(center_y)), 5, (255, 0, 0), -1)  # Draw marker centers

#                 return image, top_pixel_y, real_distance, angle
#             else:
#                 return None, None, None


# def process_single_image(input_image_path, input_image_frame, output_image_dir, output_filename, 
#                          num_markers, marker_distance_from_ground, marker_orientation, distance_between_markers, 
#                          approach="mediapipe", VERBOSE=False, SAVE_PROCESSED_IMAGE=False):
    
#     if input_image_frame is not None:
#         image = input_image_frame.copy()
#     elif input_image_path is not None:
#         image_path = input_image_path
#         image = cv2.imread(image_path)
#     else:
#         print("ERROR: Neither Image nor image path provided.")
#         return None, None, None
    
#     real_world_distances = calculate_real_world_distances(marker_distance_from_ground, 
#                                                           num_markers=num_markers,
#                                                           orientation = marker_orientation, 
#                                                           between_markers=distance_between_markers)
    
#     processed_image, top_pixel, pred_height, angle = predict_height(image, 
#                                                                     approach=approach, 
#                                                                     real_world_distances=real_world_distances, 
#                                                                     num_markers=num_markers)
    
#     if SAVE_PROCESSED_IMAGE:
#         image_output_dir = validate_path("{}/{}".format(output_image_dir, approach))
#         cv2.imwrite("{}/{}.jpg".format(image_output_dir, output_filename), processed_image)                
    
#     if VERBOSE:
#         print("The real-world distance for the top point of the person is approximately {:.2f} cm.".format(pred_height))
    
#     return processed_image, top_pixel, pred_height, angle
    

# def process_single_video(input_video_path,
#                          num_markers=3, 
#                          marker_distance_from_ground=20.3, marker_orientation="blank_left", distance_between_markers=90, 
#                          approach="mediapipe", VERBOSE=False, SAVE_INTERMEDIATE_RESULTS=False):
#     """
#     Processes a single video for height estimation.

#     Parameters:
#     ----------
#     input_video_path : str
#         Path to the input video file to be processed.
        
#     num_markers : int, optional
#         Number of markers to be used in the processing. Default is 3.
        
#     marker_distance_from_ground : float, optional
#         Distance from the ground to the bottom marker page boundary in cms. Default is 20.3 cm.
        
#     marker_orientation : str, optional
#         Orientation of marker. Possible values are "blank_left", "blank_right", "blank_bottom", "blank_top"
#         depending on where the larger blank of the A4 page is placed.
#         Default is "blank_left".
        
#     distance_between_markers : float, optional
#         Distance between markers page boundaries in cms. Default is 90 cm.
        
#     approach : str, optional
#         Method used for processing. Options might include "mediapipe" or "yolo". Default is "mediapipe".
        
#     VERBOSE : bool, optional
#         If True, enables detailed logging of the processing steps. Default is False.
    
#     SAVE_INTERMEDIATE_RESULTS : bool, optional
#         If True, enables storage of input video and output video frames. Default is False.

#     Returns:
#     -------
#     output_video_filepath : str
#         Path of the Processed video with height and other markings
    
#     predicted_height : float
#         Estimated value of person's height for the video
        
#     """
#     print("inside the file")
#     # Get Video Filename from Video Path
#     input_filename = str(input_video_path).split("/")[-1].split(".")[0]
    
#     print("Processing {} ...".format(input_filename))
    
#     # Open the video file
#     cap = cv2.VideoCapture(input_video_path)

#     # Check if the video opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open video.")
#         return None, None, None

#     frame_number = 0
    
#     processed_frames_list = []
#     top_pixel_list = []
#     height_list = []
#     max_height_frame = None
#     max_height = 0

#     while True:
#         # Read a frame from the video
#         ret, frame = cap.read()
        
#         # Break the loop if there are no more frames
#         if not ret:
#             break
        
#         output_image_dir = None
#         frame_name_string = "frame_{}".format(frame_number)

#         if SAVE_INTERMEDIATE_RESULTS:
#             frames_output_dir = validate_path("{}/{}".format(FRAMES_OUTPUT_BASE_DIR, input_filename))
#             frame_filename = "{}/frame_{}.jpg".format(frames_output_dir, frame_number)
#             cv2.imwrite(frame_filename, frame)
            
#             output_image_dir = validate_path("{}/{}".format(PROCESSED_FRAMES_OUTPUT_BASE_DIR, input_filename))
        
#         processed_image, pred_top_pixel, pred_height, angle = process_single_image(input_image_path=None, 
#                                                                                    input_image_frame=frame,
#                                                                                    output_image_dir=output_image_dir, 
#                                                                                    output_filename=frame_name_string,
#                                                                                    num_markers=num_markers,
#                                                                                    marker_distance_from_ground=marker_distance_from_ground, 
#                                                                                    marker_orientation=marker_orientation, 
#                                                                                    distance_between_markers=distance_between_markers, 
#                                                                                    approach=approach,
#                                                                                    VERBOSE=VERBOSE, 
#                                                                                    SAVE_PROCESSED_IMAGE=SAVE_INTERMEDIATE_RESULTS)
        
#         processed_frames_list.append(processed_image)        
#         top_pixel_list.append(pred_top_pixel)
#         height_list.append(pred_height)
        
#         if (89.25 <= angle <= 90.75) and (pred_height > max_height):
#             max_height = pred_height
#             max_height_frame = frame_name_string
        
#         if VERBOSE:
#             print("Frame: {} Angle: {:.2f}".format(frame_name_string, angle))

#         frame_number += 1
    
#     # Release the video capture object and close all windows
#     cap.release()
    
#     final_pred_height = max_height
#     pred_height_frame = max_height_frame

#     # Stich a Video from O/P dir
#     output_video_dir = validate_path("{}/{}".format(PROCESSED_VIDEO_PATH, approach))
#     output_video_filepath="{}/{}.avi".format(output_video_dir, input_filename)
        
#     height, width, _ = processed_frames_list[0].shape
    
#     video = cv2.VideoWriter(output_video_filepath, cv2.VideoWriter_fourcc(*'MJPG'), 30, (width,height))

#     for frame in processed_frames_list:
#         video.write(frame)

#     video.release()
    
#     return output_video_filepath, final_pred_height, pred_height_frame
