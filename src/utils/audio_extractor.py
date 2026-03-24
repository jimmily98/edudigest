import os
import subprocess

def extract_audio(video_path, output_audio_path):
    """Extracts audio from video using FFmpeg."""
    try:
        command = [
            'ffmpeg', '-i', video_path,
            '-q:a', '0', '-map', 'a',
            output_audio_path, '-y'
        ]
        subprocess.run(command, check=True)
        print(f"Audio extracted successfully: {output_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio extraction: {e}")

if __name__ == "__main__":
    # Prototype: Assume video is in data/uploads/example.mp4
    video_file = "data/uploads/example.mp4"
    audio_file = "data/transcripts/example.mp3"
    
    if os.path.exists(video_file):
        extract_audio(video_file, audio_file)
    else:
        print(f"Please place a video file at {video_file} for testing.")
