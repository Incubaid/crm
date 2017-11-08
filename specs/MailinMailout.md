## mail in

- use python mailserver which processes all incoming mails & attaches them to appropriate object
    - e.g. https://github.com/kennethreitz/inbox.py
- mail addresses used will be
    - $uid_$objtype@$maildomain e.g. 4jd3_contact@main.threefoldtoken.com
    - support@$maildomain will be attached to project: support as ticket
- only recognized senders will be allowed to send
- the author field is used to show where mail comes from (who is originator)
- if author not recognized then we send message back to see we don't recognize you in our system please send email to support@$maildomain to get help
- attachments will be stored in $webdir/files/$blakehash.$extension & linked into the message (markdown)

## mail out

- depending the object we decide to who to send emails e.g. project will send to all users & contacts & companies attached to project, ...
- if the destination field was used before sending then use the email addr as stated there
- we need a state field to know what the state of the email is:
   - tosend, failed, ...


