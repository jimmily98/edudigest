import os
import google.generativeai as genai

# Setup Gemini API Key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    try:
        with open('/home/admin/.openclaw/workspace/.env', 'r') as f:
            for line in f:
                if 'GEMINI_API_KEY' in line:
                    api_key = line.split("'")[1]
                    break
    except:
        pass

if not api_key:
    # Try a common location or fall back to a placeholder
    api_key = os.getenv('GEMINI_API_KEY')

if api_key:
    genai.configure(api_key=api_key)

def transcribe_audio(audio_file_path):
    """Transcribes audio using Gemini 1.5 Flash."""
    try:
        print(f"Uploading audio file: {audio_file_path}")
        sample_file = genai.upload_file(path=audio_file_path)
        
        print(f"Transcribing audio...")
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
        
        # We check for the file state before proceeding
        import time
        while sample_file.state.name == "PROCESSING":
            time.sleep(2)
            sample_file = genai.get_file(sample_file.name)

        if sample_file.state.name == "FAILED":
            raise ValueError(f"Audio file processing failed on Gemini side: {sample_file.name}")

        response = model.generate_content([
            "Please provide a highly accurate transcription of this audio file. "
            "Identify the key topics covered and provide a brief summary of the main points.",
            sample_file
        ])
        
        return response.text
    except Exception as e:
        print(f"Transcriber Error: {e}")
        return f"Error during transcription: {e}"
