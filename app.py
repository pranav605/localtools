import os
import pythoncom
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from docx2pdf import convert
import subprocess
from PIL import Image
app = Flask(__name__)

# Create upload and output folders
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# ---------------- DOCX TO PDF ----------------
def safe_convert(input_path, output_path):
    """Convert DOCX to PDF safely (with COM initialization)."""
    pythoncom.CoInitialize()
    try:
        convert(input_path, output_path)
    finally:
        pythoncom.CoUninitialize()

# ---------------- PDF COMPRESS ----------------
GS_PATH = r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe"  # actual path must be updated accordingly

def compress_pdf_file(input_path, output_path):
    """Compress a PDF using Ghostscript on Windows."""
    try:
        subprocess.run([
            GS_PATH,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/prepress",  # /screen = low-res, /ebook = medium, /prepress = high
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            input_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ghostscript compression failed: {e}")


# ---------------- ROUTES ----------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_doc():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and file.filename.lower().endswith('.docx'):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_filename = os.path.splitext(filename)[0] + '.pdf'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        safe_convert(input_path, output_path)

        return send_file(output_path, as_attachment=True)

    return "Please upload a .docx file"


@app.route('/compress', methods=['POST'])
def compress_pdf():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_filename = os.path.splitext(filename)[0] + '_compressed.pdf'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        compress_pdf_file(input_path, output_path)

        return send_file(output_path, as_attachment=True)

    return "Please upload a PDF file"

@app.route("/convert-image", methods=['POST'])
def convert_image_to_webp():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']

    if file.filename == '':
        return "No selected file"
    
    if file and file.filename.lower().endswith(('.jpeg', '.jpg', '.png')):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        #open image with pillow
        with Image.open(input_path) as img:
            output_filename = os.path.splitext(filename)[0]+'.webp'
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            img.save(output_path, 'webp')

        return send_file(output_path, as_attachment=True)

    return "Please upload a JPEG, JPG, or PNG file"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
