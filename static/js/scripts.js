// State Management
let currentMode = "encode";

const modes = {
    encode: {
        title: "Encode Image",
        desc: "Convert an image file to Base64 encoded text.",
        fileLabel: "Select Image",
        fileAccept: "image/*",
        fileKey: "image_to_encode",
        endpoint: "/encode",
        needsSeed: false,
        needsQuality: false,
    },
    decode: {
        title: "Decode Text",
        desc: "Convert a Base64 text file back to an image.",
        fileLabel: "Select Text File",
        fileAccept: ".txt",
        fileKey: "encoded_text",
        endpoint: "/decode",
        needsSeed: false,
        needsQuality: false,
    },
    shuffle: {
        title: "Shuffle Pixels",
        desc: "Scramble image pixels based on a numeric seed.",
        fileLabel: "Select Image",
        fileAccept: "image/*",
        fileKey: "origin_image",
        endpoint: "/shuffle",
        needsSeed: true,
        needsQuality: true,
    },
    recover: {
        title: "Recover Pixels",
        desc: "Restore a scrambled image using the original seed.",
        fileLabel: "Select Shuffled Image",
        fileAccept: "image/*",
        fileKey: "shuffled_image",
        endpoint: "/recover",
        needsSeed: true,
        needsQuality: true,
    },
};

function setMode(mode) {
    currentMode = mode;
    const config = modes[mode];

    // Update UI Text
    document.getElementById("form-title").innerText = config.title;
    document.getElementById("form-desc").innerText = config.desc;
    document.getElementById("btn-text").innerText =
        mode.charAt(0).toUpperCase() + mode.slice(1);

    // Update Tabs
    document
        .querySelectorAll(".md-tab")
        .forEach((t) => t.classList.remove("active"));
    document.getElementById(`tab-${mode}`).classList.add("active");

    // Update Inputs
    const fileInput = document.getElementById("file-input");
    fileInput.value = ""; // Clear file
    fileInput.accept = config.fileAccept;
    document.getElementById("file-name").innerText = "No file selected";

    // Toggle Seed Input
    const seedContainer = document.getElementById("seed-container");
    const seedInput = document.getElementById("seed-input");

    if (config.needsSeed) {
        seedContainer.classList.remove("hidden");
        seedInput.required = true;
    } else {
        seedContainer.classList.add("hidden");
        seedInput.required = false;
        seedInput.value = "";
    }

    // Toggle Quality Input
    const qualityContainer = document.getElementById("quality-container");
    const qualityInput = document.getElementById("quality-input");

    if (config.needsQuality) {
        qualityContainer.classList.remove("hidden");
        qualityInput.required = true;
    } else {
        qualityContainer.classList.add("hidden");
        qualityInput.required = false;
        // We leave the value as is (High by default) or reset it if needed
    }

    // Hide Error
    document.getElementById("error-msg").classList.add("hidden");
}

function updateFileName(input) {
    const fileNameDisplay = document.getElementById("file-name");
    if (input.files && input.files.length > 0) {
        fileNameDisplay.innerText = input.files[0].name;
        fileNameDisplay.style.opacity = "1";
    } else {
        fileNameDisplay.innerText = "No file selected";
        fileNameDisplay.style.opacity = "0.7";
    }
}

async function handleSubmit(e) {
    e.preventDefault();

    const config = modes[currentMode];
    const fileInput = document.getElementById("file-input");
    const seedInput = document.getElementById("seed-input");
    const qualityInput = document.getElementById("quality-input");
    const submitBtn = document.getElementById("submit-btn");
    const btnText = document.getElementById("btn-text");
    const loader = document.getElementById("loader");
    const errorMsg = document.getElementById("error-msg");

    // Validation
    if (!fileInput.files[0]) {
        showError("Please select a file.");
        return;
    }

    // UI Loading State
    submitBtn.disabled = true;
    submitBtn.classList.add("opacity-75");
    btnText.classList.add("hidden");
    loader.classList.remove("hidden");
    errorMsg.classList.add("hidden");

    const formData = new FormData();
    formData.append(config.fileKey, fileInput.files[0]);

    // Append Seed
    if (config.needsSeed) {
        if (!seedInput.value) {
            showError("Seed is required.");
            resetBtn();
            return;
        }
        formData.append("seed", seedInput.value);
    }

    // Append Quality
    if (config.needsQuality) {
        formData.append("image_quality", qualityInput.value);
    }

    try {
        const response = await fetch(config.endpoint, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.statusText}`);
        }

        // Handle File Download
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const disposition = response.headers.get("Content-Disposition");
        let filename = "result";

        if (disposition && disposition.indexOf("attachment") !== -1) {
            const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            const matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, "");
            }
        } else {
            // Fallback filename logic
            const ext = currentMode === "encode" ? ".txt" : ".png";
            filename = `pixelpuzzle_${Date.now()}${ext}`;
        }

        // Trigger Download
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(downloadUrl);
    } catch (err) {
        console.error(err);
        showError("An error occurred while processing. Please try again.");
    } finally {
        resetBtn();
    }

    function resetBtn() {
        submitBtn.disabled = false;
        submitBtn.classList.remove("opacity-75");
        btnText.classList.remove("hidden");
        loader.classList.add("hidden");
    }

    function showError(msg) {
        document.getElementById("error-text").innerText = msg;
        errorMsg.classList.remove("hidden");
    }
}

// Initialize drag and drop
const dropZone = document.getElementById("drop-zone");

["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

dropZone.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    document.getElementById("file-input").files = files;
    updateFileName(document.getElementById("file-input"));
}
