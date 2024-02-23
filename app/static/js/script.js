function menu() {
    var buttonsContainer = document.getElementById('buttons-container')
    if (buttonsContainer.style.transform !== "scale(1)") {
        buttonsContainer.style.transform = "scale(1)";
        buttonsContainer.style.display = "flex";
        buttonsContainer.style.top = "1vh";
    } else {
        buttonsContainer.style.transform = "scale(0)";
        buttonsContainer.style.display = "flex";
        buttonsContainer.style.top = "-2vh";
    }
    
}

function postMenu(idPost) {
    var menu = document.getElementById(`post-menu-${idPost}`);
    if (menu.style.transform !== "scale(1)") {
        menu.style.transform = "scale(1)";
    } else {
        menu.style.transform = "scale(0)";
    }
}

function littlePostMenu(idPost) {
    var menu = document.getElementById(`little-post-menu-${idPost}`);
    if (menu.style.transform !== "scale(1)") {
        menu.style.transform = "scale(1)";
    } else {
        menu.style.transform = "scale(0)";
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

function showRespond(postId, idUser, idChannel) {
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

                //création little test
                var littleTest = document.createElement("div");
                littleTest.id = "little-test";

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
                image.onclick = function() {littlePostMenu(`${respPost.id_post}`)};
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


                //création overlay elements
                var littleMenu = document.createElement("div");
                littleMenu.className = "little-post-menu";
                littleMenu.id = `little-post-menu-${respPost.id_post}`;

                    //création element
                    if (respPost.id_user === idUser) {
                        var deleteButton = document.createElement("a");
                        deleteButton.href = `/post/delete_post_from_channel/${idChannel}/${respPost.id_post}`;

                        var trashIcon = document.createElement('i');
                        trashIcon.className = "fa-solid fa-trash";
                        deleteButton.appendChild(trashIcon);

                        var modifyButton = document.createElement("a");
                        modifyButton.href = `/post/modify_post_from_channel/${idChannel}/${respPost.id_post}`;

                        var modifyIcon = document.createElement('i');
                        modifyIcon.className = "fa-solid fa-pen-to-square";
                        modifyButton.appendChild(modifyIcon);

                        littleMenu.appendChild(modifyButton);
                        littleMenu.appendChild(deleteButton);
                    } else {
                        var nothing = document.createElement("a");
                        nothing.onclick = function() {littlePostMenu(`${respPost.id_post}`)};

                        var xmark = document.createElement('i');
                        xmark.className = "fa-solid fa-xmark";
                        nothing.appendChild(xmark);

                        littleMenu.appendChild(nothing);
                    };
                

                littlePost.appendChild(upperPart)
                littlePost.appendChild(text)
                littlePost.appendChild(downPart)
                littleTest.appendChild(littlePost)
                littleTest.appendChild(littleMenu)
                CenterDiv.appendChild(littleTest)
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

//delete Post from user page
function deletePost(postId){
    fetch(`/post/delete_post/${postId}`)
    .then((res) => res.json())
    .then((respmes) => {
        var post = document.getElementById(`post-${postId}`);
        post.innerHTML = "";
    }); 
}