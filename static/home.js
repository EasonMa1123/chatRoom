/*
Home Page and Authentication Script
This script handles the main functionality of the home page including:
- User authentication (login/signup)
- Room management
- Admin panel functionality
- Dynamic UI updates
*/

/**
 * Switches the view to show the login form
 * Hides the signup form
 */
function login_open(){
    document.getElementById("signup-form").style.display = "None";
    document.getElementById("login-form").style.display = "flex";
}

/**
 * Switches the view to show the signup form
 * Hides the login form
 */
function signup_open(){
    document.getElementById("signup-form").style.display = "flex";
    document.getElementById("login-form").style.display = "None";
}

/**
 * Validates new user registration data
 * Initiates email verification process
 */
function confirm_new_user_data(){
    let Username = document.getElementById("signup-Username").value
    let Password = document.getElementById("signup-Password").value
    let Confirm_password = document.getElementById("ConfirmPassword").value
    const Confirm_email = document.getElementById("signup-email").value

    // Validate input fields
    if (Username == "") {
        alert("please enter a username")
    }else if(Password == ""){
        alert("Please enter a password")
    }else if (Password != Confirm_password){
        alert("Invalid Password confirmation!")
    }else if(Password.includes("DROP")){
        alert("Invalid Password")
    }else{
        // Send verification email
        $.post('/email_verification',{Email:Confirm_email}, function(data) {
            document.getElementById("code-input").style.display = "flex"
            document.getElementById("Submit-button").style.display = "flex"
            sessionStorage.setItem("code",data.Code)
        })
        alert("Email sent,please enter the code")
    }
}

/**
 * Submits new user registration
 * Verifies email code and creates user account
 */
function submit_new_user_data(){
    let user_code = document.getElementById("code-input").value
    let DataCode = sessionStorage.getItem("code")
    let Username = document.getElementById("signup-Username").value
    let Password = document.getElementById("signup-Password").value
    const Confirm_email = document.getElementById("signup-email").value
    
    if (Number(user_code) == Number(DataCode)){
        $.post('/insertNewUser',{ userName: Username, Password:Password,Email:Confirm_email.toLowerCase() }, function(data) {
            if (data.Feedback == "Invalid Username,This Username had been used "){
                alert("Invalid Username,This Username had been used ")
            } else {
                alert("Vaild Signup,please login to enter!")
            }
        });
    }else{
        alert("Invalid Code,please submit again!")
    }
}

/**
 * Handles user login
 * Validates credentials and sets up user session
 */
function login(){
    let Username = document.getElementById("login-Username").value
    let Password = document.getElementById("login-Password").value

    $.post('/CheckUserPassword',{ userName:Username,Password:Password }, function(data){
        if (data.check == true){
            sessionStorage.setItem("Username",Username)
            sessionStorage.setItem("Password",Password)
            
            $.post('/accessUserRole',{userName:Username},function(data){
                sessionStorage.setItem("role",data.role)
                Username = "";
                Password = "";
                document.location.href = "/lobby";
            })
        } else {
            alert("Incorrect Password/Username")
        }
    })
}

/**
 * Closes the room password input modal
 */
function close_room_password(){
    document.getElementById("room-password-container").style.display = "none"
}

/**
 * Opens the room password input modal
 * @param {string} roomCode - The code of the room to join
 */
function joinRoom(roomCode){
    document.getElementById("room-password-container").style.display = "flex"
    document.getElementById("selected-room-code").innerHTML = `Selected Room: ${roomCode}`
    sessionStorage.setItem("SelectRoom",roomCode)
}

/**
 * Handles joining a password-protected room
 * Validates room password and redirects to room
 */
function JoinRoomCode() {
    const roomCode = sessionStorage.getItem("SelectRoom")
    $.post('/join_room', {room_code:roomCode }, function(response) {
        if (response.Feedback === "Success") {
            const Room_password= response.roomPassword
            document.getElementById("room-password-container").style.display = "none"
            const user_password = document.getElementById("Room-password").value
            if (Room_password == user_password){
                window.location.href = `/room/${roomCode}`;
                sessionStorage.setItem("room",roomCode)
            } else {
                alert("Incorrect Password")
            }
        } else {
            alert("Room not found!");
        }
    });
}

/**
 * Creates a new chat room
 * Validates room password and creates room in database
 */
function createRoom() {
    const admin_name = sessionStorage.getItem("Username")
    const room_password = document.getElementById("room-password").value
    if (room_password != null){
        $.post('/create_room', {admin:admin_name,password:room_password},function(response) {
            if (response.Feedback === "Room created") {
                window.location.href = `/room/${response.room_code}`;
                sessionStorage.setItem("room",response.room_code)
            } else {
                alert(response.Feedback);
            }
        });
    } else {
        alert("Invalid Room Password")
    }
}

/**
 * Executes custom SQL query in admin panel
 * Handles query construction and result display
 */
function submit_command(){
    const username = sessionStorage.getItem("Username")
    const field = document.getElementById("field-area")
    const field_values = Array.from(field.selectedOptions).map(option => option.value).join(",");
    
    var table = document.getElementById("table-area").value
    var con_field = document.getElementById("con-field-area").value
    const join_table = document.getElementById("join-table-area").value
    const match_field = document.getElementById("current-field-area").value
    const join_field = document.getElementById("join-field-area").value
    const join_toggle = document.getElementById("join-SQL-toggle").checked
    var param = document.getElementById("param-area").value

    $.post('/customSQL',{
        userName:username,
        field:field_values,
        table:table,
        con_field:con_field,
        param:param,
        join_toggle:join_toggle,
        join_table:join_table,
        match_field:match_field,
        join_field:join_field
    }, function(data){
        if (data.log.startsWith("Error executing query") || data.log == true){
            document.getElementById("log").innerHTML= data.log
            let logTableDiv = document.getElementById("log-table");
            logTableDiv.innerHTML = ""; // Clear previous content
        }else{
            createTableFromString(data.log)
            document.getElementById("log").innerHTML = ""
        }
    })
}

/**
 * Creates an HTML table from query results
 * @param {string} dataString - JSON string containing query results
 */
function createTableFromString(dataString) {
    // Convert the string into a valid JSON object
    let jsonData;
    try {
        jsonData = eval("(" + dataString + ")"); // Convert string to object safely
    } catch (error) {
        console.error("Invalid data format:", error);
        return;
    }

    if (!Array.isArray(jsonData) || jsonData.length === 0) {
        console.error("Invalid or empty data");
        return;
    }

    // Create the table element
    let table = document.createElement("table");
    table.border = "1"; // Add border for visibility
    table.style.borderCollapse = "collapse";
    table.style.width = "100%";

    // Create table header
    let thead = document.createElement("thead");
    let headerRow = document.createElement("tr");

    // Get column names (keys from first object)
    let columns = Object.keys(jsonData[0]);

    columns.forEach(col => {
        let th = document.createElement("th");
        th.textContent = col;
        th.style.padding = "8px";
        th.style.backgroundColor = "#f2f2f2";
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    let tbody = document.createElement("tbody");

    jsonData.forEach(row => {
        let tr = document.createElement("tr");
        columns.forEach(col => {
            let td = document.createElement("td");
            td.textContent = row[col];
            td.style.padding = "8px";
            td.style.textAlign = "left";
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(tbody);

    // Append the table to the div with id "log-table"
    let logTableDiv = document.getElementById("log-table");
    logTableDiv.innerHTML = ""; // Clear previous content
    logTableDiv.appendChild(table);
}

/**
 * Returns to the current chat room
 */
function return_room(){
    window.location.href = `/room/${sessionStorage.getItem("room")}`;
}

/**
 * Loads and displays available chat rooms
 * Updates the room list dynamically
 */
function load_live_chat_room(){
    $.getJSON(`/room_list`, function(data) {
        let chatBox = $('#chat-room-list');
        chatBox.html('');
        data.forEach(msg => {
            chatBox.append(`<label for="room-${msg}" class="Chat-room-code">${msg}</label>
                <input type="radio" id="room-${msg}" style="display: none;" onclick=" joinRoom(${msg})"></input>`);
        });
    })
}

if (window.location.href.includes("/lobby")){
    setInterval(load_live_chat_room, 3000);
    $(document).ready(load_live_chat_room);
}
