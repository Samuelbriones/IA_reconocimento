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
    {"type": "Oblongo", "recommendation": "Lentes altos para acortar visualmente el rostro."},
    {"type": "Corazón", "recommendation": "Lentes sin montura o redondos para balancear la frente amplia."},
]

LENTES_IMAGES = {
    "Ovalado": [
        {"url":"/static/lentes/Ovalado/1.jpg","nombre": "Lentes Rectangulares Clásicos"},
        {"url":"/static/lentes/Ovalado/2.jpg", "nombre": "Lentes Wayfarer Tradicional"},
        {"url":"/static/lentes/Ovalado/3.jpg", "nombre": "Lentes John Lennon style"},
        {"url":"/static/lentes/Ovalado/4.jpg", "nombre": "Lentes Hexagonales suaves"},
        {"url":"/static/lentes/Ovalado/5.jpg", "nombre": "Lentes Aviador Clásico"},
        {"url":"/static/lentes/Ovalado/6.jpg", "nombre": "Lentes Clubmaster"},
    ],
    "Redondo": [
        {"url":"/static/lentes/Redondo/1.jpg","nombre": "Lentes Rectangulares clásicos"},
        {"url":"/static/lentes/Redondo/2.jpg", "nombre": "Lentes Cuadrados Angulosos"},
        {"url":"/static/lentes/Redondo/3.jpg", "nombre": "Lentes Browline marcado"},
        {"url":"/static/lentes/Redondo/4.jpg", "nombre": "Lentes Hexagonales"},
        {"url":"/static/lentes/Redondo/5.jpg", "nombre": "Lentes Montura semi-rimless"},
        {"url":"/static/lentes/Redondo/6.jpg", "nombre": "Lentes Aviador Clásico"},
    ],
    "Cuadrado": [
        {"url":"/static/lentes/Cuadrado/1.jpg","nombre": "Lentes Rendodos"},
        {"url":"/static/lentes/Cuadrado/2.jpg","nombre": "Lentes Cuadrados "},
        {"url":"/static/lentes/Cuadrado/3.jpg","nombre": "Lentes de sol tipo aviador"},
        {"url":"/static/lentes/Cuadrado/4.jpg","nombre": "Lentes de pasta gruesa"},
        {"url":"/static/lentes/Cuadrado/5.jpg","nombre": "Lentes tipo browline"},
        {"url":"/static/lentes/Cuadrado/6.jpg","nombre": "Lentes ligeramente ovaladas"},
    ],
    "Oblongo": [
        {"url":"/static/lentes/Oblongo/1.jpg","nombre": "Lentes Rectangular Oversize "},
        {"url":"/static/lentes/Oblongo/2.jpg","nombre": "Lentes Wayfarer Ancho"},
        {"url":"/static/lentes/Oblongo/3.jpg","nombre": "Lentes Modelo Oval"},
        {"url":"/static/lentes/Oblongo/4.jpg","nombre": "Lentes Clubmaster Moderno"},
        {"url":"/static/lentes/Oblongo/5.jpg","nombre": "Lentes Geométrica Moderna"},
        {"url":"/static/lentes/Oblongo/6.jpg","nombre": "Lentes Forma Ligeramente"}
    ],
    "Corazón": [
        {"urls":"/static/lentes/Corazon/1.jpg","nombre": "Lentes Oftalmicos"},
        {"urls":"/static/lentes/Corazon/2.jpg","nombre": "Lentes Rectangulares Redondeados Bajos"},
        {"urls":"/static/lentes/Corazon/3.jpg","nombre": "Lentes Aviador Oversize (suave)"},
        {"urls":"/static/lentes/Corazon/4.jpg","nombre": "Lentes Modelo Ovalado Ligero"},
        {"urls":"/static/lentes/Corazon/5.jpg","nombre": "Lentes Semi-rimless invertidos"},
        {"urls":"/static/lentes/Corazon/6.jpg","nombre": "Lentes Aviador Invertido"},
    ],
}

@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    shape=None
    recommendation = None
    pred = None
    lentes_imgs = []

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
                if item["type"] == shape:
                    recommendation = item["recommendation"]
                    lentes_imgs = LENTES_IMAGES.get(shape, [])
                    break
                
            for item in FACE_TYPES:
                if item["type"]== shape:
                    recommendation = item["recommendation"]
                    break

    return render_template("index.html",
                           image_data=image_data,
                           face_type=shape,
                           recommendation=recommendation,
                           pred=round(pred, 2) if pred else 0,
                           lentes_imgs=lentes_imgs
                           )

if __name__ == "__main__":
    app.run(debug=True)