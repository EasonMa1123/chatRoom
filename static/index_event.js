


function setting_on() {
    document.location.href = "/setting";
    menu_close();

}
  
function setting_off() {
    window.location.href = `/room/${sessionStorage.getItem("room")}`;
    
    
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




