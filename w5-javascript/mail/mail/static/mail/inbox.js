document.addEventListener('DOMContentLoaded', function(e) {
  // Use buttons to toggle between views
  console.log(e);
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#compose-form').addEventListener('submit', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  // Set compose-form to post email on submit
  document.querySelector('#compose-form').onsubmit = function() {
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
  }
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  // document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  // Get all emails in mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach((email) => {
      // add newline
      document.querySelector('#emails-view').append(document.createElement('hr'));
      // add custom div for read / unread emails
      if (email.read) {
        const element = document.createElement('inbox_div_read');
      } else {
        const element = document.createElement('inbox_div_unread');
      }
      element.innerHTML = `${email.sender} ${email.subject} ${email.timestamp}`
      element.id = `${email.id}`
      document.querySelector('#emails-view').append(element);
      element.addEventListener('click', function() {
        console.log(`Email ${email.id} has been clicked!`)
        load_email(email)
      });
    });
  });
}

function load_email(email) {
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#email-view').innerHTML = '';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // PUT /emails/<int:email_id> - mark email as read
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  // GET /emails/<int:email_id>
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {
      const element0 = document.createElement('div');
      element0.innerHTML = `From: ${email.sender}`;
      document.querySelector('#email-view').append(element0);
      const element1 = document.createElement('div');
      element1.innerHTML = `To: ${email.recipients} `;
      document.querySelector('#email-view').append(element1);
      const element2 = document.createElement('div');
      element2.innerHTML = `Subject: ${email.subject}`;
      document.querySelector('#email-view').append(element2);
      const element3 = document.createElement('div');
      element3.innerHTML = `Timestamp: ${email.timestamp}`;
      document.querySelector('#email-view').append(element3);
      const element4 = document.createElement('div');
      document.querySelector('#email-view').append(document.createElement('hr'));
      element4.innerHTML = `${email.body}`;
      document.querySelector('#email-view').append(element4);
    });
}