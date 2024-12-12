import logging
import subprocess
from flask import Flask, request, jsonify
import re
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.image as mpimg
from pathlib import Path
from flask_cors import CORS
import requests
import torch
import base64
import gunicorn
import pathlib
import sys


def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

app = Flask(__name__)
# CORS(app, resources={r"/get-detection": {"origins": "http://localhost:5173"}})
CORS(app, resources={
    r"/get-detection": {"origins": ["http://localhost:5173", "https://regex-fkgrid-ash28.netlify.app"]},
    r"/get-product": {"origins": ["http://localhost:5173", "https://regex-fkgrid-ash28.netlify.app"]}
})

@app.route("/")
def hello():
    with open("m.png", "rb") as image_file:
            base64_encoded_data = base64.b64encode(image_file.read())
            base64_string = base64_encoded_data.decode('utf-8')
            # print(base64_string)
            # url = "http://localhost:5000/get-detection"
            url = "http://localhost:5000/get-product"
            # url = "http://192.168.1.36:5000/get-detection"
            payload = {"img": base64_string}
            response = requests.post(url, json=payload)
            # print(response.json())
    return response.json()

@app.route("/get-detection", methods=["POST"])
def get_fruits():
    data = request.get_json()
    image_data = base64.b64decode(data.get('img'))
    img = "base64.jpg"
    with open(img, "wb") as image_file:
        image_file.write(image_data)
    cmd = [
        "python", 'detect.py',
        '--weights', 'best_veg_latest.pt',
        '--img', '640',
        '--conf', '0.1',
        '--source', img,
        '--save-conf'
    ]
    result_data = subprocess.run(cmd, capture_output=True, text=True)
    print("result : ",result_data)
    output = result_data.stdout+result_data.stderr
    lines = output.splitlines()
    logging.info("lines : ",lines)
    results_saved_info = ''+lines[-1].split(" ",4)[-1].split("\\",3)[-1].strip()
    
    parts = lines[-3].split(":", 2)
    detection_info = parts[2].strip() + ""
    clean_dir = remove_ansi_escape_sequences(results_saved_info)
    image_path = Path("runs/detect") / clean_dir / img
    with open(image_path, "rb") as image_file:
            base64_encoded_data = base64.b64encode(image_file.read())
            base64_string = base64_encoded_data.decode('utf-8')
    user_data = {
    "deteted_image": base64_string,
    "result" : detection_info
    }

    return jsonify(user_data), 200

@app.route("/get-product", methods=["POST"])
def get_product():
    data = request.get_json()
    image_data = base64.b64decode(data.get('img'))
    img = "base64.jpg"
    with open(img, "wb") as image_file:
        image_file.write(image_data)
    cmd = [
        "python", 'detect.py',
        '--weights', 'brand.pt',
        '--img', '640',
        '--conf', '0.1',
        '--source', img,
        '--save-conf'
    ]
    result_data = subprocess.run(cmd, capture_output=True, text=True)
    print("result : ",result_data)
    output = result_data.stdout+result_data.stderr
    lines = output.splitlines()
    logging.info("lines : ",lines)
    results_saved_info = ''+lines[-1].split(" ",4)[-1].split("\\",3)[-1].strip()
    
    parts = lines[-3].split(":", 2)
    detection_info = parts[2].strip() + ""
    clean_dir = remove_ansi_escape_sequences(results_saved_info)
    image_path = Path("runs/detect") / clean_dir / img
    with open(image_path, "rb") as image_file:
            base64_encoded_data = base64.b64encode(image_file.read())
            base64_string = base64_encoded_data.decode('utf-8')
    user_data = {
    "deteted_image": base64_string,
    "result" : detection_info
    }

    return jsonify(user_data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
