function setQuestion(text) {
    document.getElementById("question").value = text;
}


// ===============================
// MCQ GENERATOR
// ===============================

function generateMCQ() {

    let number = document.getElementById("mcq-number").value;
    let level = document.getElementById("mcq-level").value;

    let prompt = `
Generate ${number} multiple-choice questions based on this PDF.

Difficulty level: ${level}

Instructions:

- Create exactly ${number} questions.
- Each question must have 4 options:
  A)
  B)
  C)
  D)
- Clearly show the correct answer.
- Provide a short explanation after each answer.
- Make sure the questions cover different sections of the PDF.
- Avoid repeating similar questions.
`;

    document.getElementById("question").value = prompt;

}


// ===============================
// FLASHCARD FLIP
// ===============================

function flipCard(card) {

    card.classList.toggle("flipped");

}


// ===============================
// LOADING SCREEN
// ===============================

const loadingScreen = document.getElementById("loading-screen");

if (loadingScreen) {

    loadingScreen.classList.add("hidden");

}


// Upload form

const uploadForm = document.getElementById("upload-form");

if (uploadForm) {

    uploadForm.addEventListener("submit", function () {

        if (loadingScreen) {
            loadingScreen.classList.remove("hidden");
        }

    });

}


// Question form

const questionForm = document.getElementById("question-form");

if (questionForm) {

    questionForm.addEventListener("submit", function () {

        if (loadingScreen) {
            loadingScreen.classList.remove("hidden");
        }

    });

}
// Study Tools forms

const toolForms = document.querySelectorAll(".tool-form");

toolForms.forEach(function(form) {

    form.addEventListener("submit", function() {

        if (loadingScreen) {
            loadingScreen.classList.remove("hidden");
        }

    });

});
// =========================================
// FLASHCARD SYSTEM
// =========================================

function createFlashcards() {

    const answerContainers =
        document.querySelectorAll(".answer-content");


    answerContainers.forEach(function(container) {

        const text = container.innerText.trim();


        // Check whether this is a flashcard response

        if (!text.includes("FLASHCARD 1")) {
            return;
        }


        // Split the AI response into flashcards

        const sections =
            text.split(/FLASHCARD\s+\d+/i)
                .filter(section => section.trim() !== "");


        if (sections.length === 0) {
            return;
        }


        const flashcardsContainer =
            document.createElement("div");

        flashcardsContainer.className =
            "flashcards-container";


        sections.forEach(function(section) {

            const frontMatch =
                section.match(
                    /FRONT:\s*([\s\S]*?)(?=BACK:)/i
                );


            const backMatch =
                section.match(
                    /BACK:\s*([\s\S]*)/i
                );


            if (!frontMatch || !backMatch) {
                return;
            }


            const front =
                frontMatch[1].trim();


            const back =
                backMatch[1].trim();


            // Create card

            const card =
                document.createElement("div");

            card.className =
                "flashcard";


            card.innerHTML = `

                <div class="flashcard-inner">

                    <div class="flashcard-front">

                        <div class="flashcard-label">
                            Question
                        </div>

                        <h3>
                            ${front}
                        </h3>

                        <div class="flashcard-hint">
                            👆 Click to reveal answer
                        </div>

                    </div>


                    <div class="flashcard-back">

                        <div class="flashcard-label">
                            Answer
                        </div>

                        <p>
                            ${back}
                        </p>

                        <div class="flashcard-hint">
                            👆 Click to flip back
                        </div>

                    </div>

                </div>

            `;


            // Flip card when clicked

            card.addEventListener(
                "click",
                function() {

                    card.classList.toggle("flipped");

                }
            );


            flashcardsContainer.appendChild(card);

        });


        // Only replace the AI response
        // if actual cards were created

        if (flashcardsContainer.children.length > 0) {

            container.innerHTML = "";

            container.appendChild(
                flashcardsContainer
            );

        }

    });

}


// Run after page loads

document.addEventListener(
    "DOMContentLoaded",
    function() {

        createFlashcards();

    }
);

function copyAnswer(button) {

    const aiAnswer = button.previousElementSibling;

    const text = aiAnswer.innerText;

    navigator.clipboard.writeText(text)
        .then(() => {

            button.innerText = "✅ Copied!";

            setTimeout(() => {
                button.innerText = "📋 Copy";
            }, 2000);

        })
        .catch(() => {

            button.innerText = "❌ Failed";

        });
}