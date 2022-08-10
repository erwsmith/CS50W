document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', create_post);
    // By default, load the inbox
    load_mailbox('inbox');
  });

  function create_post() {
    // Show compose view and hide other views
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    // Set compose-form to post email on submit
    document.querySelector('#compose-form').onsubmit = function(e) {
      e.preventDefault();
      // POST /emails
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value,
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      })
      .then(function() {load_mailbox('sent');});
      return false;
    }
  }