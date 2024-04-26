$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});
const dropFileZone = document.querySelector(".upload-zone_dragover")
const statusText = document.getElementById("uploadForm_Status")
const sizeText = document.getElementById("uploadForm_Size")
const uploadInput = document.querySelector(".form-upload__input")

let setStatus = (text) => {
    statusText.textContent = text
}

const uploadUrl = "/unicorns";

["dragover", "drop"].forEach(function (event) {
    document.addEventListener(event, function (evt) {
        evt.preventDefault()
        return false
    })
})

dropFileZone.addEventListener("dragenter", function () {
    dropFileZone.classList.add("_active")
})

dropFileZone.addEventListener("dragleave", function () {
    dropFileZone.classList.remove("_active")
})

dropFileZone.addEventListener("drop", function () {
    dropFileZone.classList.remove("_active")
    const file = event.dataTransfer?.files[0]
    if (!file) {
        return
    }

    if (file.type.startsWith("image/")) {
        uploadInput.files = event.dataTransfer.files
        processingUploadFile()
    } else {
        setStatus("Можно загружать только изображения")
        return false
    }
    handleFileSelect(uploadInput);
})

uploadInput.addEventListener("change", (event) => {
    const file = uploadInput.files?.[0]
    if (file && file.type.startsWith("image/")) {
        processingUploadFile()
    } else {
        setStatus("Можно загружать только изображения")
        return false
    }
    handleFileSelect(uploadInput);
})

function processingUploadFile(file) {
    if (file) {
        const dropZoneData = new FormData()
        const xhr = new XMLHttpRequest()

        dropZoneData.append("file", file)

        xhr.open("POST", uploadUrl, true)

        xhr.send(dropZoneData)

        xhr.onload = function () {
            if (xhr.status == 200) {
                setStatus("Всё загружено")
            } else {
                setStatus("Oшибка загрузки")
            }
            HTMLElement.style.display = "none"
        }
    }
}

function processingDownloadFileWithFetch() {
    fetch(url, {
        method: "POST",
    }).then(async (res) => {
        const reader = res?.body?.getReader();
        while (true && reader) {
            const { value, done } = await reader?.read()
            console.log("value", value)
            if (done) break
            console.log("Received", value)
        }
    })
}

function handleFileSelect(evt) {
    var files = uploadInput.files; // FileList object
    $('.thumb').remove();

    // Loop through the FileList and render image files as thumbnails.
    for (var i = 0, f; f = files[i]; i++) {

        // Only process image files.
        if (!f.type.match('image.*')) {
            continue;
        }

        var reader = new FileReader();

        // Closure to capture the file information.
        reader.onload = (function (theFile) {
            return function (e) {
                // Render thumbnail.
                var div = document.createElement('div');
                div.setAttribute('class', 'col');
                div.innerHTML = ['<img class="thumb object-fit-cover" src="', e.target.result,
                    '" title="', escape(theFile.name), '"/>'].join('');
                document.getElementById('previewImg').insertBefore(div, null);
            };
        })(f);

        // Read in the image file as a data URL.
        reader.readAsDataURL(f);
    }
}

document.getElementById('uploadForm_File').addEventListener('change', handleFileSelect, false);
