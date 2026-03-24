import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

# Import our utilities
from src.utils.audio_extractor import extract_audio
from src.utils.transcriber import transcribe_audio
from src.utils.pdf_generator import create_pdf
from src.utils.notebooklm_client import NotebookLMClient

app = Flask(__name__)
app.secret_key = "supersecretkey_edudigest_2026"

UPLOAD_FOLDER = 'data/uploads'
TRANSCRIPT_FOLDER = 'data/transcripts'
ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'pdf', 'txt', 'docx', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRANSCRIPT_FOLDER'] = TRANSCRIPT_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    notebook_name = request.form.get('notebook_name', 'Untitled Course')
    action = request.form.get('action', 'gist')
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        analysis_text = ""
        pdf_filename = ""
        
        # Determine file type and process
        if filename.endswith('.mp4'):
            # 1. Extract audio
            audio_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], filename.replace('.mp4', '.mp3'))
            extract_audio(upload_path, audio_path)
            
            # 2. Transcribe & Summarize via Gemini
            analysis_text = transcribe_audio(audio_path)
            
            # 3. Save PDF version
            pdf_filename = filename.replace('.mp4', '.pdf')
            pdf_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], pdf_filename)
            create_pdf(analysis_text, pdf_path, title=f"Analysis: {notebook_name}")
            
        elif filename.endswith('.mp3'):
            analysis_text = transcribe_audio(upload_path)
            pdf_filename = filename.replace('.mp3', '.pdf')
            pdf_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], pdf_filename)
            create_pdf(analysis_text, pdf_path, title=f"Analysis: {notebook_name}")
            
        else:
            # For other text formats, handle appropriately (Coming soon)
            analysis_text = "File uploaded successfully. Intelligent text analysis for documents is coming in the next update!"
            pdf_filename = filename + ".pdf" # Placeholder

        return render_template('result.html', 
                               notebook_name=notebook_name, 
                               filename=filename, 
                               action=action.capitalize(), 
                               analysis=analysis_text,
                               pdf_url=url_for('download_file', filename=pdf_filename))
    
    flash("Invalid file type.")
    return redirect(request.url)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['TRANSCRIPT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
