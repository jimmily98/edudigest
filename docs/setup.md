# EduDigest 📖 - Setup & Requirements

## Prerequisites

- **Python 3.8+**
- **FFmpeg** (installed and in your PATH)
- **Google Generative AI SDK** (`pip install google-generativeai`)
- **Flask** (`pip install flask`)

## Getting Started

1.  Clone the repository:
    ```bash
    git clone https://github.com/jimmily98/edudigest.git
    cd edudigest
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set your Gemini API Key:
    ```bash
    export GEMINI_API_KEY='your-api-key-here'
    ```
4.  Run the application:
    ```bash
    python src/backend/app.py
    ```

## Project Progress

- [x] Directory structure and README
- [x] Audio extraction from video (FFmpeg)
- [x] Transcription using Gemini 1.5 Flash
- [x] Basic Flask backend for file uploads
- [ ] PDF generation for transcripts
- [ ] Integration with NotebookLM API
- [ ] Advanced text processing (DOC, CSV, etc.)
