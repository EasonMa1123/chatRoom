


function setting_on() {
    document.getElementById("overlay-setting").style.display = "block";
    menu_close();

}
  
function setting_off() {
    document.getElementById("overlay-setting").style.display = "none";
} 


function menu_open() {
    document.getElementById('sidebar').style.display = "block";
    document.getElementById('Username-display').innerHTML = sessionStorage.getItem("Username")
    if(sessionStorage.getItem("role") != "admin"){
        document.getElementById('admin-label').style.display = "none";

    }


}

function menu_close() {
    document.getElementById('sidebar').style.display = "None";
    document.getElementById('Username-display').innerHTML = ""


}




