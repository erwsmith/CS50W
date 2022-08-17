document.addEventListener('DOMContentLoaded', function() {
    // document.querySelector('#all-posts').addEventListener('click', () => load_posts('all'));
    // document.querySelector('#following-posts').addEventListener('click', () => load_posts('following'));
    // document.querySelector('#profile-posts').addEventListener('click', () => load_posts('profile'));
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
    })

function load_posts(filter) {
    document.querySelector('#posts-view-js').style.display = 'block';
    fetch(`/posts/${filter}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach((post) => {
            const post_data = [`${post.id}`, `${post.username}`, `${post.body}`, `${post.timestamp}`]
        })
    })
}

function like_post(post_id, active_user_id) {
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked_by: active_user_id,
        })
    })
}

function unlike_post(post_id, active_user_id) {
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            unliked_by: active_user_id
        })
    })
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