document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#all-posts').addEventListener('click', () => load_posts('all'));
    document.querySelector('#following-posts').addEventListener('click', () => load_posts('following'));
    document.querySelector('#profile-posts').addEventListener('click', () => load_posts('profile'));
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
    
    let au = document.querySelector('#active_user_id')
    let active_user_id = au.dataset.active_user_id
    

    fetch(`/posts/${post_view}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach((post) => {
            
            let post_username = document.createElement('button')
            post_username.innerHTML = `${post.username}`
            post_username.id = "post_username"
            post_username.className = "btn btn-link m-0 p-0"
            post_username.addEventListener('click', function() {
                load_profile(post.username)
            });
            
            let post_body = document.createElement('div')
            post_body.className = "m-2"
            post_body.innerHTML = `${post.body}`
            
            let post_timestamp = document.createElement('div')
            post_timestamp.className = "text-muted m-2"
            post_timestamp.innerHTML = `${post.timestamp}`
            
            let edit_button = document.createElement('button');
            if (post.user_id === parseInt(active_user_id)) {
                edit_button.innerHTML = "Edit";
                edit_button.id = "edit";
                edit_button.className = "btn btn-sm btn-outline-dark mx-2 px-3";
                edit_button.addEventListener('click', function() {
                    console.log(`Edit button ${post.id} clicked!`)
                });
            } else {
                edit_button.style.display = "none";
            }

            let likes_count = document.createElement('span')
            likes_count.className = "mx-2"
            likes_count.innerHTML = `${post.likes_count}`

            let like_button = document.createElement('button');
            like_button.innerHTML = "Like";
            like_button.id = "like";
            like_button.className = "btn btn-sm btn-outline-dark mx-2 px-3";
            like_button.addEventListener('click', function() {
                like_post(post.id, active_user_id, post_view)
            })

            document.querySelector('#posts-view').append(
                document.createElement('hr'), 
                post_username, 
                post_body, 
                post_timestamp, 
                edit_button, 
                like_button, 
                likes_count, 
                )
        });
    });
}

function load_profile(username) {
    document.querySelector('#posts-view-head').innerHTML = `<h3>${username}'s Profile</h3>`;
    document.querySelector('#posts-view').innerHTML = '';
    document.querySelector('#posts-view').style.display = 'block';
    fetch(`/profile/${username}`)
    .then(response => response.json())
    .then(posts => {
        posts.forEach((post) => {
            let post_username = document.createElement('div')
            post_username.innerHTML = `${post.username}`
            post_username.id = "post_username"
            post_username.className = "m-0 p-0"
            
            let post_body = document.createElement('div')
            post_body.className = "m-2"
            post_body.innerHTML = `${post.body}`
            
            let post_timestamp = document.createElement('div')
            post_timestamp.className = "text-muted m-2"
            post_timestamp.innerHTML = `${post.timestamp}`
            
            let edit_button = document.createElement('button');
            if (post.user_id === parseInt(active_user_id)) {
                edit_button.innerHTML = "Edit";
                edit_button.id = "edit";
                edit_button.className = "btn btn-sm btn-outline-dark mx-2 px-3";
                edit_button.addEventListener('click', function() {
                    console.log(`Edit button ${post.id} clicked!`)
                });
            } else {
                edit_button.style.display = "none";
            }

            let likes_count = document.createElement('span')
            likes_count.className = "mx-2"
            likes_count.innerHTML = `${post.likes_count}`

            let like_button = document.createElement('button');
            like_button.innerHTML = "Like";
            like_button.id = "like_button";
            like_button.className = "btn btn-sm btn-outline-dark mx-2 px-3";
            like_button.addEventListener('click', function() {
                like_post(post.id, active_user_id, post_view)
                document.querySelector('#likes_count').innerHTML = `${post.likes_count}`
            });

            document.querySelector('#posts-view').append(
                document.createElement('hr'), 
                post_username, 
                post_body, 
                post_timestamp, 
                edit_button, 
                like_button, 
                likes_count, 
                )
            });
    });
}


function like_post(post_id, active_user_id, post_view) {
    fetch(`/like_post/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked_by: active_user_id,
        })
    })
    // .then(function() {load_posts(post_view);});
    .then(function() {document.location.reload()});
    // .then(function () {
    //     fetch(`/like_post/${post_id}`)
    //     .then(response => response.json())
    //     .then(post => {
    //         console.log(`Post ${post_id} liked by user ${active_user_id}, now has ${post.likes_count} likes.`);
    //     })
    // })
}


// function like_button(post_id, active_user_id) {
//     fetch(`/posts/${post_id}`)
//     .then(response => response.json())
//     .then(console.log(response))
//     // if post.liked_by.filter(id=active_user.id).exists()
//     }

// function unlike_post(post_id, active_user_id) {
//     fetch(`/posts/${post_id}`, {
//         method: 'PUT',
//         body: JSON.stringify({
//             unliked_by: active_user_id
//         })
//     })
//     .then(function () {fetch(`/posts/${post_id}`)
//         .then(response => response.json())
//         .then(post => {
//             console.log(post.likes_count);
//             document.querySelector('#likes-count').innerHTML = `${post.likes_count}`;
//         })
//     })
// }


// function edit_post(post_id, active_user_id) {
//     fetch(`/posts/${post_id}`)
//     .then(response => response.json())
//     .then(post => {
//         // TODO
//         const post_data = [`${post.id}`, `${post.username}`, `${post.body}`, `${post.timestamp}`]
//         console.log(post_data, active_user_id)
//     })
// }