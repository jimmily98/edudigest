# EduDigest Design Mockups

This directory contains visual designs and mockups for the EduDigest user interface.

## Current Mockups

1.  **Dashboard (`mockups/dashboard.html`)**
    - A modern, dashboard-style interface featuring:
        - Sidebar navigation (My Notebooks, Analytics, Settings).
        - Multi-file drag-and-drop upload area.
        - Analysis type selection (Executive Summary, FAQ, Study Guide, Briefing).
        - Recent analysis history with status tracking (Completed, Processing).
        - Direct links to Transcripts and NotebookLM.

## Design Philosophy

- **User-Centric:** Simple workflows for uploading and analyzing.
- **Modern & Clean:** Using Indigo and Slate color palettes for a professional feel.
- **Responsive:** Optimized for both desktop and mobile views.
- **Visual Feedback:** Clear status indicators for background processing (ASR, AI generation).

## Technology Stack (Proposed)

- **Frontend:** Tailwind CSS, Font Awesome, JavaScript (Alpine.js or React/Vue for more complex interactions).
- **Backend:** Flask (Python) or FastAPI.
- **Communication:** WebSockets (for real-time progress updates during video processing).
