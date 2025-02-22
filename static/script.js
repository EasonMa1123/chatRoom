




function logout(){
    document.location.href = "/";
    sessionStorage.setItem("",Username)
    sessionStorage.setItem("",Password)
}

let roomCode = window.location.pathname.split("/").pop(); // Get room code from URL
document.getElementById("room-code").textContent = roomCode; // Set room code in input field          
function check_invalid_enter() {
    if (sessionStorage.getItem("Username") == null) {
        alert("You must log in first!");
        window.location.href = "/";
    }
}

function loadMessages() {
    $.getJSON(`/messages/${roomCode}`, function(data) {
        let chatBox = $('#chat-box');
        chatBox.html('');
        data.forEach(msg => {
            chatBox.append(`<p><b>${msg.username}:</b> ${msg.message}</p>`);
        });
    });
}

function sendMessage() {
    let username = sessionStorage.getItem("Username");
    let message = $('#message').val();
    if (username && message) {
        $.post('/send', {username: username, message: message, room_code: roomCode}, function() {
            $('#message').val('');
            loadMessages();
        });
    }
}

// Auto-refresh chat every 3 seconds
setInterval(loadMessages, 3000);
$(document).ready(loadMessages);