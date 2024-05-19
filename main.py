from translation import translate_srt
from transcription import transcribe_and_create_srt, transcribe_and_create_srt_fon
from add_subtitles import add_subtitles_to_video
import subprocess
import time


import uuid
import os

def process_video_with_subtitles(video_path, input_lang, output_lang, dub=False):
    """
    Process a video by transcribing, translating subtitles, and optionally dubbing the video.
    
    Args:
    video_path (str): Path to the video file.
    input_lang (str): Language code of the video's spoken language.
    output_lang (str): Language code for the translated subtitles.
    dub (bool): If True, the video will be dubbed in the output language.
    """
    unique_id = uuid.uuid4().hex
    video_path = os.path.abspath(video_path)
    # Transcribe the video and create an SRT file
    audio_file_path = video_path.replace('.mp4', '.wav')  # Convert video file path to audio file path
    srt_path = video_path.replace('.mp4', '.srt')
    
    # Convert mp4 to wav using ffmpeg
    try:
        subprocess.run(['ffmpeg', '-i', video_path, '-acodec', 'pcm_s16le', '-ar', '16000', audio_file_path], check=True)
        print(f"Audio extracted to WAV format at {audio_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract audio: {e}")
        return
    # wait 5 seconds
    time.sleep(5)
    language_map = {'Yoruba': 'yo', 'English': 'en', 'French': 'fr', 'Fon': 'fon', 'Spanish': 'es'}
    if input_lang in language_map:
        try:
            if input_lang == 'Fon':
                print("Transcribing and creating SRT for Fon language...")
                transcribe_and_create_srt_fon(audio_file_path)
                print("Transcription and SRT creation for Fon language completed.")
            else:
                print("Transcribing and creating SRT... with file path: ", audio_file_path)
                transcribe_and_create_srt(audio_file_path)
                print("Transcription and SRT creation completed.")
        except Exception as e:
            print(f"Failed to transcribe and create SRT: {e}")
            return
    else:
        print(f"Transcription for the language {input_lang} is not supported.")
        return
    
    # Translate the SRT file
    try:
        translated_srt_path = srt_path.replace('.srt', f'_{output_lang}.srt')
        print("Translating SRT file...")
        translate_srt(srt_path, language_map[input_lang], language_map[output_lang], translated_srt_path)
        print("Translation completed.")
    except Exception as e:
        print(f"Failed to translate SRT file: {e}")
        return
    
    # Add subtitles to video
    try:
        subtitled_video_path = video_path.replace('.mp4', f'_subtitled_{output_lang}_{unique_id}.mp4')
        add_subtitles_to_video(video_path, translated_srt_path, subtitled_video_path)
    except Exception as e:
        print(f"Failed to add subtitles to video: {e}")
        return
    
    if dub:
        # Dubbing functionality can be added here if required in the future
        print("Dubbing feature is not implemented yet.")
    
    print(f"Processed video with subtitles is available at {subtitled_video_path}")

    # Clean up intermediate files
    os.remove(audio_file_path)
    os.remove(srt_path)
    os.remove(translated_srt_path)

    return subtitled_video_path
# Example Usage:
# process_video_with_subtitles("test.mp4", "English", "Yoruba", dub=False)

