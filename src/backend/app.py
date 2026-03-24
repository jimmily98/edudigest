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
                <input type="file" name="file" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Upload and Process</button>
        </form>
    </body>
    </html>
    """

@app.route('/upload', method=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
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
            
            return f"<h1>Processing Complete!</h1><p>Transcript saved to: {pdf_path}</p><p>{transcript}</p>"
        
        return "File uploaded successfully. Processing for other types coming soon!"
    
    return "Invalid file type."

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
