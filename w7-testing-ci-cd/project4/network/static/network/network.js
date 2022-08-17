document.addEventListener('DOMContentLoaded', function() {
    // document.querySelector('#all-posts').addEventListener('click', () => load_posts('all'));
    // document.querySelector('#following-posts').addEventListener('click', () => load_posts('following'));
    // document.querySelector('#profile-posts').addEventListener('click', () => load_posts('profile'));
    document.querySelectorAll('input').forEach(button => {
        button.onclick = function() {
                post_id = this.dataset.postid
                button_name = this.dataset.name
                if (button_name === "edit") {
                    edit_post(post_id)
                } else if (button_name === "like") {
                    console.log(`${button_name} button ${post_id} clicked!`)
                    like_post(post_id)
                } else if (button_name === "unlike") {
                    console.log(`${button_name} button ${post_id} clicked!`)
                    unlike_post(post_id)
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

function like_post(post_id) {
    fetch(`posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked: true // this isn't correct
        })
    })
}

function unlike_post(post_id) {
    fetch(`posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked: false // this isn't correct
        })
    })
}

function edit_post(post_id) {
    fetch(`posts/${post_id}`)
    .then(response => response.json())
    .then(post => {
        const post_data = [`${post.id}`, `${post.username}`, `${post.body}`, `${post.timestamp}`]
        console.log(post_data)
    })
}