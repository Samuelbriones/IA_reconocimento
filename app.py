
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    face_type = None
    recommendation = None

    if request.method == "POST":
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":
                filename = secure_filename(image.filename)
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(path)
                image_url = path

                # Datos quemados
                face_type = "Ovalado"
                recommendation = "Lentes cuadrados para equilibrar las proporciones."

    return render_template("index.html", image_url=image_url, face_type=face_type, recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
