import streamlit as st
import cv2
import numpy as np
from graph_cut_segmentation import graph_cut_withoutGB
import tempfile
import os

st.title('Grain Boundary Detection')
st.write("Performs performs grain boundary detection using graph cut segmentation with morphological operations.")

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

# Add number inputs for morphological operations
erosion_iterations = st.number_input('Number of Erosion Iterations', min_value=1, max_value=10, value=1, 
                                   help="Controls how many times erosion is applied. Higher values create stronger erosion effect.")
dilation_iterations = st.number_input('Number of Dilation Iterations', min_value=1, max_value=10, value=1,
                                    help="Controls how many times dilation is applied. Higher values create stronger dilation effect.")

if uploaded_file is not None:
    st.write("Processing image...")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_path = tmp_file.name

    # Process image with custom iterations
    result = graph_cut_withoutGB(temp_path, erosion_iter=erosion_iterations, dilation_iter=dilation_iterations)
    
    # Display images one after the other
    st.subheader("Original Image")
    st.image(uploaded_file, width=800)
    st.write("Original input image before processing")
    
    st.subheader("Segmented Image with Morphological Operations without Gaussian Blur")
    st.image(result, width=800)
    st.write("Processed image with grain boundaries detected")
    
    # with col1:
    #     st.subheader("Original Image")
    #     st.image(uploaded_file, width=600)
    #     st.write("Original input image before processing")
    
    # with col2:
    #     st.subheader("Segmented Image")
    #     # st.image(result)
    #     # image size increase
    #     st.image(result, width=600)
    #     st.write("Processed image with grain boundaries detected")
    
    st.write("Current Settings:")
    st.write(f"- Erosion Iterations: {erosion_iterations}")
    st.write(f"- Dilation Iterations: {dilation_iterations}")
    
    # Convert result to bytes for download
    is_success, buffer = cv2.imencode(".png", result)
    if is_success:
        btn = st.download_button(
            label="Download Segmented Image",
            data=buffer.tobytes(),
            file_name="segmented_image.png",
            mime="image/png"
        )
    
    # Cleanup temp file
    os.unlink(temp_path)
else:
    st.write("Please upload an image to begin processing.")
