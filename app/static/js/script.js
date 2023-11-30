function menu() {
    var hiddenButtons = document.getElementById('hiddenButtons');
    if (hiddenButtons.style.display === "none") {
        hiddenButtons.style.display = "flex";
    }
    else{
        hiddenButtons.style.display = "none";
    }
}