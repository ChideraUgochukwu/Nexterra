from flask import Flask, request, jsonify
import openai
import PyPDF2

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Call GPT-4 to summarize the text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    summary = response['choices'][0]['message']['content']
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)