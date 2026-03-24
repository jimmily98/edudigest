import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

# Import our utilities
from src.utils.audio_extractor import extract_audio
from src.utils.transcriber import transcribe_audio
from src.utils.pdf_generator import create_pdf
from src.utils.notebooklm_client import NotebookLMClient
from src.utils.text_processor import read_text_file

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
    if 'files' not in request.files:
        flash('No files provided')
        return redirect(request.url)
    
    files = request.files.getlist('files')
    notebook_name = request.form.get('notebook_name', 'Untitled Course')
    action = request.form.get('action', 'gist')
    
    if not files or all(f.filename == '' for f in files):
        flash('No selected files')
        return redirect(request.url)
    
    processed_contents = []
    file_metadata = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            
            content_snippet = ""
            ext = filename.rsplit('.', 1)[1].lower()
            
            # 1. Handle Multimedia (Video/Audio)
            if ext in {'mp4', 'mp3'}:
                if ext == 'mp4':
                    audio_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], filename.replace('.mp4', '.mp3'))
                    extract_audio(upload_path, audio_path)
                    content_snippet = transcribe_audio(audio_path)
                else:
                    content_snippet = transcribe_audio(upload_path)
            
            # 2. Handle Documents
            elif ext in {'pdf', 'docx', 'txt', 'csv', 'html'}:
                content_snippet = read_text_file(upload_path)
            
            processed_contents.append(f"--- SOURCE: {filename} ---\n{content_snippet}")
            file_metadata.append(filename)
    
    # Combined analysis using Gemini
    all_content = "\n\n".join(processed_contents)
    import google.generativeai as genai
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    prompt = f"""
    The following is a collection of materials for the course "{notebook_name}". 
    The user wants to: {action.upper()}.
    
    Please analyze ALL the sources provided below collectively. 
    Synthesize the information into a unified response. 
    If there are conflicting points between sources, please note them.
    
    MATERIALS:
    {all_content[:60000]} # Limit for Flash model token safety
    """
    
    response = model.generate_content(prompt)
    analysis_text = response.text
    
    # Save unified PDF
    pdf_filename = f"{secure_filename(notebook_name)}_unified_summary.pdf"
    pdf_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], pdf_filename)
    create_pdf(analysis_text, pdf_path, title=f"Unified Analysis: {notebook_name}")

    return render_template('result.html', 
                           notebook_name=notebook_name, 
                           filename=", ".join(file_metadata), 
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
