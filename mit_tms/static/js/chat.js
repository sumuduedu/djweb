function toggleChat() {
    document.getElementById("chatBox").classList.toggle("hidden");
}

function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value;

    fetch("/chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        const messages = document.getElementById("messages");

        messages.innerHTML += `<div>👤 ${message}</div>`;
        messages.innerHTML += `<div>🤖 ${data.reply}</div>`;

        input.value = "";
    });
}

function getCSRFToken() {
    return document.cookie.split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
}
