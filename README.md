# EduDigest 📖

EduDigest is an automated course summarization tool designed to help users grasp the essence of online courses without watching lengthy videos.

## Features

- **Multi-Format Upload:** Supports video (MP4), audio, and text (PDF, DOC, TXT, HTML, CSV).
- **Audio Extraction:** Automatically extracts audio from video files.
- **Speech-to-Text (ASR):** Converts course audio into searchable text.
- **Transcript Generation:** Stores processed text into PDF format for easy consumption.
- **NotebookLM Integration:** Leverages the NotebookLM API for advanced analysis and interaction.

## Deployment on Render

This project is configured for deployment on **Render.com** using Docker.

1.  **Fork/Clone** the repository to your GitHub account.
2.  **Create a New Web Service** on Render and select this repository.
3.  **Docker Support:** Render will automatically detect the `Dockerfile`.
4.  **Environment Variables:** Add your `GEMINI_API_KEY` in the Render dashboard.
5.  **Disk (Optional):** Add a persistent disk if you want to save processed files across redeploys (mount at `/app/data`).

---

## Roadmap

- [ ] Initial project structure
- [ ] Backend for file uploads (Node.js/Python)
- [ ] Video/Audio processing pipeline (FFmpeg + ASR)
- [ ] PDF generation for transcripts
- [ ] Integration with NotebookLM API
- [ ] User-friendly Web Interface
