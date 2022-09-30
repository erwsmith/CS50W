document.addEventListener('DOMContentLoaded',() => {
    document.querySelector('#all-posts').addEventListener('click', () => show_posts('all'));
    document.querySelector('#following-posts').addEventListener('click', () => show_posts('following'));
    document.querySelector('#profile-posts').addEventListener('click', () => show_posts('profile'));
    show_posts('all');
})


function show_posts(post_view, username='none') {
    
    let view_name = ''
    if (post_view === 'all') {
        view_name = "All Posts";
    } else if (post_view === 'following') {
        view_name = "Following View";
    } else if (post_view === 'profile' && username != 'none') {
        view_name = `${username}'s Profile`;
    } else if (post_view === 'profile' && username == 'none') {
        view_name = `Your Profile`;
    } else {
        console.log("Error: Invalid Post View")
        view_name = "All Posts";
    }

    document.querySelector('#posts-view-head').innerHTML = `<h3>${view_name}</h3>`;
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#posts-view').innerHTML = '';
    
    let au = document.querySelector('#active_user_id')
    let active_user_id = au.dataset.active_user_id
    
    let aun = document.querySelector('#active_username')
    let active_username = aun.dataset.active_username

    if (username === 'none') {
        fetch(`/posts/${post_view}`)
        .then(response => response.json())
        .then(posts => {
            get_post_data(posts)
        });
    } else {
        Promise.all([
            fetch(`/profile/${username}`),
            fetch(`/followers/${username}`)
        ]).then((responses) => {
            // Get a JSON object from each of the responses
            return Promise.all(responses.map((response) => {
                return response.json();
            }));
        }).then((data) => {
            let posts = data[0]
            get_post_data(posts)
            
            let follower = data[1]

            let following_count = document.createElement('span')
            following_count.className = "h4 ml-2 font-weight-bold"
            following_count.innerHTML = `${follower.following_count}`

            let following_text = document.createElement('span')
            following_text.innerHTML = "Following"
            following_text.className = "my-2 ml-2 mr-4"

            let followers_count = document.createElement('span')
            followers_count.className = "h4 ml-2 font-weight-bold"
            followers_count.innerHTML = `${follower.followers_count}`

            let followers_text = document.createElement('span')
            followers_text.innerHTML = "Follower(s)"
            followers_text.className = "m-2"

            document.querySelector('#posts-view-head').append(
                following_count,
                following_text,
                followers_count,
                followers_text,
                
                )
        }).catch((error) => {
                    console.log(error);
                });
    }

    // let followers_display = document.createElement('div')
    // // TODO - Translate this into better format
    // followers_display.innerHTML = `<div class="col-auto">Following: {{ follower.following.count }}</div>
    // <div class="col-auto ">Followers: {{ profile_user.followers.count }}</div>
    // {% if user != profile_user %}
    //     {% if is_following %}
    //         <div class="col-auto ">
    //             <input type="button" class="btn btn-sm btn-outline-dark mx-2 px-3" id="unfollow-button" value="Unfollow">
    //         </div>
    //     {% else %}
    //         <div class="col-auto ">
    //             <input type="button" class="btn btn-sm btn-outline-dark mx-2 px-3" id="follow-button" value="Follow">
    //         </div>
    //     {% endif %}
    // {% endif %}`
    // document.querySelector('#posts-view-head').append(followers_display)

}

function get_post_data(posts) {

    posts.forEach(post => {

        // all_post_data = [`
        //     ${post.id}, 
        //     ${post.username}, 
        //     ${post.user_id}, 
        //     ${post.body}, 
        //     ${post.timestamp}, 
        //     ${post.liked_by}, 
        //     ${post.likes_count}
        // `]
        
        let post_username = document.createElement('button')
        post_username.innerHTML = `${post.username}`
        post_username.id = "post_username"
        post_username.className = "btn btn-link m-0 p-0"
        post_username.addEventListener('click', () => {
            show_posts('profile', post.username)
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
            edit_button.addEventListener('click', () => {
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
        like_button.addEventListener('click', () => {
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
}


function like_post(post_id, active_user_id, post_view) {
    fetch(`/like_post/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked_by: active_user_id,
        })
    })
    .then(function() {document.location.reload()});
    
    // TODO - update likes count without reloading the whole page, don't change scroll position
    // .then(function() {show_posts(post_view);});
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