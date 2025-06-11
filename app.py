from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import base64
import random
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Datos quemados para simular predicciones
FACE_TYPES = [
    {"type": "Ovalado", "recommendation": "Lentes cuadrados para equilibrar las proporciones."},
    {"type": "Redondo", "recommendation": "Lentes angulares para afilar los rasgos."},
    {"type": "Cuadrado", "recommendation": "Lentes redondeados o tipo aviador para suavizar."},
    {"type": "Alargado", "recommendation": "Lentes altas para acortar visualmente el rostro."},
    {"type": "Corazón", "recommendation": "Lentes sin montura o redondos para balancear la frente amplia."},
]

def save_base64_image(data_url, upload_folder):
    """Convierte imagen base64 en archivo y lo guarda."""
    header, encoded = data_url.split(',', 1)
    file_ext = header.split('/')[1].split(';')[0]
    filename = f"captured_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_ext}"
    filepath = os.path.join(upload_folder, filename)
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(encoded))
    return filepath

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    face_type = None
    recommendation = None

    if request.method == "POST":
        # 1. Imagen subida
        if "image" in request.files and request.files["image"].filename != "":
            image = request.files["image"]
            filename = secure_filename(image.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(path)
            image_url = path
            

        # 2. Imagen capturada desde la cámara (base64)
        elif "captured_image" in request.form and request.form["captured_image"] != "":
            data_url = request.form["captured_image"]
            path = save_base64_image(data_url, app.config["UPLOAD_FOLDER"])
            image_url = path

        # Selecciona datos quemados aleatorios
        result = random.choice(FACE_TYPES)
        face_type = result["type"]
        recommendation = result["recommendation"]

    return render_template("index.html",
                           image_url=image_url,
                           face_type=face_type,
                           recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
