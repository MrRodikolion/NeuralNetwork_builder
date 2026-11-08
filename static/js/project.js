$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});
const dropFileZone = document.querySelector('.upload-zone_dragover');
const uploadInput = document.getElementById('uploadForm_File');
const hint = document.getElementById('uploadForm_Hint');
const preview = document.getElementById('previewImg');

function showFiles() {
    preview.replaceChildren();
    hint.textContent = '';
    for (const file of uploadInput.files) {
        if (!file.type.startsWith('image/')) {
            hint.textContent = 'Можно загружать только изображения.';
            continue;
        }
        const reader = new FileReader();
        reader.addEventListener('load', () => {
            const column = document.createElement('div');
            column.className = 'col';
            const image = document.createElement('img');
            image.className = 'thumb object-fit-cover';
            image.src = reader.result;
            image.alt = file.name;
            image.title = file.name;
            column.appendChild(image);
            preview.appendChild(column);
        });
        reader.addEventListener('error', () => {
            hint.textContent = 'Не удалось прочитать файл: ' + file.name;
        });
        reader.readAsDataURL(file);
    }
}

for (const eventName of ['dragover', 'drop']) {
    document.addEventListener(eventName, event => event.preventDefault());
}
dropFileZone.addEventListener('dragenter', () => dropFileZone.classList.add('_active'));
dropFileZone.addEventListener('dragleave', () => dropFileZone.classList.remove('_active'));
dropFileZone.addEventListener('drop', event => {
    event.preventDefault();
    dropFileZone.classList.remove('_active');
    if (event.dataTransfer && event.dataTransfer.files.length) {
        uploadInput.files = event.dataTransfer.files;
        showFiles();
    }
});
uploadInput.addEventListener('change', showFiles);
