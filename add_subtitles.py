import os
import subprocess

def add_subtitles_to_video(video_path, srt_path, output_path):
    """
    Adds subtitles from an SRT file to a video file using ffmpeg.
    
    Args:
    video_path (str): Path to the video file.
    srt_path (str): Path to the SRT subtitle file.
    output_path (str): Path to save the output video file with subtitles.
    """
    try:
        # Command to embed subtitles into the video
        command = [
            'ffmpeg',
            '-i', video_path,        # Input video file
            '-vf', f"subtitles='{srt_path}'",  # Path to subtitle file
            '-c:v', 'libx264',       # Video codec to use
            '-c:a', 'copy',          # Copy the audio without re-encoding
            '-crf', '22',            # Constant rate factor (quality of video)
            '-preset', 'fast',       # Encoding speed and compression rate tradeoff
            output_path              # Output file path
        ]

        # Run the command with subprocess
        subprocess.run(command, check=True)
        print(f"Subtitles have been added successfully to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add subtitles: {e}")


