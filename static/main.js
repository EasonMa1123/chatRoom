
var socket = io();

socket.on("message", function (msg) {
    let chatBox = document.getElementById("chat-box");
    let messageElement = document.createElement("div");
    messageElement.textContent = msg;
    chatBox.appendChild(messageElement);
});

function sendMessage() {
    let messageInput = document.getElementById("message");
    let message = messageInput.value;
    if (message.trim() !== "") {
        socket.emit('message', message);
        messageInput.value = "";
    }
};
