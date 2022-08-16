document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input').forEach(button => {
        button.onclick = function() {
            console.log(`${this.dataset.name} button clicked!`)
        };
    });
  });


// function load_display(display) {
//     // Show create view and hide other views
//     document.querySelector('#posts-view').style.display = 'block';

//     fetch(`/posts/${display}`)
//     .then(response => response.json())
//     .then(posts => {
//         console.log(posts)
//         // posts.forEach((post) => {
//         //     const post_data = [`${post.user}`]
//         // });
//     });
// }
