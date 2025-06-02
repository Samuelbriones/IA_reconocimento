const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const capturedInput = document.getElementById('captured_image');
const toggleCamBtn = document.getElementById('toggleCamBtn');

let stream = null;
let camOn = false;

async function encenderCamara() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        camOn = true;
        toggleCamBtn.textContent = '🔴 Apagar cámara';
    } catch (err) {
        alert('No se pudo acceder a la cámara: ' + err);
    }
}

function apagarCamara() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        camOn = false;
        toggleCamBtn.textContent = '🔴 Encender cámara';
    }
}

toggleCamBtn.addEventListener('click', () => {
    if (camOn) {
        apagarCamara();
    } else {
        encenderCamara();
    }
});

function capturarFoto() {
    if (!camOn) {
        alert('Por favor, enciende la cámara primero.');
        return;
    }
    const context = canvas.getContext('2d');
    canvas.style.display = 'block';
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/png');
    capturedInput.value = dataUrl;
    document.getElementById('fileInput').value = '';  // Limpiar input file si había imagen cargada
}
