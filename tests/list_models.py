import os
import google.generativeai as genai

# Setup Gemini API Key
api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyA_YuAJ_Ot8G6Pa0Qg8MXfZmesy7tv8rTg')
genai.configure(api_key=api_key)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
