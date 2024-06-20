from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os 
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'
#max file size allowed = 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    #check if there is a extension, and if there is, is it a csv file
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

def save_secure_file(file):
    random_filename = secure_filename(f"{uuid.uuid4()}.csv")
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], random_filename))
    return random_filename

@app.route('/upload', methods = ['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No File Part'}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invali File Type'}), 400
    filename = save_secure_file(file)
    return jsonify({'message': 'File Uploaded Successfully', 'filename': filename}), 200

@app.route("/")
def hello():
    return "Hello World!!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"),debug=True)