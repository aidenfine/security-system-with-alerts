# EMAIL ADDRESS Alerts212421241@gmail.com
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
try:
    from config import EMAIL_PASSWORD, EMAIL_ADDRESS
except ImportError:
    pass

from email.mime.text import MIMEText
from datetime import datetime, timedelta

def getYesterdayDate(frmt='%m-%d-%Y', string=True):
    date = datetime.now() - timedelta(1)
    if string:
        return date.strftime(frmt)
    return date


emailfrom = EMAIL_ADDRESS
emailto = "fineaiden@gmail.com"
fileToSend = "/Users/aidenfine/security-system-with-alerts/security-system-with-alerts/main/output/11-12-2022-16-45-28.avi"
username = EMAIL_ADDRESS
password = EMAIL_PASSWORD

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = f"Movement Detected!"
msg.preamble = "WARNING"

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username,password)
server.sendmail(emailfrom, emailto, msg.as_string())
print("Email Sent")
server.quit()