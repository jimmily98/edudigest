import os
import requests
import time

def test_upload():
    # 1. Create a dummy test PDF
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a test document for EduDigest v1.0.", ln=1, align='C')
    pdf.cell(200, 10, txt="It contains information about Artificial Intelligence and Machine Learning.", ln=2, align='L')
    test_file = "data/uploads/test_upload.pdf"
    pdf.output(test_file)
    print(f"Created test file: {test_file}")

    # 2. Try to POST to the local running server (via localhost:5000)
    # Note: The server must be running
    url = "http://127.0.0.1:5000/upload"
    files = [('files', ('test_upload.pdf', open(test_file, 'rb'), 'application/pdf'))]
    data = {
        'notebook_name': 'Test Integration',
        'action': 'gist'
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, files=files, data=data, timeout=60)
        if response.status_code == 200:
            print("SUCCESS: Server returned 200 OK")
            if "Unified Analysis" in response.text:
                print("SUCCESS: Analysis found in response")
                return True
            else:
                print("FAILURE: Analysis header not found in response")
        else:
            print(f"FAILURE: Server returned status code {response.status_code}")
            print(f"Response snippet: {response.text[:500]}")
    except Exception as e:
        print(f"ERROR: Could not connect to server: {e}")
    
    return False

if __name__ == "__main__":
    test_upload()
