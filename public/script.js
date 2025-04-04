document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'You' ? 'user-message' : 'bot-message');
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessage(message) {
        appendMessage('You', message);
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('Bot', data.response);
            if (data.quickReplies) {
                data.quickReplies.forEach(reply => {
                    const button = document.createElement('button');
                    button.textContent = reply;
                    button.onclick = () => sendMessage(reply);
                    chatBox.appendChild(button);
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }

    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            sendMessage(message);
            userInput.value = '';
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && userInput.value.trim()) {
            sendMessage(userInput.value.trim());
            userInput.value = '';
        }
    });

    // Initial message
    sendMessage('start');
});