function login_open(){
    document.getElementById("signup-form").style.display = "None";
    document.getElementById("login-form").style.display = "flex";

}

function signup_open(){
    document.getElementById("signup-form").style.display = "flex";
    document.getElementById("login-form").style.display = "None";

}


function confirm_new_user_data(){
    let Username = document.getElementById("signup-Username").value
    let Password = document.getElementById("signup-Password").value
    let Confirm_password = document.getElementById("ConfirmPassword").value
    const Confirm_email = document.getElementById("signup-email").value


    
    if (Username == "") {
        alert("please enter a username")
    }else if(Password == ""){
        alert("Please enter a password")
    }else if (Password != Confirm_password){
        alert("Invalid Password confirmation!")
    }else{

        $.post('/email_verification',{Email:Confirm_email}, function(data) {
            
            document.getElementById("code-input").style.display = "flex"
            document.getElementById("Submit-button").style.display = "flex"
            
            sessionStorage.setItem("code",data.Code)
            
            
        }
        )
        alert("Email sent,please enter the code")
    }
}


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
                alert("Vaild Signup,please login to enter!")}});
        }else{alert("Invalid Code,please submit again!")}
}
    


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


function joinRoom() {
    let roomCode = $("#room-code").val();
    $.post('/join_room', {room_code: roomCode}, function(response) {
        if (response.Feedback === "Success") {
            window.location.href = `/index/${roomCode}`;
            sessionStorage.setItem("room",roomCode)
        } else {
            alert("Room not found!");
        }
    });
}

function createRoom() {
    let roomCode = $("#new-room-code").val();
    $.post('/create_room', function(response) {
        if (response.Feedback === "Room created") {
            window.location.href = `/index/${response.room_code}`;
            sessionStorage.setItem("room",response.room_code)
        } else {
            alert(response.Feedback);
        }
    });
}


function submit_command(){
    var field = document.getElementById("field-area").value
    var table = document.getElementById("table-area").value
    var param = document.getElementById("param-area").value
    $.post('/customSQL',{field:field,table:table,param:param},function(data){
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


function showTable(){
    $.getJSON('/showdb',function(data){
        document.getElementById("log").innerHTML= data.field
    })
}

function return_room(){
    window.location.href = `/index/${sessionStorage.getItem("room")}`;
}