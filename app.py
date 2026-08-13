```python
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)


# =========================
# BACKEND
# =========================

def get_answer(question):

    question = question.lower().strip()

    if not question:
        return "Please ask a question."

    if "hello" in question or "hi" in question:
        return "Hello! I am your Smart Learning Assistant. How can I help you?"

    elif "python" in question:
        return "Python is a high-level programming language used for Artificial Intelligence, Data Science, Web Development and Automation."

    elif "artificial intelligence" in question or question == "ai":
        return "Artificial Intelligence is a technology that enables machines to perform tasks that normally require human intelligence."

    elif "machine learning" in question:
        return "Machine Learning is a branch of Artificial Intelligence that enables computers to learn from data and make predictions."

    elif "deep learning" in question:
        return "Deep Learning is a subset of Machine Learning that uses neural networks with multiple layers to learn complex patterns."

    elif "data science" in question:
        return "Data Science is the process of collecting, analyzing and visualizing data to discover useful information."

    elif "what is flask" in question:
        return "Flask is a lightweight Python web framework used to build web applications and APIs."

    elif "thank" in question:
        return "You're welcome! Keep learning and keep improving."

    elif "bye" in question:
        return "Goodbye! Have a great learning session."

    else:
        return (
            "I am your Voice-Based Smart Learning Assistant. "
            "Please ask questions related to Python, Artificial Intelligence, "
            "Machine Learning, Deep Learning or Data Science."
        )


# =========================
# FRONTEND
# =========================

HTML_PAGE = """

<!DOCTYPE html>

<html>

<head>

<title>Voice Based Smart Learning Assistant</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    width: 90%;
    max-width: 750px;
    background: white;
    padding: 35px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
    text-align: center;
}

h1 {
    color: #333;
}

.subtitle {
    color: #666;
}

button {
    padding: 15px 25px;
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

.voice-button {
    background: #667eea;
    margin: 20px;
}

.voice-button:hover {
    background: #4f5fc5;
}

.ask-button {
    background: #28a745;
}

.input-area {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

input {
    flex: 1;
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 10px;
    font-size: 16px;
}

.box {
    margin-top: 25px;
    padding: 20px;
    background: #f5f5f5;
    border-radius: 12px;
    text-align: left;
}

.box h3 {
    margin-top: 0;
}

#status {
    color: #777;
}

</style>

</head>


<body>

<div class="container">

<h1>🎓 Voice-Based Smart Learning Assistant</h1>

<p class="subtitle">
Interactive AI-powered learning support system
</p>


<!-- Voice Button -->

<button class="voice-button" onclick="startVoice()">

🎤 Start Speaking

</button>


<p id="status">
Click the microphone and ask your question.
</p>


<!-- Text Input -->

<div class="input-area">

<input
type="text"
id="question"
placeholder="Type your question here..."
>

<button
class="ask-button"
onclick="askQuestion()">

Ask

</button>

</div>


<!-- Question -->

<div class="box">

<h3>🗣️ Your Question</h3>

<p id="userQuestion">
Your question will appear here.
</p>

</div>


<!-- Answer -->

<div class="box">

<h3>🤖 Assistant Response</h3>

<p id="answer">
Waiting for your question...
</p>

</div>

</div>


<script>


// =========================
// SEND QUESTION TO BACKEND
// =========================

function askQuestion() {

    const question =
        document.getElementById("question").value.trim();

    const answer =
        document.getElementById("answer");

    const userQuestion =
        document.getElementById("userQuestion");

    const status =
        document.getElementById("status");


    if (question === "") {

        answer.innerText =
            "Please enter or speak a question.";

        return;
    }


    userQuestion.innerText = question;

    status.innerText =
        "Processing your question...";


    fetch("/ask", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question
        })

    })

    .then(response => response.json())

    .then(data => {

        answer.innerText =
            data.answer;

        status.innerText =
            "Response generated successfully.";


        // Text to Speech

        const speech =
            new SpeechSynthesisUtterance(
                data.answer
            );

        speech.lang = "en-US";

        window.speechSynthesis.speak(speech);

    })

    .catch(error => {

        answer.innerText =
            "Unable to connect to the server.";

        status.innerText =
            "Error occurred.";

    });

}



// =========================
// VOICE RECOGNITION
// =========================

function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Voice recognition is not supported. Please use Google Chrome or Microsoft Edge."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;


    document.getElementById("status").innerText =
        "🎙️ Listening... Please speak.";


    recognition.start();


    recognition.onresult = function(event) {

        const voiceText =
            event.results[0][0].transcript;


        document.getElementById("question").value =
            voiceText;


        document.getElementById("userQuestion").innerText =
            voiceText;


        document.getElementById("status").innerText =
            "Voice recognized successfully.";


        askQuestion();

    };


    recognition.onerror = function() {

        document.getElementById("status").innerText =
            "Unable to recognize your voice. Please try again.";

    };

}

</script>

</body>

</html>

"""


# =========================
# FLASK ROUTES
# =========================

@app.route("/")
def home():

    return render_template_string(HTML_PAGE)


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question", "")

    answer = get_answer(question)

    return jsonify({
        "answer": answer
    })


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    app.run(debug=True)
```
