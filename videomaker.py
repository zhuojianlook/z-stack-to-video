import streamlit as st
import cv2
import numpy as np
import tempfile

def images_to_video(image_files, fps):
    img_array = []
    frame_size = None

    for uploaded_file in image_files:
        # Read the file as bytes, then convert it to an image
        bytes_data = uploaded_file.read()
        nparr = np.frombuffer(bytes_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            continue

        # Set frame size based on first image
        if frame_size is None:
            frame_size = (img.shape[1], img.shape[0])

        img = cv2.resize(img, frame_size)
        img_array.append(img)

    # Temporary file to store video
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        # Create a video writer object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_file.name, fourcc, fps, frame_size)

        for img in img_array:
            out.write(img)

        out.release()
        return temp_file.name

# Streamlit interface
st.title("z-stack to Video Converter")

# File uploader
uploaded_files = st.file_uploader("Choose Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
fps = st.number_input("Frames per second (FPS)", min_value=1, value=30)

if st.button("Convert Images to Video"):
    if uploaded_files:
        try:
            video_path = images_to_video(uploaded_files, fps)
            st.success("Video created successfully!")
            with open(video_path, "rb") as file:
                st.download_button(label='Download Video', data=file, file_name='output_video.mp4', mime='video/mp4')
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("No files uploaded. Please upload some image files.")
