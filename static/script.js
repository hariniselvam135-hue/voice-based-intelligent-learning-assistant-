```javascript
// ==========================================
// Voice-Based Smart Learning Assistant
// JavaScript Frontend Logic
// ==========================================


// Get HTML elements
const questionInput = document.getElementById("question");
const userQuestion = document.getElementById("userQuestion");
const answerBox = document.getElementById("answer");
const statusText = document.getElementById("status");


// ==========================================
// ASK QUESTION TO BACKEND
// ==========================================

function askQuestion() {

    const question = questionInput.value.trim();

    // Check empty question
    if (question === "") {

        answerBox.innerText =
            "Please enter or speak a question.";

        return;
    }


    // Display user question
    userQuestion.innerText = question;

    statusText.innerText =
        "Processing your question...";


    // Send question to Flask backend
    fetch("/ask", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question
        })

    })

    .then(response => {

        if (!response.ok) {
            throw new Error("Server error");
        }

        return response.json();

    })

    .then(data => {

        // Display assistant answer
        answerBox.innerText = data.answer;

        statusText.innerText =
            "Response generated successfully.";


        // ==========================================
        // TEXT TO SPEECH
        // ==========================================

        if ("speechSynthesis" in window) {

            // Stop previous speech
            window.speechSynthesis.cancel();

            const speech =
                new SpeechSynthesisUtterance(data.answer);

            speech.lang = "en-US";

            speech.rate = 1;

            speech.pitch = 1;

            window.speechSynthesis.speak(speech);
        }

    })

    .catch(error => {

        console.error(error);

        answerBox.innerText =
            "Unable to connect to the server.";

        statusText.innerText =
            "An error occurred. Please try again.";

    });
}



// ==========================================
// VOICE RECOGNITION
// ==========================================

function startVoice() {

    // Check browser support
    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Voice recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge."
        );

        return;
    }


    // Create speech recognition object
    const recognition =
        new SpeechRecognition();


    // Language
    recognition.lang = "en-US";


    // Recognize only one sentence
    recognition.continuous = false;


    // Don't show partial results
    recognition.interimResults = false;


    // Status
    statusText.innerText =
        "🎙️ Listening... Please speak.";


    // Start microphone
    recognition.start();


    // ==========================================
    // WHEN SPEECH IS RECOGNIZED
    // ==========================================

    recognition.onresult = function(event) {

        const voiceText =
            event.results[0][0].transcript;


        // Put voice text into input box
        questionInput.value = voiceText;


        // Display question
        userQuestion.innerText = voiceText;


        statusText.innerText =
            "Voice recognized successfully.";


        // Send question to backend
        askQuestion();
    };


    // ==========================================
    // SPEECH RECOGNITION ERROR
    // ==========================================

    recognition.onerror = function(event) {

        console.error(
            "Speech recognition error:",
            event.error
        );


        statusText.innerText =
            "Unable to recognize your voice. Please try again.";
    };


    // ==========================================
    // SPEECH RECOGNITION ENDED
    // ==========================================

    recognition.onend = function() {

        if (
            statusText.innerText.includes("Listening")
        ) {

            statusText.innerText =
                "Voice recognition stopped.";
        }
    };
}



// ==========================================
// ENTER KEY SUPPORT
// ==========================================

questionInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            askQuestion();
        }

    }
);
```
