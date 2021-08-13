
import os
#import urllib.request
#from app import app
from flask import Flask, request, redirect, jsonify, render_template
from flask_autoindex import AutoIndex
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path


UPLOAD_FOLDER = './uploads'


app = Flask(__name__)

CORS(app, resources={
     r"/*": {"origins": ['http://localhost:5000', r' ^ https://.+example.com$']}})

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


#ppath = "./uploads"  # update your own parent directory here

AutoIndex(app, browse_root=UPLOAD_FOLDER)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/file-upload/<new_folder>', methods=['POST'])
def upload_file(new_folder):
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message': 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message': 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		new_path = Path(app.config['UPLOAD_FOLDER']+"/" +
		                new_folder).mkdir(parents=True, exist_ok=True)
		print(new_path)
		file.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+new_folder, filename))
		resp = jsonify({'message': 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(
			{'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
