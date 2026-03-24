import os
import google.generativeai as genai

# Setup Gemini API Key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    # Try reading from .env file
    try:
        with open('/home/admin/.openclaw/workspace/.env', 'r') as f:
            for line in f:
                if 'GEMINI_API_KEY' in line:
                    api_key = line.split("'")[1]
                    break
    except:
        pass

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment or .env file.")

genai.configure(api_key=api_key)

def transcribe_audio(audio_file_path):
    """Transcribes audio using Gemini 1.5 Flash."""
    try:
        print(f"Uploading audio file: {audio_file_path}")
        sample_file = genai.upload_file(path=audio_file_path)
        
        print(f"Transcribing audio...")
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([
            "Please provide a highly accurate transcription of this audio file. "
            "Identify the key topics covered and provide a brief summary of the main points.",
            sample_file
        ])
        
        return response.text
    except Exception as e:
        return f"Error during transcription: {e}"

if __name__ == "__main__":
    # Prototype: Assume audio is in data/transcripts/example.mp3
    audio_file = "data/transcripts/example.mp3"
    
    if os.path.exists(audio_file):
        transcription = transcribe_audio(audio_file)
        
        # Save transcription to a text file for now
        output_file = "data/transcripts/example_transcript.txt"
        with open(output_file, "w") as f:
            f.write(transcription)
        print(f"Transcription saved to: {output_file}")
    else:
        print(f"Please place an audio file at {audio_file} for testing.")
