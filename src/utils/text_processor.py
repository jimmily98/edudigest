import os
import PyPDF2
from docx import Document
import csv

def read_text_file(file_path):
    """Extracts text from various file formats."""
    ext = file_path.rsplit('.', 1)[1].lower()
    text = ""
    
    try:
        if ext == 'pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        
        elif ext == 'docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        
        elif ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        
        elif ext == 'csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    text += " ".join(row) + "\n"
        
        elif ext == 'html':
            from bs4 import BeautifulSoup
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                text = soup.get_text()
                
        return text.strip()
    except Exception as e:
        print(f"Error reading {ext} file: {e}")
        return ""

if __name__ == "__main__":
    # Test with a dummy file if needed
    pass
