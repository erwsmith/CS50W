document.addEventListener('DOMContentLoaded', function() {
    // document.querySelector('#all-posts').addEventListener('click', () => load_posts('all'));
    // document.querySelector('#following-posts').addEventListener('click', () => load_posts('following'));
    // document.querySelector('#profile-posts').addEventListener('click', () => load_posts('profile'));
    document.querySelectorAll('input').forEach(button => {
        button.onclick = function() {
                console.log(`${this.dataset.name} button ${this.dataset.postid} clicked!`);
                const post_id = parseInt(this.dataset.postid);
                load_post(post_id);
            }
        });
    });

function load_posts(filter) {
    // Show create view and hide other views
    document.querySelector('#posts-view-js').style.display = 'block';
    fetch(`/posts/${filter}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach((post) => {
            const post_data = [`${post.id}`, `${post.username}`, `${post.body}`, `${post.timestamp}`]
        });
    });
}

function load_post(post_id) {
    fetch(`posts/${post_id}`)
    .then(response => response.json())
    .then(post => {
        const post_data = [`${post.id}`, `${post.username}`, `${post.body}`, `${post.timestamp}`];
        console.log(post_data);
    });
}