window.onpopstate = function(event) {
    show_posts(event.state.section, event.state.profile_user)
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            const section = this.dataset.section;
            history.pushState({section: section, profile_user: 'none'}, "");
        };
    });
    document.querySelectorAll('a').forEach(a => {
        a.onclick = function() {
            const section = this.dataset.section;
            history.pushState({section: section, profile_user: 'none'}, "");
        };
    });
    document.querySelector('#all-posts').addEventListener('click', () => show_posts('all'));
    if (document.querySelector('#following-posts')) {
        document.querySelector('#following-posts').addEventListener('click', () => show_posts('following'));
    }
    if (document.querySelector('#profile-posts')) {
        document.querySelector('#profile-posts').addEventListener('click', () => show_posts('profile'));
    }
    show_posts('all')
    const section = 'all';
    history.pushState({section: section, profile_user: 'none'}, "");
})


function show_posts(post_view, username='none') {
    
    let active_user_id = parseInt(document.querySelector('#active_user_id').dataset.active_user_id);
    let active_username = document.querySelector('#active_username').dataset.active_username;
    
    let view_name = ''
    if (post_view === 'all') {
        view_name = "All Posts";
    } else if (post_view === 'following') {
        view_name = "Following View";
    } else if (post_view === 'profile' && username !== 'none') {
        view_name = `${username}'s Profile`;
    } else if (post_view === 'profile' && username === 'none') {
        username = active_username
        view_name = `${username}'s Profile`;
    } else {
        console.log("Error: Invalid Post View")
        view_name = "All Posts";
    }

    document.querySelector('#posts-view-head').innerHTML = `<h4>${view_name}</h4>`;
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#posts-view').innerHTML = '';
    
    if (username === 'none') {
        fetch(`/posts/${post_view}`)
        .then(response => response.json())
        .then(posts => {
            get_post_data(posts, post_view)
        });
    } else {
        Promise.all([
            fetch(`/profile/${username}`),
            fetch(`/followers/${username}`)
        ])
        .then((responses) => {
            // Get a JSON object from each of the responses
            return Promise.all(responses.map((response) => {
                return response.json();
            }));
        })
        .then((data) => {
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
            
            let follow_button = document.createElement('button')

            if (follower.user_id === active_user_id) {
                follow_button.style.visibility = "hidden"
            } else if (follower.is_following) {
                follow_button.className = "btn btn-sm btn-outline-dark mx-2 px-3"
                follow_button.id = "unfollow-button"
                follow_button.innerHTML = "Unfollow"
                follow_button.addEventListener('click', () => {
                    console.log("Unfollow button clicked")
                    fetch(`/profile/${username}`, {
                      method: 'PUT',
                      body: JSON.stringify({
                        follow: false
                      })
                    })
                    .then(() => {
                        const section = 'profile';
                        history.pushState({section: section, profile_user: username}, "");
                    })
                    .then(() => {show_posts('profile', username)})
                })
            } else {
                follow_button.className = "btn btn-sm btn-outline-dark mx-2 px-3"
                follow_button.id = "follow-button"
                follow_button.innerHTML = "Follow"
                follow_button.addEventListener('click', () => {
                    console.log("Follow button clicked")
                    fetch(`/profile/${username}`, {
                      method: 'PUT',
                      body: JSON.stringify({
                        follow: true
                      })
                    })
                    .then(() => {
                        const section = 'profile';
                        history.pushState({section: section, profile_user: username}, "");
                    })
                    .then(() => {show_posts('profile', username)})
                })
            }

            document.querySelector('#posts-view-head').append(
                following_count,
                following_text,
                followers_count,
                followers_text,
                follow_button,
                )
        }).catch((error) => {console.log(error);});
    }
}

function get_post_data(posts, post_view='all') {
    
    let active_user_id = parseInt(document.querySelector('#active_user_id').dataset.active_user_id)
    let active_username = document.querySelector('#active_username').dataset.active_username

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
        post_username.name = `${post.username}`
        post_username.addEventListener('click', () => {
            const section = 'profile';
            history.pushState({section: section, profile_user: post_username.name}, "");
            show_posts('profile', post.username)
        })
        
        let post_body = document.createElement('div')
        post_body.className = "m-2"
        post_body.id = `body-${post.id}`
        post_body.innerHTML = `${post.body}`
        
        let post_timestamp = document.createElement('div')
        post_timestamp.className = "text-muted m-2"
        post_timestamp.innerHTML = `${post.timestamp}`
        
        let edit_button = document.createElement('button')
        if (post.user_id === active_user_id) {
            edit_button.innerHTML = "Edit";
            edit_button.id = "edit";
            edit_button.className = "btn btn-sm btn-outline-dark mx-2 px-3";
            edit_button.addEventListener('click', () => {
                console.log(`Edit button ${post.id} clicked!`)
                document.querySelector('#posts-view').style.display = 'none';
                document.querySelector('#compose-post').style.display = 'none';
                document.querySelector('#posts-view-head').style.display = 'block';
                document.querySelector('#post-edit-view').style.display = 'block';
                document.querySelector('#posts-view-head').innerHTML = '<h4>Edit post</h4>'
                document.querySelector('#post-edit-view').append(post_body);
                document.querySelector(`#body-${post.id}`).innerHTML = ''
                post_timestamp.style.visibility = "hidden"
                edit_button.style.visibility = "hidden"
                like_button.style.visibility = "hidden"
                likes_count.style.visibility = "hidden"
                
                let edit_post_body = document.createElement('textarea') 
                edit_post_body.className = "form-control" 
                edit_post_body.id = "edit-post-body" 
                edit_post_body.value = `${post.body}`
                document.querySelector(`#body-${post.id}`).append(edit_post_body)
                
                let save_edit_button = document.createElement('button')
                save_edit_button.innerHTML = 'Save changes'
                save_edit_button.id = 'save-edit-button'
                save_edit_button.className = "btn btn-sm btn-outline-dark my-0 mx-2 px-3"
                save_edit_button.addEventListener('click', () => {
                    console.log('Save changes button clicked')
                    fetch(`/get_post/${post.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            post_body: document.querySelector('#edit-post-body').value,
                        })
                    })
                    .then(() => {show_posts('profile')})
                })
                document.querySelector(`#body-${post.id}`).append(
                    document.createElement('br'),
                    save_edit_button
                    )
            });
        } else {
            edit_button.style.display = "none";
        }

        let likes_count = document.createElement('span')
        likes_count.id = `likes-count-${post.id}`
        likes_count.className = "mx-2"
        likes_count.innerHTML = `${post.likes_count}`

        let like_button = document.createElement('button');
        like_button.className = "btn btn-sm btn-outline-dark mx-2 px-3";

        if (post.liked_by.includes(active_username)) {
            like_button.innerHTML = 'Unlike';
            like_button.id = `unlike-${post.id}`;
            like_button.name = 'unlike';
            like_button.addEventListener('click', () => {
                console.log(`User ${active_user_id} clicked post ${post.id} ${like_button.name} button.`)
                fetch(`/like_post/${post.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: false,
                    })
                })
                .then(() => {show_posts(post_view)})
                // .then(() => {
                //     fetch(`/get_post/${post.id}`, {
                //         method: 'GET'
                //     })
                //     .then(response => response.json())
                //     .then(post => {
                //         document.querySelector(`#likes-count-${post.id}`).innerHTML = `${post.likes_count}`
                //         document.querySelector(`#unlike-${post.id}`).innerHTML = 'Like'
                //         document.querySelector(`#unlike-${post.id}`).id = `like-${post.id}`;
                //     })
                // })
            })
        } else {
            like_button.innerHTML = "Like";
            like_button.id = `like-${post.id}`;
            like_button.name = 'like';
            like_button.addEventListener('click', () => {
                console.log(`User ${active_user_id} clicked post ${post.id} like button.`)
                fetch(`/like_post/${post.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: true,
                    })
                })
                .then(() => {show_posts(post_view)})
                // .then(() =>{
                //     fetch(`/get_post/${post.id}`, {
                //         method: 'GET'
                //     })
                //     .then(response => response.json())
                //     .then(post => {
                //         document.querySelector(`#likes-count-${post.id}`).innerHTML = `${post.likes_count}`;
                //         document.querySelector(`#like-${post.id}`).innerHTML = 'Unlike';
                //         document.querySelector(`#like-${post.id}`).id = `unlike-${post.id}`;
                //     })  
                // })
            })
        }
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