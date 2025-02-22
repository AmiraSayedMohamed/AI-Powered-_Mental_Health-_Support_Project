document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const chatContainer = document.getElementById('chatContainer');
    const sendButton = document.querySelector('button');
    let isProcessing = false;

    // Handle both Enter key and button click
    const handleSend = () => {
        if (!isProcessing) sendMessage();
    };

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });

    sendButton.addEventListener('click', handleSend);

    async function sendMessage() {
        if (isProcessing) return;
        isProcessing = true;
        
        const message = userInput.value.trim();
        if (!message) {
            isProcessing = false;
            return;
        }

        // Immediately add user message
        addMessage('user', message);
        userInput.value = '';
        userInput.disabled = true;
        sendButton.disabled = true;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            addMessage('bot', data.response);
        } catch (error) {
            addMessage('bot', 'Sorry, I encountered an error. Please try again.');
        } finally {
            isProcessing = false;
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});