


function setting_on() {
    document.location.href = "/setting";
    menu_close();

}
  
function setting_off() {
    window.location.href = `/room/${sessionStorage.getItem("room")}`;
    
    
} 


function menu_open() {
    document.getElementById('sidebar').style.width = "250px";
    document.getElementById('Username-display').innerHTML = sessionStorage.getItem("Username")
    if(sessionStorage.getItem("role") != "admin"){
        document.getElementById('admin-label').style.display = "none";

    }
}

function menu_close() {
    document.getElementById('sidebar').style.width = "0";
    document.getElementById('Username-display').innerHTML = ""


}




