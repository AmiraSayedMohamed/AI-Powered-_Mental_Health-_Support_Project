document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();

    if (message === "") return;

    // Add user message to chat box
    appendMessage("user", message);
    userInput.value = "";

    // Show loading indicator
    const loadingIndicator = document.createElement("div");
    loadingIndicator.id = "loading";
    loadingIndicator.textContent = "Thinking...";
    document.getElementById("chat-box").appendChild(loadingIndicator);

    // Send message to backend
    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
    })
        .then((response) => response.json())
        .then((data) => {
            // Remove loading indicator
            document.getElementById("loading").remove();

            if (data.response) {
                appendMessage("bot", data.response);
            } else if (data.error) {
                appendMessage("bot", "Sorry, something went wrong. Please try again.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            // Remove loading indicator
            document.getElementById("loading").remove();
            appendMessage("bot", "Sorry, I couldn't process your request.");
        });
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.innerHTML = `<p>${message}</p>`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}