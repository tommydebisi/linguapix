import subprocess
import time
import uuid
import os
import logging

from add_subtitles import add_subtitles_to_video
from transcription import transcribe_and_create_srt, transcribe_and_create_srt_fon
from translation import translate_srt

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def process_video_with_subtitles(video_path, input_lang, output_lang, dub=False):
    try:
        logging.info("Starting process_video_with_subtitles")
        
        unique_id = uuid.uuid4().hex
        video_path = os.path.abspath(video_path)
        audio_file_path = video_path.replace('.mp4', '.wav')
        srt_path = video_path.replace('.mp4', '.srt')

        # Convert mp4 to wav using ffmpeg
        try:
            logging.info(f"Extracting audio from {video_path}")
            subprocess.run(['ffmpeg', '-i', video_path, '-acodec', 'pcm_s16le', '-ar', '16000', audio_file_path], check=True)
            logging.info(f"Audio extracted to WAV format at {audio_file_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to extract audio: {e}")
            return None
        
        time.sleep(5)

        language_map = {'Yoruba': 'yo', 'English': 'en', 'French': 'fr', 'Fon': 'fon', 'Spanish': 'es'}
        if input_lang in language_map:
            try:
                if input_lang == 'Fon':
                    logging.info("Transcribing and creating SRT for Fon language...")
                    transcribe_and_create_srt_fon(audio_file_path)
                    logging.info("Transcription and SRT creation for Fon language completed.")
                else:
                    logging.info(f"Transcribing and creating SRT... with file path: {audio_file_path}")
                    transcribe_and_create_srt(audio_file_path)
                    logging.info("Transcription and SRT creation completed.")
            except Exception as e:
                logging.error(f"Failed to transcribe and create SRT: {e}")
                return None
        else:
            logging.error(f"Transcription for the language {input_lang} is not supported.")
            return None

        # Translate the SRT file
        try:
            translated_srt_path = srt_path.replace('.srt', f'_{output_lang}.srt')
            logging.info("Translating SRT file...")
            translate_srt(srt_path, language_map[input_lang], language_map[output_lang], translated_srt_path)
            logging.info("Translation completed.")
        except Exception as e:
            logging.error(f"Failed to translate SRT file: {e}")
            return None

        # Add subtitles to video
        try:
            subtitled_video_path = video_path.replace('.mp4', f'_subtitled_{output_lang}_{unique_id}.mp4')
            logging.info(f"Adding subtitles to video, saving to {subtitled_video_path}")
            add_subtitles_to_video(video_path, translated_srt_path, subtitled_video_path)
            logging.info("Subtitles added to video.")
        except Exception as e:
            logging.error(f"Failed to add subtitles to video: {e}")
            return None

        if dub:
            logging.info("Dubbing feature is not implemented yet.")

        logging.info(f"Processed video with subtitles is available at {subtitled_video_path}")

        # Clean up intermediate files
        os.remove(audio_file_path)
        os.remove(srt_path)
        os.remove(translated_srt_path)

        return subtitled_video_path
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
