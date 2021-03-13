from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Attachment, FileContent, FileName, FileType, Disposition, ContentId
import pdb
from datetime import datetime as date
from decouple import config
	
def send_simple_email(title, text, username=None, to_email='fightquake@gmail.com', from_email="contactus@fightquake.com"):
	creator = ''
	if username:
		creator = f' FROM {username}'
	msg_body = f'''<h1>Contact Us {creator}</h1>
				<p><b>Title</b>: {title}</p>
				<p><b>Message</b>: {text}</p>
				<br/>
				{date.now().strftime("%Y-%m-%d %H:%M")}
				<br />
				Website: <a target="_blank" href="https://fightquake.com">FightQuake</a>
				<br />
				Twitter: <a target="_blank" href="https://twitter.com/fightquake">@FightQuake</a>
				'''
	message = Mail(
		from_email=from_email,
		to_emails=[to_email, 'aaronchildres9@gmail.com'],
		subject=title,
		html_content=msg_body)
	status = 'delivered'
	try:
		sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
		response = sg.send(message)
		print(response.status_code)
		if response.status_code == 202:
			status = 'delivered'
	except Exception as e:
		print(str(e))
		status = 'failed'

	return status