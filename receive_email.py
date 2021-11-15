import email, getpass, imaplib, os, io, base64 

address = os.environ.get("SCS_SENDER_EMAIL")
password = os.environ.get("SCS_EMAIL_PASSWORD")

imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
imap_server.login(address, password)
imap_server.select( ) 

_, data = imap_server.search(None, 'ALL')

for num in data[0].split():
    typ, data = imap_server.fetch(num, '(RFC822)')

    for response_part in data:
      
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1].decode('utf-8'))
            email_subject = msg['subject']
            email_from = msg['from']
            email_header = msg['SCS2021']
            print('SCS2021:', "%s" % email_header)
            print ('From : ' + email_from)
            print ('Subject : ' + email_subject)
