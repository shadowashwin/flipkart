import subprocess
from flask import Flask, request, jsonify
import re
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.image as mpimg
from pathlib import Path
import torch
import base64
import gunicorn
import sys


def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

app = Flask(__name__)
@app.route("/")
def hello():
    return "user_data"

@app.route("/get-detection")
def get_user():
    
    img = "fresh_banana.jpg"
    cmd = [
        sys.executable, 'detect.py',
        '--weights', './best_veg.pt',
        '--img', '640',
        '--conf', '0.1',
        '--source', img
    ]
    result_data = subprocess.run(cmd, capture_output=True, text=True)
    
    output = result_data.stderr
    lines = output.splitlines()
    print("lines : ",lines)
    results_saved_info = ''+lines[-1].split(" ",4)[-1].split("\\",3)[-1].strip()
    
    parts = lines[-3].split(":", 2)
    detection_info = parts[2].strip() + ""
    
    print(detection_info)
    clean_dir = remove_ansi_escape_sequences(results_saved_info)
    image_path = Path("runs/detect") / clean_dir / img
    print(image_path)
    with open(image_path, "rb") as image_file:
            base64_encoded_data = base64.b64encode(image_file.read())
            base64_string = base64_encoded_data.decode('utf-8')
            print(base64_string)
    user_data = {
    "deteted_image": base64_string,
    "result" : detection_info
    }

    return jsonify(user_data), 200

if __name__ == "__main__":
    app.run()
