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
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Get all emails in 'mailbox'
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach((email) => {
      const hr = document.createElement('hr');
      document.querySelector('#emails-view').append(hr);
      const element = document.createElement('inbox_div');
      element.innerHTML = `${email.sender} ${email.subject} ${email.timestamp}`
      element.id = `${email.id}`
      document.querySelector('#emails-view').append(element);
      element.addEventListener('click', function() {
        console.log(`email ${element.id} has been clicked!`)
      });
    });
  });
}

// // GET /emails/<int:email_id>
// // get email with id=100
// fetch('/emails/${email.id}')
// .then(response => response.json())
// .then(email => {
//     // Print email
//     console.log(email);

//     // ... do something else with email ...
// });

// // POST /emails
// fetch('/emails', {
//   method: 'POST',
//   body: JSON.stringify({
//       recipients: 'baz@example.com',
//       subject: 'Meeting time',
//       body: 'How about we meet tomorrow at 3pm?'
//   })
// })
// .then(response => response.json())
// .then(result => {
//     // Print result
//     console.log(result);
// });

// // PUT /emails/<int:email_id>
// fetch('/emails/100', {
//   method: 'PUT',
//   body: JSON.stringify({
//       archived: true // or read: true / false
//   })
// })