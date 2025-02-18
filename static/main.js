function loadMessages() {
    $.getJSON('/messages', function(data) {
        let chatBox = $('#chat-box');
        chatBox.html('');
        data.forEach(msg => {
            chatBox.append(`<p><b>${msg.username}:</b> ${msg.message}</p>`);
        });
    });
}

function sendMessage() {
    let username = sessionStorage.getItem("Username")
    let message = $('#message').val();
    if (username && message) {
        $.post('/send', {username: username, message: message}, function() {
            $('#message').val('');
            loadMessages();
        });
    }
}

// Auto-refresh chat every 3 seconds
setInterval(loadMessages, 3000);
$(document).ready(loadMessages);
