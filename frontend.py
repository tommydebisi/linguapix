import streamlit as st
from PIL import Image
from main import process_video_with_subtitles

# Load logo image
logo_path = 'logo.webp'  # Adjust this to your local path
logo = Image.open(logo_path)

# Set the page layout
st.set_page_config(layout='wide')

# Sidebar for parameters
with st.sidebar:
    st.image(logo, use_column_width=True)

    st.header("Parameters")

    # Input Language Options
    input_language = st.selectbox(
        "Select Input Language",
        ["French", "English", "Yoruba", "Dendi", "Fon"]
    )

    # Determine the output language options based on the selected input language
    if input_language in ["Yoruba", "Fon"]:
        output_language_options = ["English", "French"]
    elif input_language == "Dendi":
        output_language_options = ["English"]
    else:
        output_language_options = ["Yoruba", "Fon", "Dendi"]

    output_language = st.selectbox(
        "Select Output Language",
        output_language_options
    )

    # Logic for disabling/enabling Dub based on language selections
    disable_dub = (input_language in ["Fon", "Dendi"]) or \
                  (input_language == "French" and output_language in ["Fon", "Dendi"]) or \
                  (input_language == "English" and output_language in ["Fon", "Dendi"])

    subtitles = st.checkbox("Subtitles", value=True)
    dub = st.checkbox("Dub", value=True, disabled=disable_dub)

    if disable_dub:
        st.warning("Dub is not available for the selected input/output language combination.")

    # If Dendi is selected as input and both subtitles/dub are unchecked, show a warning
    if input_language == "Dendi" and not subtitles:
        st.warning("At least subtitles should be selected for Dendi input.")

# Main content
st.write("## Upload your Video and Configure Translation")
st.write("### Streamlit app to build a video translation model in a few clicks")

col1, col2 = st.columns([1, 3])

# Upload/Drag and Drop box
with col1:
    st.write("### Parameters")
    st.write(f"**Input Language:** {input_language}")
    st.write(f"**Output Language:** {output_language}")
    st.write(f"**Subtitles:** {'Enabled' if subtitles else 'Disabled'}")
    st.write(f"**Dub:** {'Enabled' if dub else 'Disabled'}")

with col2:
    st.write("### Upload your Video")
    video_file = st.file_uploader(
        "Drag and Drop your video here",
        type=["mp4", "mov", "avi", "mkv"],
        label_visibility="collapsed"
    )

# Start button
if st.button("Start"):
    if video_file:
        st.write("Processing video...")
        process_video_with_subtitles(video_file, input_language, output_language, dub)
    else:
        st.error("Please upload a video to start.")
