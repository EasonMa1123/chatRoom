



// index.html

function check_invalid_enter(){
    if(sessionStorage.getItem("Username") == null){
        alert("What are you doing in here,this is not your place,leave! Thank You :)")
        logout()
    }
}






function logout(){
    document.location.href = "/";
    sessionStorage.setItem("",Username)
    sessionStorage.setItem("",Password)
}


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
