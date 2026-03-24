import os
from fpdf import FPDF

def create_pdf(transcript_text, output_pdf_path, title="Course Transcript"):
    """Converts transcript text into a formatted PDF."""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Add Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, title, ln=True, align='C')
        pdf.ln(10)
        
        # Add Content
        pdf.set_font("Arial", size=12)
        # Multi-cell handles line wrapping
        pdf.multi_cell(0, 10, transcript_text)
        
        pdf.output(output_pdf_path)
        print(f"PDF created successfully: {output_pdf_path}")
    except Exception as e:
        print(f"Error during PDF creation: {e}")

if __name__ == "__main__":
    # Prototype: Assume text is in data/transcripts/example_transcript.txt
    text_file = "data/transcripts/example_transcript.txt"
    pdf_file = "data/transcripts/example_transcript.pdf"
    
    if os.path.exists(text_file):
        with open(text_file, "r") as f:
            content = f.read()
        create_pdf(content, pdf_file)
    else:
        # Create a dummy for testing
        dummy_content = "This is a sample transcript for testing the PDF generator.\nKey points:\n1. Introduction to the course.\n2. Deep dive into topics."
        create_pdf(dummy_content, pdf_file)
