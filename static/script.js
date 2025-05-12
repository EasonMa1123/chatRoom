/*
Main Chat Room Script
This script handles the core chat room functionality including:
- User authentication
- Message sending and receiving
- Room management
- Auto-refresh functionality
*/

/**
 * Logs out the current user and clears session storage
 * Redirects to the login page
 */
function logout(){
    document.location.href = "/";
    $.post('/remove_session_data',{Session_ID:sessionStorage.getItem("Session_ID")})
}

/**
 * Redirects the user to the admin panel
 */
function direct_to_adminP(){
    document.location.href = "/admin";
}

// Get room code from URL and update UI
let roomCode = window.location.pathname.split("/").pop(); // Get room code from URL
console.log("Room Code:", roomCode); // Debug log
document.getElementById("room-code").textContent = roomCode; // Set room code in input field          
document.getElementById("Chat-Room-Title").innerText = `Room: ${roomCode}`

/**
 * Checks if user is properly authenticated
 * Redirects to login page if not authenticated
 */
function check_invalid_enter() {
    $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"Username"},function(data){
        if (data.item_Value == null) {
            alert("You must log in first!");
            window.location.href = "/";
        }})
}

/**
 * Loads and displays chat messages for the current room
 * Fetches messages from server and updates the chat box
 */
function loadMessages() {
    console.log("Loading messages for room:", roomCode); // Debug log
    $.getJSON(`/messages/${roomCode}`, function(data) {
        var message_data = data
        $.post('/decrypting_message',{message:JSON.stringify(message_data),room_code:roomCode},function(data){
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
            }})
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error("Error loading messages:", textStatus, errorThrown); // Debug log
    });
}

/**
 * Sends a new message to the chat room
 * Includes username, message content, room code, and user role
 */
function sendMessage() {
    $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"Username"},function(data){
        let username = data.item_Value
        let message = $('#message').val();
        $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"role"},function(data){
            let role =  data.item_Value
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
            }})})
}

/**
 * Allows user to leave the current chat room
 * Redirects to the lobby and clears room data
 */
function leave_room(){
    document.location.href = "/lobby";
    sessionStorage.setItem("room","")
}

// Add event listener for Enter key in message input
document.getElementById("message").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent new line
        sendMessage(); // Call sendMessage() function
    }
});

// Auto-refresh chat every 3 seconds
setInterval(loadMessages, 3000);
$(document).ready(loadMessages);
