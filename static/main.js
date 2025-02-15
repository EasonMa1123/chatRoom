const socket = io();

$('#login-form').submit(function(e) {
    e.preventDefault();
    var username = $('#login-username').val();
    var password = $('#login-password').val();
    if (username.trim() !== '' && password.trim() !== '') {
        socket.emit('login', { username: username, password: password });
        $('#login-username').val('');
        $('#login-password').val('');
        $('.login-form').hide();
        $('.signup-form').hide();
        $('#name-form').hide();
        $('#message-form').show();
        $('#chat-messages').show();
    }
});

// Handle signup form submission
$('#signup-form').submit(function(e) {
    e.preventDefault();
    var username = $('#signup-username').val();
    var password = $('#signup-password').val();
    if (username.trim() !== '' && password.trim() !== '') {
        socket.emit('signup', { username: username, password: password });
        $('#signup-username').val('');
        $('#signup-password').val('');
    }
});

// Handle message submission
$('#message-submit-form').submit(function(e) {
    e.preventDefault();
    var message = $('#message-input').val();
    if (message.trim() !== '') {
        socket.emit('message', { message: message });
        $('#message-input').val('');
    }
});
socket.on('login_success', function() {
    $('.login-form').hide();
    $('.signup-form').hide();
    $('#name-form').hide();
    $('#message-form').show();
    $('#chat-messages').show();
});

// Handle login failure
socket.on('login_failure', function() {
    $('#message-form').hide();
    $('#chat-messages').hide();
    $('.login-form').show();
    $('.signup-form').show();
    alert('Invalid username or password');
    // Additional error handling if desired
});
// Handle incoming messages
socket.on('new_message', function(data) {
    var username = data.username;
    var message = data.message;
    var messageElement = $('<p><strong>' + username + ':</strong> ' + message + '</p>');
    chatMessages.append(messageElement);
    chatMessages.scrollTop(chatMessages[0].scrollHeight); // Scroll to the bottom
});
// Handle incoming messages(non-broadcast)
socket.on('bad_word_non_boardcast', function() {
    alert('Please do not use this word!'); 
});
// Handle repeated sign up
socket.on('repeated_sign_up_non_boardcast', function() {
    alert('This account has been sign up'); 
});
// Handle incoming user
socket.on('new_user_intro', function(data) {
    var message = data.message;
    var messageElement = $('<p><strong>' + message + '</strong></p>');
    chatMessages.append(messageElement);
    chatMessages.scrollTop(chatMessages[0].scrollHeight); // Scroll to the bottom
});