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
            document.location.href = "/index";
            Username = "";
            Password = "";
            
        } else {
            alert("Incorrect Password/Username")
        }
    })


}
