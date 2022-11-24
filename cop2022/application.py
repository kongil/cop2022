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

import cv2
import math

import numpy as np # linear algebra
from PIL import Image
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

app = Flask(__name__)

# 이미지 경로
app.config['IMG_FOLDER'] = os.path.join('static', 'images')	# 이미지 파일의 경로
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'upload')	# 이미지 파일의 업로드 경로
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'PNG' 'jpg', 'JPG', 'jpeg', 'gif', 'tiff', 'raw', 'bmp'])


def get_pad_width(im, new_shape, is_rgb=True):
    pad_diff = new_shape - im.shape[0], new_shape - im.shape[1]
    t, b = math.floor(pad_diff[0]/2), math.ceil(pad_diff[0]/2)
    l, r = math.floor(pad_diff[1]/2), math.ceil(pad_diff[1]/2)
    if is_rgb:
        pad_width = ((t,b), (l,r), (0, 0))
    else:
        pad_width = ((t,b), (l,r))
    return pad_width

def pad_and_resize_cv(image_path, dataset, desired_size=224):
    img = cv2.imread(f'../input/{dataset}/{image_path}')
    
    pad_width = get_pad_width(img, max(img.shape))
    padded = np.pad(img, pad_width=pad_width, mode='constant', constant_values=0)
    
    resized = cv2.resize(padded, (desired_size,)*2).astype('uint8')
    
    return resized

def pad_and_resize_pil(image_path, dataset, desired_size=224):
    '''Experimental'''
    im = Image.open(f'../input/{dataset}/{image_path}')
    
    # old_size = im.size
    # ratio = float(desired_size)/max(old_size)
    # new_size = tuple([int(x*ratio) for x in old_size])
    # resized = im.resize(new_size)
    # im_array = np.asarray(resized)
    
    # pad_width = get_pad_width(im_array, desired_size)
    # padded = np.pad(im_array, pad_width=pad_width, mode='constant', constant_values=0)
    
    return padded


def pad_and_resize(image_path, dataset, desired_size=224, mode='cv'):
    if mode =='pil':
        return pad_and_resize_pil(image_path, dataset, desired_size)
    else:
        return pad_and_resize_cv(image_path, dataset, desired_size)
    
def make_image_to_nparray(image_path, filename):
    ab_path = image_path+"/"+filename
    print(ab_path)
    img = cv2.imread(f'./{image_path}/{filename}')
    print(f'./{image_path}/{filename}')
    pad_width = get_pad_width(img,max(img.shape))
    padded = np.pad(img, pad_width=pad_width, mode='constant', constant_values=0)
    resized = cv2.resize(padded, (224,224))
    print(resized.shape)
    return resized


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
    print(file)
    filename = secure_filename(file.filename)
    print(filename)
    print("end")

    file.save(os.path.join(app.config['UPLOAD_FOLDER'] , filename))

    return jsonify({
                "status": "success",
                "filename": filename,
                "benign" : "1",
                "malignant" : "1",
                "normal" : "1"
                }), 200
"""
    image_path = app.config['UPLOAD_FOLDER']
    print("filename : " + image_path + "/" + filename)
    image_array = make_image_to_nparray(image_path, filename)
    
    print("image_array : ", image_array.shape)
    
    new_image_array = np.array([image_array / 255 * 1.])
    print(new_image_array)
    print(new_image_array.shape)
    model = load_model('./my_model.h5')
    
    result = model.predict(new_image_array)
    print(result)
    #result = 0
    return jsonify({
        			"status": "success",
         			"filename": filename,
       				"benign" : str(round(result[0][0] * 100, 2)),
        	        "malignant" : str(round(result[0][1] * 100, 2)),
                    "normal" : str(round(result[0][2] * 100, 2))
    				}), 200
"""

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=int(sys.argv[1]))

        
