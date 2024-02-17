function menu() {
    var buttonsContainer = document.getElementById('buttons-container')
    if (buttonsContainer.style.transform !== "scaleY(1)") {
        buttonsContainer.style.transform = "scaleY(1)";
        buttonsContainer.style.display = "flex";
        buttonsContainer.style.top = "1vh";
    } else {
        buttonsContainer.style.transform = "scaleY(0)";
        buttonsContainer.style.display = "flex";
        buttonsContainer.style.top = "-2vh";
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

function showRespond(postId) {
    const responds = document.getElementById(`responds-${postId}`);
    const comment = document.getElementById(`comment-${postId}`);

    if (responds.className !== 'responds visible') {
        fetch(`/y/get_comments/${postId}`)
        .then((res) => res.json())
        .then((respPosts) => { 
            console.log(respPosts.slice(-1)[0].includes(15));
            console.log(respPosts.slice(-1)); // Vérifiez si les données sont correctement récupérées
            for (const respPost of respPosts.slice(0,-1)) {
                //création center div
                var CenterDiv = document.createElement("div");
                CenterDiv.className = "center-h";

                //création  little post
                var littlePost = document.createElement("div");
                littlePost.className = "little-post";
                
                //création upper part
                var upperPart = document.createElement("div");
                upperPart.className = "upperpart";

                //création username
                var userName = document.createElement("p");
                userName.innerText = "@"+respPost.username;
                upperPart.appendChild(userName);

                var threePoint = document.createElement("p");
                var image = document.createElement("img");
                image.src = "http://127.0.0.1:5000/static/image/buttons/threepoint.svg";
                image.onclick = function() {menu('flex',"threepoint")};
                threePoint.appendChild(image);
                upperPart.appendChild(threePoint);

                //création text
                var text = document.createElement("p");
                text.innerText = respPost.text

                //création downPart
                var downPart = document.createElement("div");
                downPart.className = "downpart";

                //création like
                var heart = document.createElement("i");
                console.log(respPost.respond_to);
                if (respPosts.slice(-1)[0].includes(respPost.id_post)) {
                    heart.className = "fa-solid fa-heart like-button-on";
                } else {
                    heart.className = "fa-regular fa-heart like-button-off";
                };
                heart.id = `like-button-${respPost.id_post}`;
                heart.onclick =function() {like(respPost.id_post)};
                downPart.appendChild(heart);

                //création share
                var share = document.createElement("i");
                share.className = "fa-regular fa-share-from-square";
                downPart.appendChild(share);

                littlePost.appendChild(upperPart)
                littlePost.appendChild(text)
                littlePost.appendChild(downPart)
                CenterDiv.appendChild(littlePost)
                responds.appendChild(CenterDiv)
            }
            responds.className = 'responds visible'; 
            comment.className = "fa-solid fa-comment comment-button-on";
        });
    } else {
        responds.innerHTML = '';
        responds.className = 'responds hidden'; 
        comment.className = "fa-regular fa-comment comment-button-off";
    }

}


//resize textarea
textarea = document.querySelector(".post-textarea#text");
textarea.addEventlistener('input', autoResize, false);

function autoResize(){
    this.style.height = 'auto'
    this.style.height = this.scrollHeight + '5px'
}