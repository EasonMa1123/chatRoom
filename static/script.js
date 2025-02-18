



// index.html

function check_invalid_enter(){
    if(sessionStorage.getItem("Username") == null){
        alert("What are you doing in here,this is not your place,leave! Thank You :)")
        logout()
    }
}






function logout(){
    document.location.href = "/";
    sessionStorage.setItem("",Username)
    sessionStorage.setItem("",Password)
}
