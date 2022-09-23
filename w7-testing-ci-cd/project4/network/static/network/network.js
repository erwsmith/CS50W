document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#all-posts').addEventListener('click', () => load_posts(1));
    document.querySelector('#following-posts').addEventListener('click', () => load_posts(2));
    document.querySelector('#profile-posts').addEventListener('click', () => load_posts(3));
    document.querySelectorAll('input').forEach(button => {
        button.onclick = function() {
            post_id = this.dataset.postid
            active_user_id = this.dataset.active_user_id
            button_name = this.dataset.name
            if (button_name === "edit") {
                edit_post(post_id, active_user_id)
            } else if (button_name === "like") {
                console.log(`${button_name} button ${post_id} clicked!`)
                like_post(post_id, active_user_id)
            } else if (button_name === "unlike") {
                console.log(`${button_name} button ${post_id} clicked!`)
                unlike_post(post_id, active_user_id)
            }
        }
    })
    load_posts(1);
})


function load_posts(post_view) {
    document.querySelector('#grid').innerHTML = '';
    document.querySelector('#posts-view').style.display = 'block';
    fetch(`/posts/${post_view}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach((post) => {
            const post_data = [`${post.username}`, `${post.body}`, `${post.timestamp}`]
            const grid = document.getElementById("grid");
            for (let a of post_data) { 
                let cell = document.createElement("div");
                cell.innerHTML = a;
                cell.addEventListener('click', function() {
                    load_profile(post.username);
                  });
                grid.appendChild(cell);
            }
        });
    });
}

function load_profile(username) {
    document.querySelector('#grid').innerHTML = '';
    document.querySelector('#posts-view').style.display = 'block';
    fetch(`/posts/${username}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach((post) => {
            const post_data = [`${post.username}`, `${post.body}`, `${post.timestamp}`]
            const grid = document.getElementById("grid");
            for (let a of post_data) { 
                let cell = document.createElement("div");
                cell.innerHTML = a;
                grid.appendChild(cell);
            }
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