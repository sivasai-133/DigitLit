import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import matplotlib.pyplot as plt
import os
import numpy as np

# Define a function to validate the input value
def validate_input(value):
    if value is not None:
        value = int(value)
        if value < 10 or value > 19:
            st.error("Please enter a value between 10 and 19.")
            return None
    return value

def draw_images():
    # Specify canvas parameters in application
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("freedraw", "line", "circle")
    )

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == 'point':
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(0,0,0,0)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color="#000",
        background_color= '#fff',
        update_streamlit=True,
        height=150,
        width = 150,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        key="canvas",
    )

    if not os.path.exists(cur+'/dataset/'):
        os.makedirs( cur+ '/dataset/')


    # Add an input field to the Streamlit app
    value = None
    value = st.text_input("Enter a value between 10 and 19:","1", key="input_field")

    # Validate the input value
    validated_value = validate_input(value)

    # Do something interesting with the validated value
    if validated_value is not None :
        st.write("The validated value is:", validated_value)

    if (canvas_result.image_data is not None):
        # Save the image to a file
        st.image(canvas_result.image_data)
        image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        grayscale_image = image.convert('L')
        path = cur+ '/dataset/' + str(validated_value) + '/'
        if not os.path.exists(path) and validated_value is not None:
            os.makedirs(path)

         # Add a "Save Image" button that is only enabled when the user has completed the drawing
        if st.button("Save Image") and validated_value is not None:
                grayscale_image.save(path+f'Img_{validated_value}_{len(os.listdir(path))}.png')
                st.success("Image saved successfully.")
        else:
            st.warning("Please draw something on the canvas before saving.")

    else:
        st.warning("Please draw something on the canvas before saving.")


def display_images():
    # Add an input field to the Streamlit app
    value = None
    value = st.text_input("Enter a value between 10 and 19:","1", key="input_field")

    # Validate the input value
    validated_value = validate_input(value)

    if validated_value is not None:
        path = cur+'/dataset/' + str(validated_value) + '/'
        if os.path.exists(path) and len(os.listdir(path)) > 0:
            image_filenames = os.listdir(path)
            random_image_filename = np.random.choice(image_filenames)
            image = Image.open(os.path.join(path, random_image_filename))
            st.image(image, caption=f"Randomly selected image for value {validated_value}", use_column_width=True,width = 300)
        else:
            st.warning(f"No images found for value {validated_value}.")

# Add pages to the Streamlit app
menu = ['Display Images','Draw Images']
choice = st.sidebar.selectbox('Select an option',menu)

if choice == 'Draw Images':
    draw_images()
else:
    display_images()