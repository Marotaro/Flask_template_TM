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

function like(postId) {
    const likeButton = document.getElementById(`like-button-${postId}`);

        fetch(`/post/like_post/${postId}`, { methods: "GET" })
            .then((res) => res.json())
            .then((data) => { console.log(data);
                if (data[0].liked === true) {
                    likeButton.className ="fa-solid fa-heart like-button-on";
                } else {
                    likeButton.className ="fa-regular fa-heart like-button-off";
                }
            });
}