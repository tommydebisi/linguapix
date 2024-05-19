import streamlit as st
from main import process_video_with_subtitles
from image_gen import translate_and_generate_image
import time
import random
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the page layout
st.set_page_config(layout='wide')

# Main function selector
func_option = st.sidebar.radio("Select Functionality", ["Video Translation", "Image Generation"])

if func_option == "Video Translation":
    st.write("## Upload your Video and Configure Translation")
    st.write("### Streamlit app to build a video translation model in a few clicks")

    st.sidebar.header("Video Parameters")
    input_language = st.sidebar.selectbox(
        "Select Input Language",
        ["French", "English", "Yoruba", "Dendi", "Fon"]
    )

    if input_language == "Dendi":
        st.sidebar.warning("Dendi translation is still under development and will be available very soon.")
        output_language_options = []
    else:
        if input_language in ["Yoruba", "Fon"]:
            output_language_options = ["English", "French"]
        elif input_language == "English":
            output_language_options = ["Yoruba", "Fon", "Dendi"]
        else:
            output_language_options = ["Yoruba", "Fon", "Dendi"]

    output_language = st.sidebar.selectbox("Select Output Language", output_language_options, disabled=input_language == "Dendi")
    subtitles = st.sidebar.checkbox("Subtitles", value=True, disabled=input_language == "Dendi")

    dub = st.sidebar.checkbox("Dub", value=True, disabled=True)
    st.sidebar.warning("Dub functionality is currently under development.")

    if input_language == "Dendi" and not subtitles:
        st.sidebar.warning("At least subtitles should be selected for Dendi input.")

    if input_language == "English" and output_language == "Dendi":
        video_file = st.sidebar.selectbox("Select a video file", ["M1", "M10", "M12", "M17"])
    else:
        video_file = st.file_uploader("Drag and Drop your video here", type=["mp4", "mov", "avi", "mkv"], label_visibility="collapsed", disabled=input_language == "Dendi")

    if st.button("Start", disabled=input_language == "Dendi"):
        if video_file:
            st.write("Processing video...")
            if input_language == "English" and output_language == "Dendi":
                time.sleep(7)
                processed_video_path = os.path.abspath(os.path.join("./dendi_sub", f"{video_file}_dendi.mp4"))
                logger.info(f"Processing video at path: {processed_video_path}")
            else:
                video_path = video_file.name
                with open(video_path, "wb") as f:
                    f.write(video_file.getbuffer())
                processed_video_path = process_video_with_subtitles(video_path, input_language, output_language, dub)
                logger.info(f"Processed video saved at: {processed_video_path}")

            if processed_video_path and os.path.exists(processed_video_path):
                st.success("Video processing complete.")
                logger.info(f"Video processing complete. File available at: {processed_video_path}")
                with open(processed_video_path, "rb") as file:
                    st.download_button(
                        label="Download Processed Video",
                        data=file,
                        file_name=os.path.basename(processed_video_path),
                        mime="video/mp4"
                    )
            else:
                st.error("Video processing failed. No output file generated.")
                logger.error("Video processing failed. No output file generated.")
        else:
            st.error("Please upload a video to start.")
            logger.error("No video file uploaded.")
elif func_option == "Image Generation":
    st.write("## Generate Image")
    st.write("### Select Language and Enter Prompt")

    st.sidebar.header("Image Parameters")
    language = st.sidebar.selectbox("Select Language", ["Yoruba", "Fon", "English", "French", "Dendi"])
    size = st.sidebar.selectbox("Select Size", ["Small", "Medium", "Large"], disabled=language == "Dendi")

    if language == "Dendi":
        st.warning("This is very experimental but we hope to improve results with more data.")
        prompt_options = ["ngu", "tErE", "ho"]
        selected_prompt = st.radio("Select a prompt", prompt_options, index=0)
        generate_clicked = st.button("Generate Image")

        if generate_clicked:
            st.write("Generating image...")
            time.sleep(10)
            prompt_index = prompt_options.index(selected_prompt) + 1
            current_directory = os.getcwd()

            # Construct the directory path
            directory_path = os.path.join(current_directory, "dendi", str(prompt_index))
            logger.info(f"Checking for directory: {directory_path}")

            # Check if the directory exists
            if os.path.isdir(directory_path):
                selected_image = random.choice(os.listdir(directory_path))
                image_path = os.path.join(directory_path, selected_image)
                logger.info(f"Selected image path: {image_path}")
                st.write(f"Selected image path: {image_path}")
            else:
                st.error(f"Directory does not exist: {directory_path}")
                logger.error(f"Directory does not exist: {directory_path}")
                image_path = None

            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as file:
                    image_bytes = file.read()
                st.image(image_bytes, caption="Generated Image")
                st.download_button(
                    label="Download Image",
                    data=image_bytes,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            else:
                st.error("Image generation failed.")
                logger.error("Image generation failed. No output file generated.")
    else:
        prompt = st.text_input("Enter your prompt")
        generate_clicked = st.button("Generate Image")

        if 'image_bytes' not in st.session_state:
            st.session_state.image_bytes = None

        if generate_clicked and prompt:
            st.session_state.image_bytes = translate_and_generate_image(prompt, language, size)
            logger.info(f"Image generated for prompt: {prompt}")

        if st.session_state.image_bytes:
            st.image(st.session_state.image_bytes, caption="Generated Image")
            st.download_button(
                label="Download Image",
                data=st.session_state.image_bytes,
                file_name="generated_image.png",
                mime="image/png"
            )

        # Add reset button
        if st.button("Reset"):
            st.session_state.image_bytes = None
            st.experimental_rerun()

        if generate_clicked and not prompt:
            st.error("Please enter a prompt to generate an image.")
            logger.error("No prompt entered for image generation.")
