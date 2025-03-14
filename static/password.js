const Password_input = document.getElementById("signup-Password");
const comfirmPassword_input = document.getElementById("ConfirmPassword");


Password_input.onkeyup = function(){
    
    const Password_input_value = document.getElementById('signup-Password').value;
    var password_warning_1 = document.getElementById("Password-warning-1");
    var password_warning_2 = document.getElementById("Password-warning-2");


    if (Password_input_value.length <8 ){
        password_warning_1.innerHTML = "Password must longer than 7";
    } 
    if(Password_input_value.length >= 8){
        password_warning_1.innerHTML = "";
    } else if (Password_input_value.length > 40){
        password_warning_1.innerHTML = "Too long!";
    }
    $.post('/password_strength',{Password:Password_input_value},function(data){
        if (data.score < 20){
            password_warning_2.innerHTML = "Password is not strong enough"
        } else{
            password_warning_2.innerHTML = ""
        }
    })
}

comfirmPassword_input.onkeyup = function(){
    var Password = document.getElementById('signup-Password').value;
    var comfirmPassword_input_value = comfirmPassword_input.value;
    var comfirmPassword_input_warning = document.getElementById('ConfirmPassword-warning');
    if (comfirmPassword_input_value.length>(Password.length/2)){
        if (comfirmPassword_input_value != Password){
            
            comfirmPassword_input_warning.innerHTML = "Incorrect comfirming password";
        } else {
            comfirmPassword_input_warning.innerHTML = "";
        }
    }
}