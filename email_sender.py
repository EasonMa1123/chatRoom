import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

class email_send:
    def __init__(self):
        self.sender = "emencryption@gmail.com"
        self.password = "kpfo ebfp cmqv lfem"


    def send_email(self,subject:str,message:str,recipient:str):

        email_message = '''
	<!DOCTYPE html>
	<html>
	<head>
		<link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<style type="text/css">
		h1{font-size:56px}
		h2{font-size:28px;font-weight:900}
		p{font-weight:100}
		td{vertical-align:top}
		#email{margin:auto;width:600px;background-color:#fff}
		</style>
	</head>
	<body bgcolor="#F5F8FA" style="width: 100%; font-family:Lato, sans-serif; font-size:18px;">
	<div id="email">
		<table role="presentation" width="100%">
			<tr>
				<td bgcolor="#051014" align="center" style="color: white;">
					<h1> Your verification Code:</h1>
				</td>
		</table>
		<table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;"></table>
        <table role="presentation" width="100%">
			<tr>
				<td bgcolor="#05a614" align="center" style="color: white;">
					<h1> '''+message+'''</h1>
				</td>
		</table>
	</div>
	</body>
	</html>
'''

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient
        msg.set_content(email_message, subtype='html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, recipient, msg.as_string())
            print("Message sent!")

