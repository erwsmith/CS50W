document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#edit-button").addEventListener('click', () => {
        console.log(`edit button clicked!`)
    });
    document.querySelector("#like-button").addEventListener('click', () => {
        console.log(`like button clicked!`)
    });
    document.querySelector("#unlike-button").addEventListener('click', () => {
        console.log(`unlike button clicked!`)
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
