import requests
from fpdf import FPDF
import time
import sys
import os

def run_test():
    # 1. Generate PDF
    # Use standard FPDF (v1.7.x style) compatible arguments
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Using positional arguments for cross-version compatibility
    pdf.cell(200, 10, "This is a test document for EduDigest.", 0, 1, 'C')
    pdf.cell(200, 10, "AI is transforming education.", 0, 1, 'L')
    
    test_dir = "/home/admin/edudigest/data/uploads"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        
    test_file = os.path.join(test_dir, "test_random.pdf")
    pdf.output(test_file)
    print(f"Generated test PDF at {test_file}")

    # 2. Test Loop
    url = "http://127.0.0.1:5000/upload"
    success = False
    for i in range(3):
        print(f"Attempt {i+1}...")
        try:
            with open(test_file, 'rb') as f:
                files = [('files', ('test_random.pdf', f, 'application/pdf'))]
                data = {'notebook_name': 'Random Test', 'action': 'gist'}
                resp = requests.post(url, files=files, data=data, timeout=120)
                if resp.status_code == 200 and "Unified Analysis" in resp.text:
                    print("Success! Got 200 OK and analysis text.")
                    success = True
                    break
                else:
                    print(f"Failed. Status code: {resp.status_code}")
                    print(resp.text[:500])
        except Exception as e:
            print(f"Exception: {e}")
        time.sleep(2)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    run_test()
