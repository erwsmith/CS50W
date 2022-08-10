document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#all_posts').addEventListener('click', () => load_display('all_posts'));
    document.querySelector('#following_posts').addEventListener('click', () => load_display('following_posts'));
    document.querySelector('#create_post').addEventListener('click', create_post);
    // By default, load the inbox
    load_display('all_posts');
  });

  function create_post() {
    // Show create view and hide other views
    document.querySelector('#all-view').style.display = 'none';
    document.querySelector('#following-view').style.display = 'none';
    document.querySelector('#create-view').style.display = 'block';
    // Clear out post composition field
    document.querySelector('#post-body').value = '';
    // Set form to post on submit
    document.querySelector('#post-form').onsubmit = function(e) {
      e.preventDefault();
      // POST /posts
      fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#post-body').value,
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      })
      .then(function() {load_display('all_posts');});
      return false;
    }
  }

  function load_display(post_filter) {
    return false;
  }