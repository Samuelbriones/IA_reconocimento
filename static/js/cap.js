const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const capturedInput = document.getElementById('captured_image');
const toggleCamBtn = document.getElementById('toggleCamBtn');
const resetCamBtn = document.getElementById('resetCamBtn');
const camButtons = document.getElementById('camButtons');

let stream = null;
let camOn = false;

async function encenderCamara() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        await video.play(); // <-- Importante para algunos navegadores
        camOn = true;
        toggleCamBtn.textContent = '🔴 Apagar cámara';
        video.classList.remove('hidden');
        canvas.classList.add('hidden');
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
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/png');
    capturedInput.value = dataUrl;
    document.getElementById('fileInput').value = '';

    video.classList.add('hidden');
    canvas.classList.remove('hidden');
    camButtons.classList.add('hidden');
    resetCamBtn.classList.remove('hidden');
}

resetCamBtn.addEventListener('click', () => {
    canvas.classList.add('hidden');
    video.classList.remove('hidden');
    camButtons.classList.remove('hidden');
    resetCamBtn.classList.add('hidden');
    capturedInput.value = '';
    if (!camOn) {
        encenderCamara();
    }
});

