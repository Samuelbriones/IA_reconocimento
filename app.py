from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2
import base64
import numpy as np
from model.predict_face import predict_face_shape

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

FACE_TYPES = [
    {"type": "Ovalado", "recommendation": "Lentes cuadrados para equilibrar las proporciones."},
    {"type": "Redondo", "recommendation": "Lentes angulares para afilar los rasgos."},
    {"type": "Cuadrado", "recommendation": "Lentes redondeados o tipo aviador para suavizar."},
    {"type": "Oblongo", "recommendation": "Lentes altas para acortar visualmente el rostro."},
    {"type": "Corazón", "recommendation": "Lentes sin montura o redondos para balancear la frente amplia."},
]

@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    shape=None
    recommendation = None
    pred = None

    if request.method == "POST":
        img_np = None

        if "image" in request.files and request.files["image"].filename != "":
            image = request.files["image"]
            file_bytes = np.frombuffer(image.read(), np.uint8)
            img_np = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        elif "captured_image" in request.form and request.form["captured_image"] != "":
            data_url = request.form["captured_image"]
            _, encoded = data_url.split(",", 1)
            img_bytes = base64.b64decode(encoded)
            file_bytes = np.frombuffer(img_bytes, np.uint8)
            img_np = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img_np is not None:
            img, shape, pred  = predict_face_shape(img_np)
            
            if shape is None:
                shape = "No se detectó un rostro válido"
                recommendation = "Por favor, sube una imagen clara con solo una persona."

            success, buffer = cv2.imencode(".jpg", img)
            if success:
                image_data = base64.b64encode(buffer.tobytes()).decode("utf-8")

            for item in FACE_TYPES:
                if item["type"]== shape:
                    recommendation = item["recommendation"]
                    break

    return render_template("index.html",
                           image_data=image_data,
                           face_type=shape,
                           recommendation=recommendation,
                           pred=round(pred, 2) if pred else 0
                           )

if __name__ == "__main__":
    app.run(debug=True)
