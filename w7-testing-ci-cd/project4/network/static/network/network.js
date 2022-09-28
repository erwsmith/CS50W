document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#all-posts').addEventListener('click', () => load_posts('all'));
    document.querySelector('#following-posts').addEventListener('click', () => load_posts('following'));
    document.querySelector('#profile-posts').addEventListener('click', () => load_posts('profile'));
    document.querySelectorAll('input').forEach(button => {
        button.onclick = function() {
            post_id = this.dataset.postid
            active_user_id = this.dataset.active_user_id
            button_name = this.dataset.name
            if (button_name === "edit") {
                console.log(`${button_name} button ${post_id} clicked!`)
                // edit_post(post_id, active_user_id)
            } else if (button_name === "like") {
                console.log(`${button_name} button ${post_id} clicked!`)
                // like_post(post_id, active_user_id)
            } else if (button_name === "unlike") {
                console.log(`${button_name} button ${post_id} clicked!`)
                // unlike_post(post_id, active_user_id)
            }
        }
    })
    load_posts('all');
})


function load_posts(post_view) {
    let view_name = ''
    if (post_view === 'all') {
        view_name = "All Posts";
    } else if (post_view === 'following') {
        view_name = "Following View";
    } else if (post_view === 'profile') {
        view_name = "Profile View";
    } else {
        console.log("Error: Invalid Post View")
        view_name = "All Posts";
    }
    document.querySelector('#posts-view-head').innerHTML = `<h3>${view_name}</h3>`;
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#posts-view').innerHTML = '';
    fetch(`/posts/${post_view}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach((element) => {
            let post = document.createElement("div");
            post.innerHTML = `<button class="btn btn-link my-0">${element.username}</button>
            <button data-name="edit" class="btn btn-sm btn-outline-dark rounded mx-2 px-3">Edit</button>
            <hr>
            <p>${element.body}</p>
            <p class="mb-2 text-muted">${element.timestamp}</p>
            <button data-name="like" class="btn btn-sm btn-outline-dark rounded mx-2 px-3">Like</button>
            <span class="margin">${element.likes_count} likes</span>`
            post.className = "post_cell";
            document.querySelector('#posts-view').appendChild(post)
            
            const like_button = document.createElement('button');
            like_button.innerHTML = "Like";
            like_button.id = "like";
            like_button.className = "btn btn-sm btn-outline-primary";
            document.querySelector('#posts-view').append(like_button);
            like_button.addEventListener('click', function() {
                console.log("Like button clicked!")
            });
        });
    });
}


function load_profile(username) {
    document.querySelector('#posts-view').innerHTML = '';
    document.querySelector('#posts-view').style.display = 'block';
    fetch(`/profile/${username}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach((element) => {
            let post = document.createElement("div");
            post.innerHTML = 
            `<button class="btn btn-link user-link">${element.username}</button>
            <button class="btn btn-outline-info edit">Edit</button>
            <hr>
            <p>${element.body}</p>
            <p class= "mb-2 text-muted">${element.timestamp}</p>
            <button class="btn like">Like</button>
            <span class="margin">${element.likes_count} likes</span>`
            document.querySelector('#posts-view').append(post)
            post.id = element.id
            });
    });
}


// function like_button(post_id, active_user_id) {
//     fetch(`/posts/${post_id}`)
//     .then(response => response.json())
//     .then(console.log(response))
//     // if post.liked_by.filter(id=active_user.id).exists()
//     }


function like_post(post_id, active_user_id) {
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked_by: active_user_id,
        })
    })
    .then(function () {fetch(`/posts/${post_id}`)
        .then(response => response.json())
        .then(post => {
            console.log(post.likes_count);
            document.querySelector('#likes-count').innerHTML = `${post.likes_count}`;
        })})
}


function unlike_post(post_id, active_user_id) {
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            unliked_by: active_user_id
        })
    })
    .then(function () {fetch(`/posts/${post_id}`)
        .then(response => response.json())
        .then(post => {
            console.log(post.likes_count);
            document.querySelector('#likes-count').innerHTML = `${post.likes_count}`;
        })})
}


function edit_post(post_id, active_user_id) {
    fetch(`/posts/${post_id}`)
    .then(response => response.json())
    .then(post => {
        // TODO
        const post_data = [`${post.id}`, `${post.username}`, `${post.body}`, `${post.timestamp}`]
        console.log(post_data, active_user_id)
    })
}