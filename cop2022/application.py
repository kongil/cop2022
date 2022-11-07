from flask import Flask, request, redirect, flash, url_for, jsonify, Response
from flask import render_template

import sys

import os
from werkzeug.utils import secure_filename
from PIL import Image

import datetime
import traceback


import tensorflow as tf
from keras.models import load_model


app = Flask(__name__)

# 이미지 경로
app.config['IMG_FOLDER'] = os.path.join('static', 'images')	# 이미지 파일의 경로
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'upload')	# 이미지 파일의 업로드 경로
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'PNG' 'jpg', 'JPG', 'jpeg', 'gif', 'tiff', 'raw', 'bmp'])


@app.route('/ref/camera', methods=['POST'])
def camera():
    return render_template('/ref/camera.html')

#카메라 실행
@app.route('/', methods=['POST','GET'])
def camera2():
    print("camear2 start")
    return render_template('/ref/camera2.html')

#이미지 업로드
@app.route('/upload/image', methods=['GET', 'POST'])
def upload_image():
    print("upload_image start")
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    print("filename" + filename)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'] , filename))

    image_path = app.config['UPLOAD_FOLDER']

    model = load_model('./my_model.h5')
    model.predict()
    #result = 0
    return jsonify({
        			"status": "success",
         			"filename": filename,
   #     			"result" : result,
    				}), 200

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=int(sys.argv[1]))
