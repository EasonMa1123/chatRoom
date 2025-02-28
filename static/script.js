




function logout(){
    document.location.href = "/";
    sessionStorage.setItem("Username","")
    sessionStorage.setItem("Password","")
    sessionStorage.setItem("room","")
}

function direct_to_adminP(){
    document.location.href = "/admin";
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
            
            chatBox.append(`<p><b>[${msg.role}] </b><b>${msg.username}:</b> ${msg.message}   <b style="float: right;">${msg.timestamp}</b></p>`);
        });
    });
}

function sendMessage() {
    let username = sessionStorage.getItem("Username");
    let message = $('#message').val();
    if (username && message) {
        $.post('/send', {username: username, message: message, room_code: roomCode,role:sessionStorage.getItem("role")}, function() {
            $('#message').val('');
            loadMessages();
        });
    }
}


function leave_room(){
    document.location.href = "/lobby";
    sessionStorage.setItem("room","")
}

// Auto-refresh chat every 3 seconds
setInterval(loadMessages, 3000);
$(document).ready(loadMessages);