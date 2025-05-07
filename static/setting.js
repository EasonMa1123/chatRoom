/*
User Settings Management Script
This script handles all user settings functionality including:
- Theme switching (dark/bright mode)
- Font size adjustment
- Username changes
- Password updates
- Email verification
*/

/**
 * Sets the application theme to dark mode
 */
function set_dark_theme(){
    document.body.style.backgroundColor = "#121212";
}

/**
 * Sets the application theme to bright mode
 */
function set_bright_theme(){
    document.body.style.backgroundColor = "#575757";
}

/**
 * Updates the font size across the application
 * @param {string} size - The new font size in pixels
 */
function set_font_size(size){
    document.body.style.fontSize = `${size}px`
}

/**
 * Handles username change requests
 * Validates input and updates username in database
 */
function ChangeUserName(){
    const old_username = document.getElementById("Current-username").value;
    const new_username = document.getElementById("New-username").value;

    if (old_username == "" || new_username == ""|| old_username == " " || new_username == " "  ){
        alert("Invalid Username ")
    }
    else if (old_username == new_username){
        alert("Same Username!")
    } else{
        $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"Username"},function(data){
            if(old_username == data.item_Value){
            $.post("/access_account_detail",{Username:old_username},function(data){
                const id = data.ID
                $.post("/update_account_username",{id:id,New_username:new_username})
                store_data(sessionStorage.getItem("Session_ID"),"Username",new_username)
                alert("UserName Changed")
        })}})
    }
}

/**
 * Store Data to custom Json
 */
function store_data(session_ID,item_name,item_value){
    
    $.post('/Store_session_data',{Session_ID:session_ID,Item_Name:item_name,Item_Value:item_value})
}


/**
 * Handles password change requests
 * Validates current password and checks strength of new password
 */
function ChangePassword(){
    const old_Password = document.getElementById("Current-password").value;
    const new_Password = document.getElementById("New-password").value;

    if (old_Password == new_Password){
        alert("Same Password!")
    } else if(old_Password == sessionStorage.getItem("Password")){
        $.post('/password_strength',{Password:new_Password},function(data){
            if (data.score < 20){
                alert("Password is not Strong enough")
            }else {
                $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"Username"},function(data){
                    $.post("/access_account_detail",{Username:data.item_Value},function(data){
                        $.post("/password_Update",{id:data.ID,New_password:new_Password})
                        sessionStorage.setItem("Password",new_Password)
                        alert("Password Changed")
                    })})
        
            }
        })
            } else{
        alert("Invalid Password change")
    }
}

/**
 * Saves current user settings to database
 * Includes theme preference and font size
 */
function save_setting(){
    $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"Username"},function(data){
        $.post('/access_account_detail',{Username:data.item_Value},function(data){
            const ID = data.ID

            // Determine current theme
            if (document.body.style.backgroundColor == "rgb(87, 87, 87)"){
                var Theme = "bright"
            }else {            
                var Theme = "dark"
            }

            // Get current font size or use default
            if (document.body.style.fontSize == null ||document.body.style.fontSize == ""){
                var FontSize = "18px"
            } else{
                var FontSize = document.body.style.fontSize;
            }
            $.post('/update_user_setting',{id:ID,theme:Theme,fontSize:FontSize});
        })})
}

/**
 * Loads user settings from database
 * Applies saved theme and font size preferences
 */
function access_setting(){
    check_invalid_enter()
    get_username()
    $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"Username"},function(data){
        $.post('/access_account_detail',{Username:data.item_Value},function(data){
            const ID = data.ID
            $.post('/access_user_setting',{id:ID},function(data){
                if(data.Theme != null){
                    const Theme = data.Theme
                    const FontSize = data.Fontsize
                    if (Theme == "bright"){
                        set_bright_theme()
                        document.getElementById('bright-theme').checked = true;
                    } else{
                        document.getElementById('dark-theme').checked = true;
                    }
                    document.body.style.fontSize = FontSize
                    document.getElementById("font-size").value = Number(FontSize.substring(2,-2))
                }
            })
        })
    })
}

/**
 * Initiates email change process
 * Sends verification code to new email address
 */
function send_ver_email(){
    var new_email=document.getElementById("New-email").value.toLowerCase()
    $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"Username"},function(data){
        $.post('/access_account_detail',{Username:data.item_Value},function(data){
            if (data.email.toLowerCase() == new_email.toLowerCase()){
                alert("Same Email,Invalid Request!")
            }else { 
                $.post('/email_verification',{Email:new_email},function(data){
                    const code = data.Code
                    document.getElementById("Verification-code").style.display = "flex";
                    document.getElementById("email-confirmation-button").style.display = "flex";
                    alert("Code sent!\nPlease Check email! ")
                    sessionStorage.setItem("ver_code",code)
                })
            }})
        })
}

/**
 * Verifies email change verification code
 * Updates email if code is correct
 */
function check_ver_code(){
    var ver_code = sessionStorage.getItem("ver_code")
    var user_code = document.getElementById("Verification-code").value
    if(ver_code == user_code){
        alert("Email Changed")
        var new_email=document.getElementById("New-email").value
        document.getElementById("Verification-code").style.display = "none";
        document.getElementById("email-confirmation-button").style.display = "none";
        $.post('/access_account_detail',{Username:sessionStorage.getItem("Username")},function(data){
            const ID = data.ID
            $.post("/update_user_email",{id:ID,email:new_email},function(data){
            })
    })}else{
        alert("Incorrect Code")
    }
}

function get_username(){
    $.getJSON(`/getAllusername`, function(data) {
        const username_field = document.getElementById("username-select")

        username_field.innerHTML = ""

        for (let x of data.usernames){

            var option = document.createElement("option");
            option.text = x;
            username_field.add(option);
    }})
}

function ban_user(){
    const banning_user = document.getElementById("username-select").value
    var confirm_user = prompt("Enter the username")
    if (banning_user == confirm_user){
        $.post('/banUser',{username:banning_user},function(data){
            alert(`${banning_user} is banned` )
        })
    }
}