import os
from fpdf import FPDF

def create_pdf(transcript_text, output_pdf_path, title="Course Transcript"):
    """Converts transcript text into a formatted PDF with Unicode support."""
    try:
        # Use FPDF2 which supports Unicode more naturally
        pdf = FPDF()
        
        # Define font path
        font_path = "/home/admin/edudigest/src/backend/static/fonts/NotoSansSC-Regular.ttf"
        
        if os.path.exists(font_path):
            pdf.add_font("NotoSans", style="", fname=font_path)
            pdf.set_font("NotoSans", size=12)
        else:
            # Fallback to standard font if download failed
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
        
        pdf.add_page()
        
        # Add Title
        pdf.set_font(size=16)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(10)
        
        # Add Content
        pdf.set_font(size=12)
        pdf.multi_cell(0, 10, transcript_text)
        
        pdf.output(output_pdf_path)
        print(f"PDF created successfully: {output_pdf_path}")
        return True
    except Exception as e:
        print(f"Error during PDF creation: {e}")
        return False

if __name__ == "__main__":
    pass
