from email.mime.base import MIMEBase
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "SCSTestowe@gmail.com"
receiver_email = "piotrek9880@gmail.com"
password = input('SCS2021Testowe!')

message = MIMEMultipart("alternative")
message["Subject"] = "SCS2021<1000"
message["From"] = sender_email
message["To"] = receiver_email

filename = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Facilisi cras fermentum odio eu feugiat pretium nibh ipsum. Tincidunt praesent semper feugiat nibh sed pulvinar proin. Senectus et netus et malesuada. Potenti nullam ac tortor vitae. In nulla posuere sollicitudin aliquam ultrices sagittis. Sit amet aliquam id diam maecenas ultricies mi. Nec dui nunc mattis enim ut. Urna id volutpat lacus laoreet non curabitur gravida arcu. Sem et tortor consequat id porta nibh venenatis. Malesuada bibendum arcu vitae elementum curabitur vitae. Lobortis mattis aliquam faucibus purus in massa tempor nec feugiat. Blandit aliquam etiam erat velit scelerisque in dictum non consectetur. Habitasse platea dictumst vestibulum rhoncus est pellentesque elit. Proin libero nunc consequat interdum.Pellentesque habitant morbi tristique senectus et netus et. Odio euismod lacinia at quis risus sed vulputate. Dolor morbi non arcu risus quis varius quam quisque id. Adipiscing diam donec adipiscing tristique. Venenatis cras sed felis eget velit aliquet sagittis id. Aliquam id diam maecenas ultricies mi eget. Cursus eget nunc scelerisque viverra mauris in aliquam sem fringilla. Eget aliquet nibh praesent tristique magna sit amet purus. Pulvinar pellentesque habitant morbi tristique senectus et netus et malesuada. Ut morbi tincidunt augue interdum velit euismod in pellentesque massa. Etiam sit amet nisl purus in mollis. Tortor at auctor urna nunc id cursus metus. Mi in nulla posuere sollicitudin. Tristique et egestas quis ipsum suspendisse ultrices gravida dictum fusce. Ultricies integer quis auctor elit sed vulputate mi. Ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue. Nulla facilisi nullam vehicula ipsum a. Nibh tortor id aliquet lectus proin nibh nisl condimentum. Eget dolor morbi non arcu risus quis varius quam quisque. Porttitor lacus luctus accumsan tortor posuere ac.Id neque aliquam vestibulum morbi blandit cursus risus at ultrices. Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Sapien eget mi proin sed libero. Vel pretium lectus quam id. Tincidunt praesent semper feugiat nibh sed pulvinar. Ullamcorper dignissim cras tincidunt lobortis feugiat. Luctus venenatis lectus magna fringilla urna porttitor rhoncus. Amet nisl purus in mollis nunc sed id semper risus. Risus quis varius quam quisque id diam vel quam elementum. Nascetur ridiculus mus mauris vitae ultricies.Urna id volutpat lacus laoreet non. Elit eget gravida cum sociis. Fermentum posuere urna nec tincidunt praesent semper feugiat nibh. Dignissim convallis aenean et tortor. Non nisi est sit amet facilisis magna. Adipiscing enim eu turpis egestas. Nibh mauris cursus mattis molestie. Id diam vel quam elementum pulvinar etiam non quam lacus. Dignissim cras tincidunt lobortis feugiat vivamus at augue eget arcu. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio. Adipiscing elit duis tristique sollicitudin nibh sit. Adipiscing tristique risus nec feugiat in fermentum posuere urna nec. Nunc sed velit dignissim sodales ut. Ac auctor augue mauris augue neque gravida in. Auctor eu augue ut lectus arcu bibendum at. Sed arcu non odio euismod. Egestas purus viverra accumsan in nisl. Sodales neque sodales ut etiam sit amet nisl purus.Pharetra pharetra massa massa ultricies mi quis hendrerit. Egestas pretium aenean pharetra magna ac placerat vestibulum lectus. Elementum pulvinar etiam non quam lacus suspendisse. Sed augue lacus viverra vitae congue eu. Sed turpis tincidunt id aliquet risus. Nunc faucibus a pellentesque sit amet porttitor eget dolor morbi. Risus nec feugiat in fermentum posuere urna nec tincidunt. Sed velit dignissim sodales ut eu. Augue lacus viverra vitae congue. Id velit ut tortor pretium viverra suspendisse. Mauris pellentesque pulvinar pellentesque habitant morbi tristique. Malesuada bibendum arcu vitae elementum curabitur vitae nunc sed. Quis lectus nulla at volutpat diam ut venenatis tellus. Semper risus in hendrerit gravida rutrum. Parturient montes nascetur ridiculus mus mauris vitae. Fermentum et sollicitudin ac orci phasellus egestas tellus rutrum. Leo vel orci porta non pulvinar neque. Vitae nunc sed velit dignissim sodales ut eu sem integer.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Facilisi cras fermentum odio eu feugiat pretium nibh ipsum. Tincidunt praesent semper feugiat nibh sed pulvinar proin. Senectus et netus et malesuada. Potenti nullam ac tortor vitae. In nulla posuere sollicitudin aliquam ultrices sagittis. Sit amet aliquam id diam maecenas ultricies mi. Nec dui nunc mattis enim ut. Urna id volutpat lacus laoreet non curabitur gravida arcu. Sem et tortor consequat id porta nibh venenatis. Malesuada bibendum arcu vitae elementum curabitur vitae. Lobortis mattis aliquam faucibus purus in massa tempor nec feugiat. Blandit aliquam etiam erat velit scelerisque in dictum non consectetur. Habitasse platea dictumst vestibulum rhoncus est pellentesque elit. Proin libero nunc consequat interdum.Pellentesque habitant morbi tristique senectus et netus et. Odio euismod lacinia at quis risus sed vulputate. Dolor morbi non arcu risus quis varius quam quisque id. Adipiscing diam donec adipiscing tristique. Venenatis cras sed felis eget velit aliquet sagittis id. Aliquam id diam maecenas ultricies mi eget. Cursus eget nunc scelerisque viverra mauris in aliquam sem fringilla. Eget aliquet nibh praesent tristique magna sit amet purus. Pulvinar pellentesque habitant morbi tristique senectus et netus et malesuada. Ut morbi tincidunt augue interdum velit euismod in pellentesque massa. Etiam sit amet nisl purus in mollis. Tortor at auctor urna nunc id cursus metus. Mi in nulla posuere sollicitudin. Tristique et egestas quis ipsum suspendisse ultrices gravida dictum fusce. Ultricies integer quis auctor elit sed vulputate mi. Ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue. Nulla facilisi nullam vehicula ipsum a. Nibh tortor id aliquet lectus proin nibh nisl condimentum. Eget dolor morbi non arcu risus quis varius quam quisque. Porttitor lacus luctus accumsan tortor posuere ac.Id neque aliquam vestibulum morbi blandit cursus risus at ultrices. Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Sapien eget mi proin sed luctus accumsan tortor posuere ac.Id neque aliquam vestibulum morbi blandit cursus risus at ultrices. Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Sapien eget mi proin sed luctus accumsan tortor posuere ac.Id neque aliquam vestibulum morbi blandit cursus risus at ultrices. Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Sapien eget mi proin sed"
part = MIMEBase('charset="utf-8"', 'text/plain')

part.add_header('SCS2021', "%s" % filename)

#message.attach(part)
message.add_header('SCS2021', "%s" % filename)
# Create the plain-text and HTML version of your message
text = """\
Hi,
Czy mnie znajdziesz?"""
html = """\
<html>
  <body>
    <p>Hi,<br>
        Czy mnie znajdziesz?
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )