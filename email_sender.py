"""
Email sender module for the chat room system.
This module handles sending HTML-formatted emails using Gmail's SMTP server.
Used primarily for sending verification codes to users.
"""

import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

class email_send:
    """
    Email sender class that handles sending HTML-formatted emails.
    Uses Gmail's SMTP server for sending emails.
    """
    
    def __init__(self):
        """
        Initialize the email sender with Gmail credentials.
        Note: In a production environment, these credentials should be stored securely
        and not hardcoded in the source code.
        """
        self.sender = "emencryption@gmail.com"
        self.password = "kpfo ebfp cmqv lfem"  # Gmail app-specific password

    def send_email(self,subject:str,message:str,recipient:str):
        """
        Send an HTML-formatted email to a recipient.
        
        Args:
            subject (str): Email subject line
            message (str): Main content of the email
            recipient (str): Recipient's email address
            
        Note:
            The email is sent using a pre-formatted HTML template with custom styling.
            The message is displayed in a large, centered format with a green background.
        """
        # HTML email template with custom styling
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

        # Create and configure email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient
        msg.set_content(email_message, subtype='html')
        
        # Send email using Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, recipient, msg.as_string())
            print("Message sent!")

