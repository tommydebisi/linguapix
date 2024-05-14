from transformers import pipeline
import datetime
import os

def format_time(seconds):
    """ Convert seconds to the SRT time format """
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def create_srt(data):
    """ Create SRT content from transcription data, adjusting for timestamp resets """
    srt_content = []
    last_end_time = 0  # Track the end time of the last chunk
    
    for idx, chunk in enumerate(data['chunks'], start=1):
        # Adjust start and end times based on the last end time if they appear to reset
        start_time = chunk['timestamp'][0]
        end_time = chunk['timestamp'][1]

        if start_time < last_end_time:
            # Assume the chunk is meant to follow directly after the last one
            start_time = last_end_time
            end_time = start_time + (chunk['timestamp'][1] - chunk['timestamp'][0])

        # Format timestamps for SRT
        formatted_start_time = format_time(start_time)
        formatted_end_time = format_time(end_time)
        
        # Update the last end time to the current chunk's end time
        last_end_time = end_time

        text = chunk['text'].strip()
        srt_content.append(f"{idx}\n{formatted_start_time} --> {formatted_end_time}\n{text}\n")
    
    return "\n".join(srt_content)

def transcribe_and_create_srt(audio_file_path):
    """ 
    Transcribe audio and create an SRT file specifically for Fon language audio inputs.
    This function should be called when the input language of the application is set to 'Yoruba', 'English', or 'French'.
    
    Args:
    audio_file_path (str): The file path to the audio file to be transcribed.
    """
    # Initialize the ASR pipeline
    pipe = pipeline("automatic-speech-recognition", model="neoform-ai/whisper-medium-yoruba")
    
    # Ensure audio file exists
    if not os.path.exists(audio_file_path):
        print("Error: Audio file does not exist.")
        return

    # Perform transcription
    transcription = pipe(audio_file_path, return_timestamps=True)
    
    # Convert the transcription to SRT format
    srt_output = create_srt(transcription)
    
    # Determine SRT file name based on the audio file path
    srt_file_path = os.path.splitext(audio_file_path)[0] + ".srt"
    
    # Save the SRT content to a file
    with open(srt_file_path, 'w') as file:
        file.write(srt_output)
        print(f"SRT file created: {srt_file_path}")


def create_srt_fon(data, merge_threshold=1.0):
    """
    Create SRT content from transcription data, merging close subtitles. This function is specifically
    designed to handle word-to-word timestamps provided in the transcription data for more accurate
    subtitle synchronization.
    
    Args:
        data (dict): Transcription data containing chunks with timestamps and text.
        merge_threshold (float): Maximum time gap (in seconds) between chunks to merge them into a single subtitle.
    
    Returns:
        str: The complete SRT content as a single string.
    """
    srt_content = []
    current_text = []
    current_start = None
    current_end = None
    idx = 1

    for chunk in data['chunks']:
        start_time = chunk['timestamp'][0]
        end_time = chunk['timestamp'][1]
        text = chunk['text'].strip()

        if current_start is None:
            # Initialize the first segment
            current_start = start_time
            current_end = end_time
            current_text.append(text)
        else:
            if start_time - current_end <= merge_threshold:
                # Extend the current subtitle
                current_end = end_time
                current_text.append(text)
            else:
                # Write the current subtitle and start a new one
                srt_content.append(f"{idx}\n{format_time(current_start)} --> {format_time(current_end)}\n{' '.join(current_text)}\n")
                idx += 1
                current_start = start_time
                current_end = end_time
                current_text = [text]

    # Add the last subtitle entry
    if current_text:
        srt_content.append(f"{idx}\n{format_time(current_start)} --> {format_time(current_end)}\n{' '.join(current_text)}\n")
    
    return "\n".join(srt_content)

def transcribe_and_create_srt_fon(audio_file_path):
    """
    Transcribe audio and create an SRT file specifically for Fon language audio inputs.
    This function should be called when the input language of the application is set to 'Fon'.
    
    Args:
    audio_file_path (str): The file path to the audio file to be transcribed.
    """
    # Initialize the ASR pipeline
    pipe = pipeline("automatic-speech-recognition", model="chrisjay/fonxlsr")
    
    # Ensure audio file exists
    if not os.path.exists(audio_file_path):
        print("Error: Audio file does not exist.")
        return

    # Perform transcription with word timestamps
    transcription = pipe(audio_file_path, return_timestamps='word')
    
    # Convert the transcription to SRT format with merged subtitles
    srt_output = create_srt(transcription)
    
    # Determine SRT file name based on the audio file path
    srt_file_path = os.path.splitext(audio_file_path)[0] + ".srt"
    
    # Save the SRT content to a file
    with open(srt_file_path, 'w') as file:
        file.write(srt_output)
        print(f"SRT file created: {srt_file_path}")



