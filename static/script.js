document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', sender);
        messageElement.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(messageElement);

        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        addMessage(messageText, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'content-type':'application/json',
                },
                body: JSON.stringify({ message: messageText}),
            });

            if (!response.ok) {
                throw new Error('Gagal mendapatkan respons dari server');
            }

            const data = await response.json();

            addMessage(data.reply, 'bot');
        } catch (error) {
            console.error('Error:', error);
            addMessage('Maaf, terjadi kesalahan. Coba lagi nanti. ', 'bot');
        }
    }

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    })
})

