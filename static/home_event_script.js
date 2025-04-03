
function check_user_role(){
    if (sessionStorage.getItem("role") == "admin"){
        document.getElementById("lobby-admin-portal").style.display = "block"
    } else {
        document.getElementById("lobby-admin-portal").style.display = "none" 
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

    current_table_name.remove(table_name.value)
    })    
}


function update_join_table_name(){
    const table_name = document.getElementById("table-area");
    const current_table_name = document.getElementById("join-table-area");
    current_table_name.innerHTML = ""
    $.getJSON('/showdb',function(data){
        table = data.table
        table_list = table.split(",")
        for (let x of table_list){
            var option = document.createElement("option");
            option.text = x;
            current_table_name.add(option);
        }

    current_table_name.remove(table_name.selectedIndex)
    const join_table = document.getElementById("join-table-area")
    var join_table_display = document.getElementById("join-table")
    join_table_display.innerHTML = join_table.value
    
    })    
}

function setup_field_name(){
    $.getJSON('/showdb',function(data){
        const field_name = document.getElementById("field-area");
        const con_field_name = document.getElementById("con-field-area");
        const table_name = document.getElementById("table-area");
        const join_current_field_name = document.getElementById("current-field-area");

        field_name.innerHTML = ""
        con_field_name.innerHTML = ""
        join_current_field_name.innerHTML = ""


        var field_name_list = JSON.parse(data.field)

        for (let x of field_name_list[table_name.value]){

            var option = document.createElement("option");
            option.text = x;
            con_field_name.add(option);

            var option = document.createElement("option");
            option.text = x;
            field_name.add(option);

            var option = document.createElement("option");
            option.text = x;
            join_current_field_name.add(option);
        }

        var option = document.createElement("option");
        option.text = "*";
        field_name.add(option);

        var option = document.createElement("option");
        option.text = "None";
        con_field_name.add(option);

        document.getElementById("current-table").innerHTML = ` ${table_name.value}. `

        update_join_table_name()
        join_table_update()
    })
}

function check_invalid_enter() {
    if (sessionStorage.getItem("Username") == null || sessionStorage.getItem("Username") == "") {
        alert("You must log in first!");
        window.location.href = "/";
    }

    if (window.location.href.includes("/admin") && sessionStorage.getItem("role") != "admin"){
        alert("Invalid Access!");
        window.location.href = "/";
    }
}

function join_table_update(){
    
    const join_table = document.getElementById("join-table-area")
    var join_table_display = document.getElementById("join-table")

    join_table_display.innerHTML = ` ${join_table.value}. `
    
    const join_field = document.getElementById("join-field-area")
    join_field.innerHTML = ""


    $.getJSON('/showdb',function(data){
        var field_name_list = JSON.parse(data.field)
        for (let x of field_name_list[join_table.value]){
            var option = document.createElement("option");
            option.text = x;
            join_field.add(option);
        }
    if (document.getElementById("join-SQL-toggle").checked == true){
        join_select_update()
    }
    
    })

}


function toggle_join(){
    const join_sql = document.getElementsByClassName("join-SQL")
    const toggle = document.getElementById("join-SQL-toggle")
    for (let i = 0; i < join_sql.length; i++) {
        
      
        if (toggle.checked == true){
            join_sql[i].style.display = "flex"
            join_select_update()
        } else {
            join_sql[i].style.display = "none"
            setup_field_name()
        }
    }
}


function join_select_update(){
    $.getJSON('/showdb',function(data){
        const field_name = document.getElementById("field-area")
        field_name.innerHTML = ""
        const origianl_table = document.getElementById("table-area")
        const connect_table = document.getElementById("join-table-area")
        var field_name_list = JSON.parse(data.field)
        for (let x of field_name_list[origianl_table.value]){
            var option = document.createElement("option");
            option.text = `${origianl_table.value}.${x}`;
            field_name.add(option);
        }
        for (let x of field_name_list[connect_table.value]){
            var option = document.createElement("option");
            option.text = `${connect_table.value}.${x}`;
            field_name.add(option);
        }
        var option = document.createElement("option");
        option.text = "*";
        field_name.add(option);

    })
}
