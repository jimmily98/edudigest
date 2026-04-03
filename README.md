<h1 align="center">EduDigest </h1>

<p align="center">
  <strong>An automated, AI-powered course summarization and study guide generation pipeline.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg" alt="Flask">
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-orange.svg" alt="Gemini">
  <img src="https://img.shields.io/badge/Media-FFmpeg-green.svg" alt="FFmpeg">
  <img src="https://img.shields.io/badge/Deployment-Alibaba%20Cloud-ff6a00.svg" alt="Alibaba Cloud">
</p>

---

## Overview
**EduDigest** is a full-stack media processing and NLP tool designed to automatically extract knowledge from raw educational materials (like lecture videos or recordings). It converts hours of multimedia content into searchable transcripts and interactive, highly condensed PDF study guides.

By leveraging **FFmpeg** for media extraction and **Google Gemini** (via APIs) for transcription and summarization, EduDigest eliminates the manual effort of note-taking for dense online courses.

## Key Features
*   **Multi-Format Processing Pipeline:** Accepts diverse inputs including `MP4`, `MP3`, `PDF`, `TXT`, `DOCX`, `CSV`, and `HTML`.
*   **Automated Audio Extraction:** Utilizes `FFmpeg` to strip and compress audio tracks from heavy video lecture files.
*   **AI Speech-to-Text (ASR):** Integrates with Google Gemini APIs for high-accuracy audio transcription.
*   **Document Synthesis:** Automatically formats the processed text and generates clean, structured PDF study guides.
*   **Cloud-Native Deployment:** Fully dockerized and configured for deployment on **Alibaba Cloud ECS** (Linux) and Render, managed via `systemd`.
*   **NotebookLM Integration:** Hooks into NotebookLM for advanced document querying and semantic interaction.

---

## System Architecture
1. **Frontend:** A clean web interface built with HTML/CSS to handle large file uploads and display processing progress.
2. **Backend (Flask):** Handles secure file routing, task queuing, and API orchestration.
3. **Extraction Engine (`audio_extractor.py`):** Spawns local FFmpeg subprocesses to parse media files.
4. **AI Pipeline (`transcriber.py` & `pdf_generator.py`):** Sends payload to Gemini, receives the transcription, and compiles it into a downloadable PDF format.

---

## Tech Stack
*   **Backend:** Python, Flask, Werkzeug
*   **Media Processing:** FFmpeg
*   **AI/LLM:** Google Gemini API, NotebookLM Client
*   **Infrastructure:** Docker, Alibaba Cloud (Alinux3), Gunicorn

---

## Installation & Local Setup

### 1. Prerequisites
Ensure you have the following installed on your system:
*   Python 3.9+
*   [FFmpeg](https://ffmpeg.org/download.html) (Must be added to system PATH)

### 2. Clone and Setup
```bash
git clone https://github.com/jimmily98/edudigest.git
cd edudigest

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
python -m src.backend.app
```
The web interface will now be accessible at `http://localhost:5000`.

---

## Deployment (Alibaba Cloud / Render)
EduDigest is production-ready. 
*   **Docker:** A complete `Dockerfile` is included. Simply build and run the container mapping port `5000`.
*   **Render:** A `render.yaml` configuration is included for seamless CI/CD deployment on Render.com. Be sure to mount a persistent disk at `/app/data` to preserve generated transcripts across redeploys.
