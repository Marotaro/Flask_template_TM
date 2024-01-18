function menu() {
    var hiddenButtons = document.getElementById('hiddenButtons');
    if (hiddenButtons.style.display === "none") {
        hiddenButtons.style.display = "flex";
    }
    else{
        hiddenButtons.style.display = "none";
    }
}

function copy_to_clipboard(text,alert) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = "absolute";
    textarea.style.display = "none";
    document.body.appendChild(textarea);
    textarea.select();
    navigator.clipboard.writeText(textarea.value);
    alert(alert);
}