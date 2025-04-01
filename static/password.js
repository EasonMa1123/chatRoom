/*
Password Validation Script
This script handles password validation and strength checking during user registration.
It provides real-time feedback on password requirements and strength.
*/

// Get references to password input fields
const Password_input = document.getElementById("signup-Password");
const comfirmPassword_input = document.getElementById("ConfirmPassword");

/**
 * Calculates password strength score based on various criteria
 * @param {string} password - The password to evaluate
 * @returns {number} - A score between 0 and 100 indicating password strength
 */
function password_strength(password) {
    let score = 0;
    
    // Length check (0-20 points)
    if (len(password) >= 8) score += 10;
    if (len(password) >= 12) score += 10;
    
    // Character type checks (0-40 points)
    if (/[a-z]/.test(password)) score += 10;
    if (/[A-Z]/.test(password)) score += 10;
    if (/[0-9]/.test(password)) score += 10;
    if (/[^a-zA-Z0-9]/.test(password)) score += 10;
    
    // Complexity checks (0-40 points)
    if (password !== password.toLowerCase()) score += 10;
    if (password !== password.toUpperCase()) score += 10;
    if (/\d/.test(password)) score += 10;
    if (/[^a-zA-Z0-9]/.test(password)) score += 10;
    
    return score;
}

/**
 * Handles real-time password validation as user types
 * Checks password length and strength
 */
Password_input.onkeyup = function(){
    const Password_input_value = document.getElementById('signup-Password').value;
    var password_warning_1 = document.getElementById("Password-warning-1");
    var password_warning_2 = document.getElementById("Password-warning-2");

    // Check password length requirements
    if (Password_input_value.length <8 ){
        password_warning_1.innerHTML = "Password must longer than 7";
    } 
    if(Password_input_value.length >= 8){
        password_warning_1.innerHTML = "";
    } else if (Password_input_value.length > 40){
        password_warning_1.innerHTML = "Too long!";
    }

    // Check password strength using client-side validation
    const strength = password_strength(Password_input_value);
    if (strength < 20){
        password_warning_2.innerHTML = "Password is not strong enough"
    } else{
        password_warning_2.innerHTML = ""
    }
}

/**
 * Handles real-time password confirmation validation
 * Checks if confirmation matches the original password
 */
comfirmPassword_input.onkeyup = function(){
    var Password = document.getElementById('signup-Password').value;
    var comfirmPassword_input_value = comfirmPassword_input.value;
    var comfirmPassword_input_warning = document.getElementById('ConfirmPassword-warning');
    
    // Only check if confirmation is at least half the length of the password
    if (comfirmPassword_input_value.length>(Password.length/2)){
        if (comfirmPassword_input_value != Password){
            comfirmPassword_input_warning.innerHTML = "Incorrect comfirming password";
        } else {
            comfirmPassword_input_warning.innerHTML = "";
        }
    }
}