from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from pdf2image import convert_from_path
import os
import uuid

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save uploaded PDF
    pdf_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    file.save(pdf_path)

    # Convert PDF to JPG
    pages = convert_from_path(pdf_path)
    jpg_files = []
    for i, page in enumerate(pages):
        jpg_filename = f"{pdf_filename}_{i}.jpg"
        jpg_path = os.path.join(PROCESSED_FOLDER, jpg_filename)
        page.save(jpg_path, 'JPEG')
        jpg_files.append(jpg_filename)

    return jsonify({'files': jpg_files})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
