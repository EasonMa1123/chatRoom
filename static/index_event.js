


function setting_on() {
    document.location.href = "/setting";
    menu_close();

}
  
function setting_off() {
    $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"room"},function(data){
        window.location.href = `/room/${data.item_Value}`;
    })
    
    
} 


function menu_open() {
    document.getElementById('sidebar').style.width = "250px";
    $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"Username"},function(data){
        document.getElementById('Username-display').innerHTML = data.item_Value
        $.post('/access_session_data',{Session_ID:sessionStorage.getItem("Session_ID"),Item_Name:"role"},function(data){
            if(data.item_Value != "admin"){
                document.getElementById('admin-label').style.display = "none";

            }})
    })
}

function menu_close() {
    document.getElementById('sidebar').style.width = "0";
    document.getElementById('Username-display').innerHTML = ""


}




