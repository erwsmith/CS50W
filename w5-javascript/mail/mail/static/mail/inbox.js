document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
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
    load_mailbox('sent');
    return false;
  }
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  // document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view-head').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector('#grid').innerHTML = '';
  // Get all emails in mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach((email) => {
      const email_data = [`${email.sender}`, `${email.subject}`, `${email.timestamp}`]
      const grid = document.getElementById("grid");
      for (let a of email_data) { 
        let cell = document.createElement("div");
        cell.innerHTML = a;
        if (email.read) {
          cell.className = "read_cell";
        } else {
          cell.className = "unread_cell";
        }
        cell.addEventListener('click', function() {
          console.log(`Email ${email.id} has been clicked!`);
          load_email(email);
        });
        grid.appendChild(cell);
      }
    });
  });
}

function load_email(email) {
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#email-view-body').innerHTML = '';
  document.querySelector('#archive_button').innerHTML = '';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  // get email
  // GET /emails/<int:email_id>
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {
    const element0 = document.createElement('div');
    element0.innerHTML = `From: ${email.sender}`;
    document.querySelector('#email-view-body').append(element0);
    const element1 = document.createElement('div');
    element1.innerHTML = `To: ${email.recipients} `;
    document.querySelector('#email-view-body').append(element1);
    const element2 = document.createElement('div');
    element2.innerHTML = `Subject: ${email.subject}`;
    document.querySelector('#email-view-body').append(element2);
    const element3 = document.createElement('div');
    element3.innerHTML = `Timestamp: ${email.timestamp}`;
    document.querySelector('#email-view-body').append(element3);
    const element4 = document.createElement('div');
    document.querySelector('#email-view-body').append(document.createElement('hr'));
    element4.innerHTML = `${email.body}`;
    document.querySelector('#email-view-body').append(element4);
  });
  // mark email as read
  // PUT /emails/<int:email_id>
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  // Archive 
  if (email.archived) {
    const unarchive_button = document.createElement('button');
    unarchive_button.innerHTML = "Unarchive";
    unarchive_button.id = "unarchive-button";
    unarchive_button.className = "btn btn-sm btn-outline-primary";
    document.querySelector('#archive_button').append(unarchive_button);
    document.querySelector('#unarchive-button').onclick = function() {
      // PUT /emails/<int:email_id> - mark email as unarchived
      console.log("Unarchive button clicked!")
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
      load_mailbox('inbox')
    }
  } else {
    const archive_button = document.createElement('button');
    archive_button.innerHTML = "Archive";
    archive_button.id = "archive-button";
    archive_button.className = "btn btn-sm btn-outline-primary";
    document.querySelector('#archive_button').append(archive_button);
    document.querySelector('#archive-button').onclick = function() {
      // PUT /emails/<int:email_id> - mark email as unarchived
      console.log("Archive button clicked!")
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
      load_mailbox('inbox')
    }
  }
}