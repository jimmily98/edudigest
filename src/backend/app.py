import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from src.utils.audio_extractor import extract_audio
from src.utils.transcriber import transcribe_audio
from src.utils.pdf_generator import create_pdf

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'data/uploads'
TRANSCRIPT_FOLDER = 'data/transcripts'
ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'pdf', 'txt', 'doc', 'docx', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRANSCRIPT_FOLDER'] = TRANSCRIPT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>EduDigest - Course Summarizer</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="container mt-5">
        <h1>Welcome to EduDigest!</h1>
        <p>Upload your course materials (Video, Audio, Text) for automatic summarization.</p>
        
        <form action="/upload" method="post" enctype="multipart/form-data" class="mb-4">
            <div class="mb-3">
                <label for="file" class="form-label">Course Material:</label>
                <input type="file" name="file" class="form-control" required>
            </div>
            
            <div class="mb-3">
                <label for="action" class="form-label">Desired Action (via NotebookLM):</label>
                <select name="action" class="form-select">
                    <option value="gist">Get the Gist (Executive Summary)</option>
                    <option value="faq">Generate FAQ & Answers</option>
                    <option value="study_guide">Create Study Guide</option>
                    <option value="briefing">Briefing Document</option>
                </select>
            </div>
            
            <button type="submit" class="btn btn-primary">Upload and Process</button>
        </form>
    </body>
    </html>
    """

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    action = request.form.get('action', 'gist')
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        # Determine file type and process
        if filename.endswith('.mp4'):
            audio_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], filename.replace('.mp4', '.mp3'))
            extract_audio(upload_path, audio_path)
            transcript = transcribe_audio(audio_path)
            
            # Save PDF version
            pdf_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], filename.replace('.mp4', '.pdf'))
            create_pdf(transcript, pdf_path, title=f"Transcript: {filename}")
            
            # NOTE: At this point, the file is ready to be sent to NotebookLM
            # The client's upload_source method would be called here.
            
            return f"""
            <div class='container mt-5'>
                <h1>Processing Complete!</h1>
                <p><strong>Action Selected:</strong> {action.upper()}</p>
                <p><strong>Transcript saved to:</strong> {pdf_path}</p>
                <div class='card p-4 mt-3'>
                    <h5>NotebookLM Analysis (Gist/Summary):</h5>
                    <p>{transcript}</p>
                </div>
                <a href='/' class='btn btn-secondary mt-3'>Back to Upload</a>
            </div>
            """
        
        return "File uploaded successfully. Processing for other types coming soon!"
    
    return "Invalid file type."

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
