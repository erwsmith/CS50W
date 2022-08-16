document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#filtered-posts').addEventListener('click', () => load_posts('all'));
    document.querySelectorAll('input').forEach(button => {
        button.onclick = function() {
            console.log(`${this.dataset.name} button clicked!`)
            if (this.dataset.name === "edit") {
                console.log("EDIT BUTTON")
            }
        };
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

function load_post(post) {
    fetch(`posts/${post.id}`)
    .then(response = response.json())
    .then(console.log(`${post}`));
}