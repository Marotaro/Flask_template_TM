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

function favorit(postId) {
    const favoritButton = document.getElementById(`favorit-button-${postId}`);

        fetch(`/post/favorit_post/${postId}`, { methods: "GET" })
            .then((res) => res.json())
            .then((data) => { console.log(data);
                if (data[0].favorited === true) {
                    favoritButton.className ="fa-solid fa-bookmark favorit-button-on";
                } else {
                    favoritButton.className ="fa-solid fa-bookmark favorit-button-off";
                }
            });
}

function showRespond(postId, idUser, idChannel, host) {
    const responds = document.getElementById(`responds-${postId}`);
    const comment = document.getElementById(`comment-${postId}`);

    if (responds.className !== 'responds visible') {
        fetch(`/y/get_comments/${postId}`)
        .then((res) => res.json())
        .then((respPosts) => { 
            console.log(respPosts.slice(-1)[0].includes(15));
            console.log(respPosts.slice(-1)); // Vérifiez si les données sont correctement récupérées
            console.log(respPosts)
            for (const respPost of respPosts.slice(0,-2)) {
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

                // création user-part-info
                var userPartInfo = document.createElement("div");
                userPartInfo.className = "user-part-info";

                    //création usericon
                    var userIcon = document.createElement('img');
                    userIcon.src = `${host}/${respPost.usericon}`
                    userPartInfo.appendChild(userIcon);

                    //création username
                    var userName = document.createElement("p");
                    userName.innerText = "@"+respPost.username;
                    userPartInfo.appendChild(userName);

                upperPart.appendChild(userPartInfo);
                
                var threePoint = document.createElement("p");
                var image = document.createElement("i");
                image.className = "fa-solid fa-ellipsis-vertical";
                image.id = "dot"
                image.onclick = function() {littlePostMenu(`${respPost.id_post}`)};
                threePoint.appendChild(image);
                upperPart.appendChild(threePoint);

                //création text
                var text = document.createElement("p");
                text.innerHTML = respPost.text

                //création partie image
                var littleCenterDiv = document.createElement('div');
                littleCenterDiv.className = "center-h"

                if (! respPost.location.includes('default.png')) {
                    var img = document.createElement('img');
                    img.src= `${respPost.location}`;
                    littleCenterDiv.appendChild(img);
                };

                //création downPart
                var downPart = document.createElement("div");
                downPart.className = "downpart";

                //création like
                var heart = document.createElement("i");
                console.log(respPost.respond_to);
                if (respPosts.slice(-2)[0].includes(respPost.id_post)) {
                    heart.className = "fa-solid fa-heart like-button-on";
                } else {
                    heart.className = "fa-regular fa-heart like-button-off";
                };
                heart.id = `like-button-${respPost.id_post}`;
                heart.onclick =function() {like(respPost.id_post)};
                downPart.appendChild(heart);


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
                    }
                    var fav = document.createElement("a");

                    var bookmark = document.createElement("i");
                    if (respPosts.slice(-1)[0].includes(respPost.id_post)) {
                        bookmark.className = "fa-solid fa-bookmark favorit-button-on";
                    } else {
                        bookmark.className = "fa-solid fa-bookmark favirt-button-off";
                    };
                    bookmark.id = `favorit-button-${respPost.id_post}`;
                    bookmark.onclick =function() {favorit(respPost.id_post)};
                    fav.appendChild(bookmark);

                    littleMenu.appendChild(fav);

                

                littlePost.appendChild(upperPart)
                littlePost.appendChild(text)
                littlePost.appendChild(littleCenterDiv)
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

//show change role
function showChangeRole(idUser, type) {
    if (type === 'admin') {
        const aRight = document.getElementById(`change-role-${idUser}-right`);
        const aLeft = document.getElementById(`change-role-${idUser}-left`);
        if (aRight.style.transform !== 'scale(1)') {
            aRight.style.transform = 'scale(1)';
            aLeft.style.transform = 'scale(1)';
            aLeft.style.opacity = '0';
        } else {
            aRight.style.transform = 'scale(0)';
            aLeft.style.transform = 'scale(0)';
            aLeft.style.opacity = '0';
        };

    } else if (type === 'ban') {
        const aRight = document.getElementById(`change-role-${idUser}-right`);
        const aLeft = document.getElementById(`change-role-${idUser}-left`);
        if (aLeft.style.transform !== 'scale(1)') {
            aLeft.style.transform = 'scale(1)';
            aRight.style.transform = 'scale(1)';
            aRight.style.opacity = '0';
        } else {
            aLeft.style.transform = 'scale(0)';
            aRight.style.transform = 'scale(0)';
            aRight.style.opacity = '0';
        };

    } else if (type === 'member') {
        const aRight = document.getElementById(`change-role-${idUser}-right`);
        const aLeft = document.getElementById(`change-role-${idUser}-left`);

        if (aRight.style.transform !== 'scale(1)') {
            aRight.style.transform = 'scale(1)';
            aLeft.style.transform = 'scale(1)';
        } else {
            aRight.style.transform = 'scale(0)';
            aLeft.style.transform = 'scale(0)';
        };
    }
    

}

//change role
function changeRole(idChannel, idUser, userName, type) {
    const oldCase = document.getElementById(`user-container-${idUser}`);
    oldCase.remove();

    if (type !== 'none') {
        fetch(`/y/change_role/${idChannel}/${idUser}/${type}`)
        .then((res) => res.json())
        .then((respmes) => {
            var newCase = document.createElement('div');
            newCase.className = 'user-container';
            newCase.id = `user-container-${idUser}`;

            if (type === 'member'){
                const newBox = document.getElementById('member-box');
                
                var aLeft = document.createElement('a');
                aLeft.className = 'change-role';
                aLeft.id = `change-role-${idUser}-left`;
                aLeft.onclick = function() {changeRole(idChannel, idUser, userName, 'admin')};
    
                var iLeft = document.createElement('i');
                iLeft.className = 'fa-solid fa-star-of-life';
                iLeft.id = 'admin';
    
                aLeft.appendChild(iLeft);
    
                var p = document.createElement('p');
                p.onclick = function() {showChangeRole(idUser, type)};
                p.innerText = "@" + userName;
    
                var aRight = document.createElement('a');
                aRight.className = 'change-role';
                aRight.id = `change-role-${idUser}-right`;
                aRight.onclick =function() {changeRole(idChannel, idUser, userName, 'ban')};
    
                var iRight = document.createElement('i');
                iRight.className = 'fa-solid fa-door-closed';
                iRight.id = 'ban';
    
                aRight.appendChild(iRight);
    
                newCase.appendChild(aLeft);
                newCase.appendChild(p);
                newCase.appendChild(aRight);
    
                newBox.appendChild(newCase);


            } else if (type === 'admin') {

                const newBox = document.getElementById('admin-box');

                var aLeft = document.createElement('a');
                aLeft.className = 'change-role';
                aLeft.id = `change-role-${idUser}-left`;

                var p = document.createElement('p');
                p.onclick = function() {showChangeRole(idUser, type)};
                p.innerText = "@" + userName;

                var aRight = document.createElement('a');
                aRight.className = 'change-role';
                aRight.id = `change-role-${idUser}-right`;
                aRight.onclick =function() {changeRole(idChannel, idUser, userName, 'member')};

                var iRight = document.createElement('i');
                iRight.className = 'fa-solid fa-user';
                iRight.id = 'member';

                aRight.appendChild(iRight);
                newCase.appendChild(aLeft);
                newCase.appendChild(p);
                newCase.appendChild(aRight);



                newBox.appendChild(newCase)
            } else if (type === 'ban') {

                const newBox = document.getElementById('ban-box');

                var aLeft = document.createElement('a');
                aLeft.className = 'change-role';
                aLeft.id = `change-role-${idUser}-left`;
                aLeft.onclick =function() {changeRole(idChannel, idUser, userName, 'member')};

                var iLeft = document.createElement('i');
                iLeft.className = 'fa-solid fa-user';
                iLeft.id = 'member';

                var p = document.createElement('p');
                p.onclick = function() {showChangeRole(idUser, type)};
                p.innerText = "@" + userName;

                var aRight = document.createElement('a');
                aRight.className = 'change-role';
                aRight.id = `change-role-${idUser}-right`;




                aLeft.appendChild(iLeft);
                newCase.appendChild(aLeft);
                newCase.appendChild(p);
                newCase.appendChild(aRight);



                newBox.appendChild(newCase)
            };

            
        });
    }
}


function showInvite(idChannel) {
    var inviteOverlay = document.getElementById("invite-overlay");
    if (inviteOverlay.style.transform !== "scale(1)") {
        inviteOverlay.style.transform = "scale(1)"
    } else {
        inviteOverlay.style.transform = "scale(0)";
        inviteOverlay.style.width = '20vw'

        var inviteOverlay = document.getElementById('invite-overlay');
        inviteOverlay.innerHTML = '';

        var timeButton = document.createElement('button');
        timeButton.id = 'time-button';
        timeButton.value = '10';
        timeButton.onclick = function() {var button = document.getElementById('time-button'); if (button.value === '10') { button.innerText = '30 Minutes'; button.value = '30' } else if ( button.value === '30' ) { button.innerText = '60 Minutes'; button.value =  '60'} else { button.innerText = '10 Minutes' ; button.value = '10' };};
        timeButton.innerText = '10 Minutes';
        
        var createInvite = document.createElement('button');
        createInvite.id = 'create-invite'
        createInvite.onclick = function() {createInviteLink(idChannel)};
        createInvite.innerText = 'Créer un lien'

        inviteOverlay.appendChild(timeButton);
        inviteOverlay.appendChild(createInvite);

    }
}

function createInviteLink(idChannel) {
    var button = document.getElementById('time-button');
        fetch(`/y/invite/${idChannel}/${button.value}`)
        .then((res) => res.json())
        .then((respmes) => {
            var inviteOverlay = document.getElementById('invite-overlay');
            inviteOverlay.innerHTML = '';

            var p = document.createElement('p');
            p.id = 'created-link'
            p.innerText = `${respmes.respond}`;

            inviteOverlay.appendChild(p);
            inviteOverlay.style.width = "fit-content"
            inviteOverlay.onclick = function() {copy_to_clipboard(`${respmes.respond}`, idChannel)};

        });
}


function copy_to_clipboard(text, idChannel) {
    navigator.clipboard.writeText(text);
    var inviteOverlay = document.getElementById('invite-overlay');
    inviteOverlay.innerText = 'lien copié';
    inviteOverlay.onclick = ""
    setTimeout( function() {showInvite(idChannel)}, 2000);
}


function search(host,text) {
    var result = document.getElementById('result');
    result.innerHTML = '';
    var sousTite = document.createElement('h3');
    sousTite.innerText = "Résultats"
    var centerH = document.createElement('div');
    centerH.className = 'center-h';
    var listY = document.createElement('div');
    listY.className = 'list-y';
    centerH.appendChild(listY);
    result.appendChild(sousTite);
    result.appendChild(centerH);

    fetch(`/y/search/${text}`)
    .then((res) => res.json())
    .then((respmes) => {
        console.log(respmes)

        if ( respmes[1] === true) {
            //création message retour
            var message = document.createElement('p');
            message.innerText = 'Aucun résultat';
            listY.appendChild(message);
        } else {
            for (const respme of respmes[0]) {
                //création a
                var a = document.createElement('a');
                a.href = `${host}/y/see/${respme.idChannel}`;

                //création div
                var channelBulb = document.createElement('div');
                channelBulb.className = "channel-bulb";

                //création img
                var img = document.createElement('img');
                img.src = `${host}/${respme.location}`;

                //création p
                var p = document.createElement('p');
                p.innerText = respme.name;

                channelBulb.appendChild(img);
                channelBulb.appendChild(p);

                a.appendChild(channelBulb);

                listY.appendChild(a);
            }}

    });
}




function inputSearch(host) {
    var searchText = document.getElementById('search-text');
    if ( searchText.value !== '') { text = encodeURIComponent(searchText.value);} else { text = '|empty|' };
    console.log(text);
    search(host,text);

}

function themesSearch(host, idTheme) {
    var theme = document.getElementById(`theme-${idTheme}`);
    console.log(theme)
    text = encodeURIComponent(theme.innerText);
    search(host,text);
}