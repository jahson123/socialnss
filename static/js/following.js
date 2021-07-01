function openNav() {
    document.getElementById("slide-box").style.width = "300px";
    document.getElementById("side-users").classList.add("active");
}

function closeNav() {
    document.getElementById("slide-box").style.width = "0";
    document.getElementById("side-users").classList.remove("active")
}