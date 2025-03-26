function logout(){
    document.location.href = "/";
    sessionStorage.setItem("Username","")
    sessionStorage.setItem("Password","")
    sessionStorage.setItem("room","")
    sessionStorage.setItem("role","")
}

function direct_to_adminP(){
    document.location.href = "/admin";
}

let roomCode = window.location.pathname.split("/").pop(); // Get room code from URL
console.log("Room Code:", roomCode); // Debug log
document.getElementById("room-code").textContent = roomCode; // Set room code in input field          
document.getElementById("Chat-Room-Title").innerText = `Room: ${roomCode}`


function check_invalid_enter() {
    if (sessionStorage.getItem("Username") == null) {
        alert("You must log in first!");
        window.location.href = "/";
    }
}

function loadMessages() {
    console.log("Loading messages for room:", roomCode); // Debug log
    $.getJSON(`/messages/${roomCode}`, function(data) {
        console.log("Received messages:", data); // Debug log
        let chatBox = $('#chat-box');
        chatBox.html('');
        if (data && data.length > 0) {
            data.forEach(msg => {
                console.log("Processing message:", msg); // Debug log
                chatBox.append(`<p><b>[${msg.role}] </b><b>${msg.username}:</b> ${msg.message}   <b style="float: right;">${msg.timestamp}</b></p>`);
            });
        } else {
            console.log("No messages found"); // Debug log
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error("Error loading messages:", textStatus, errorThrown); // Debug log
    });
}

function sendMessage() {
    let username = sessionStorage.getItem("Username");
    let message = $('#message').val();
    let role = sessionStorage.getItem("role");
    console.log("Sending message:", {username, message, roomCode, role}); // Debug log
    
    if (username && message) {
        $.post('/send', {
            username: username, 
            message: message, 
            room_code: roomCode,
            role: role
        }, function() {
            console.log("Message sent successfully"); // Debug log
            $('#message').val('');
            loadMessages();
        }).fail(function(jqXHR, textStatus, errorThrown) {
            console.error("Error sending message:", textStatus, errorThrown); // Debug log
        });
    }
}


function leave_room(){
    document.location.href = "/lobby";
    sessionStorage.setItem("room","")
}

document.getElementById("message").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent new line
        sendMessage(); // Call sendMessage() function
    }
});

// Auto-refresh chat every 3 seconds
setInterval(loadMessages, 3000);
$(document).ready(loadMessages);
