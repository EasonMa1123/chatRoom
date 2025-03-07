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


function load_panel(){
    check_invalid_enter() 
    setup_admin_sql()
    setup_field_name()
}

function setup_admin_sql(){
    const table_name = document.getElementById("table-area");
    const current_table_name = document.getElementById("join-table-area");
    $.getJSON('/showdb',function(data){
        table = data.table
        table_list = table.split(",")
        for (let x of table_list){
            var option = document.createElement("option");
            option.text = x;
            table_name.add(option);
            var option = document.createElement("option");
            option.text = x;
            current_table_name.add(option);
        }
    })    
}

function setup_field_name(){
    $.getJSON('/showdb',function(data){
        const field_name = document.getElementById("field-area");
        const con_field_name = document.getElementById("con-field-area");
        field_name.innerHTML = ""
        con_field_name.innerHTML = ""
        const table_name = document.getElementById("table-area");
        var field_name_list = JSON.parse(data.field)
        for (let x of field_name_list[table_name.value]){
            var option = document.createElement("option");
            option.text = x;
            con_field_name.add(option);
            var option = document.createElement("option");
            option.text = x;
            field_name.add(option);
        }
        var option = document.createElement("option");
        option.text = "*";
        field_name.add(option);
        var option = document.createElement("option");
        option.text = "None";
        con_field_name.add(option);
    })
}

function check_invalid_enter() {
    if (sessionStorage.getItem("Username") == null) {
        alert("You must log in first!");
        window.location.href = "/";
    }
    if (window.location.href == "/admin" && sessionStorage.getItem("role") != "admin"){
        alert("Invalid Access!");
        window.location.href = "/";
    }
}

function join_table_update(){
    const join_table = document.getElementById("join-table-area")
    var join_table_display = document.getElementById("join-table")
    join_table_display.innerHTML = join_table.value
}


function toggle_join(){
    const join_sql = document.getElementById("join-SQL")
    const toggle = document.getElementById("join-SQL-toggle")
    if (toggle.checked == true){
        join_sql.style.display = "flex"
    } else {
        join_sql.style.display = "none"
    }
}