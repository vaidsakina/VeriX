const fileInput = document.getElementById("file-input");

const verifyBtn = document.getElementById("verify-btn");

const textVerifyBtn =
    document.getElementById("text-verify-btn");

const claimInput =
    document.getElementById("claim-input");

const selectedFile =
    document.getElementById("selected-file");

const loadingEl =
    document.getElementById("loading");

const resultSection =
    document.getElementById("result-section");

const resultContent =
    document.getElementById("result-content");

const resultTitle =
    document.getElementById("result-title");

const referenceSection =
    document.getElementById("reference-section");

const referenceList =
    document.getElementById("reference-list");


// --------------------------------------------------
// File selection
// --------------------------------------------------

fileInput.addEventListener("change", function () {

    const file = fileInput.files[0];

    if (!file) {

        selectedFile.classList.add("hidden");

        verifyBtn.disabled = true;

        return;
    }


    selectedFile.textContent =
        "Selected: " + file.name;


    selectedFile.classList.remove("hidden");


    verifyBtn.disabled = false;

});



// --------------------------------------------------
// Loading
// --------------------------------------------------

function showLoading(show) {

    if (show) {

        loadingEl.classList.remove("hidden");

    } else {

        loadingEl.classList.add("hidden");

    }

}



// --------------------------------------------------
// Display AI result
// --------------------------------------------------

function showResult(result) {

    resultSection.classList.remove("hidden");

    resultTitle.textContent =
        "Analysis Complete";

    resultContent.textContent =
        result || "No analysis was returned.";

}



// --------------------------------------------------
// Display database references
// --------------------------------------------------

function showReferences(references) {

    referenceList.innerHTML = "";


    if (!references || references.length === 0) {

        referenceSection.classList.add("hidden");

        return;

    }


    referenceSection.classList.remove("hidden");


    references.forEach(function (item) {

        const card =
            document.createElement("div");

        card.className =
            "reference-card";


        const title =
            document.createElement("h4");

        title.textContent =
            item.title || "Reference Record";


        const content =
            document.createElement("p");

        content.textContent =
            item.content || "";


        const details =
            document.createElement("div");

        details.className =
            "reference-details";


        const verdict =
            document.createElement("span");

        verdict.className =
            "reference-verdict";

        verdict.textContent =
            "Verdict: " +
            (item.verdict || "Not specified");


        const source =
            document.createElement("span");

        source.className =
            "reference-source";

        source.textContent =
            "Source: " +
            (item.source || "Not specified");


        const category =
            document.createElement("span");

        category.className =
            "reference-category";

        category.textContent =
            "Category: " +
            (item.category || "General");


        details.appendChild(verdict);

        details.appendChild(source);

        details.appendChild(category);


        card.appendChild(title);

        card.appendChild(content);

        card.appendChild(details);


        referenceList.appendChild(card);

    });

}



// --------------------------------------------------
// Analyze text claim
// --------------------------------------------------

textVerifyBtn.addEventListener(
    "click",
    async function () {

        const message =
            claimInput.value.trim();


        if (!message) {

            alert(
                "Please enter a claim or message first."
            );

            return;

        }


        showLoading(true);


        resultSection.classList.add("hidden");

        referenceSection.classList.add("hidden");


        textVerifyBtn.disabled = true;


        try {

            const response =
                await fetch("/chat", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })

                });


            const data =
                await response.json();


            showResult(
                data.response ||
                "No analysis was returned."
            );


            showReferences(
                data.references || []
            );


        } catch (error) {

            console.error(error);


            showResult(
                "Unable to connect to the VeriX analysis server."
            );


            showReferences([]);

        } finally {

            showLoading(false);

            textVerifyBtn.disabled = false;

        }

    }
);



// --------------------------------------------------
// Analyze uploaded file
// --------------------------------------------------

verifyBtn.addEventListener(
    "click",
    async function () {

        const file =
            fileInput.files[0];


        if (!file) {

            alert(
                "Please select a file first."
            );

            return;

        }


        let endpoint = null;


        if (file.type.startsWith("image/")) {

            endpoint =
                "/analyze_image";

        }

        else if (file.type.startsWith("audio/")) {

            endpoint =
                "/analyze_audio";

        }

        else if (file.type.startsWith("video/")) {

            endpoint =
                "/analyze_video";

        }

        else {

            alert(
                "Unsupported file type. Please upload an image, audio, or video."
            );

            return;

        }


        const formData =
            new FormData();


        formData.append(
            "file",
            file
        );


        showLoading(true);


        resultSection.classList.add("hidden");

        referenceSection.classList.add("hidden");


        verifyBtn.disabled = true;


        try {

            const response =
                await fetch(endpoint, {

                    method: "POST",

                    body: formData

                });


            const data =
                await response.json();


            showResult(
                data.response ||
                "No analysis was returned."
            );


            showReferences(
                data.references || []
            );


        } catch (error) {

            console.error(error);


            showResult(
                "Unable to connect to the VeriX analysis server."
            );


        } finally {

            showLoading(false);


            verifyBtn.disabled = true;


            fileInput.value = "";


            selectedFile.classList.add(
                "hidden"
            );

        }

    }
);


