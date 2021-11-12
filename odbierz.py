
import email, getpass, imaplib, os, io, base64 

user = "scs2tste@gmail.com"
pwd = "SCS2021Testowe!"

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
m.select( ) # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes

type, data = m.search(None, 'ALL')

for num in data[0].split():
    typ, data = m.fetch(num, '(RFC822)' )

    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1].decode('utf-8'))
            email_subject = msg['subject']
            email_from = msg['from']
            email_heder = msg['SCS2021']
            print('SCS2021:', "%s" % email_heder)
            print ('From : ' + email_from )
            print ('Subject : ' + email_subject )
