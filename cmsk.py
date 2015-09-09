import csv
import random
from login import username, password, PROMPTSFILE, NAMES, EMAILS, SUBJECT
from email.mime.text import MIMEText
import smtplib


def prompts_to_list(promptsfile=PROMPTSFILE):
	prompts=[]
	rownumbers=[]
	count=-1
	with open(promptsfile,"rb") as csvfile:
		reader= csv.DictReader(csvfile, delimiter=',', fieldnames=["Used?", "Prompt"])
		for row in reader:
			if row == {'Prompt': '', 'Used?': ''}:
				break
			print row
			prompts.append(row["Prompt"])
			if not row["Used?"]:
				rownumbers.append(count)
			count=count+1
	prompts.remove("Prompt")

	print rownumbers
	return prompts, rownumbers

def select_prompt_and_remove_from_list(prompts, rownumbers, promptsfile=PROMPTSFILE):
	prompt_row_number = random.choice(rownumbers)
	rownumbers.remove(prompt_row_number)
	print prompt_row_number
	print rownumbers
	with open(promptsfile, "wb") as csvfile:
		writer=csv.DictWriter(csvfile, fieldnames=['Used?','Prompt'])
		writer.writerow({"Used?":"Used?", "Prompt":"Prompt"})
		for i in range(len(prompts)):
			used="yes"
			if i in rownumbers:
				used=""
			writer.writerow({'Used?':used,'Prompt':prompts[i]})
	return prompts[prompt_row_number]


def send_message(msgtext, names=NAMES, emails=EMAILS, subject=SUBJECT):
	print msgtext
	msgtext=names[-2] + " and " + names[-1] + ",\n" + msgtext
	for name in names [:-2]:
		msgtext = name + ", " + msgtext
	msgtext = "Dear "+ msgtext + "\nSent by The CMSK secret app"
	print msgtext

	message=MIMEText(msgtext)

	#fill it in
	message['Subject']=subject
	message['From']="CMSK secret app"
	message['To']=",".join(emails)
	message['Reply-To']=",".join(emails)

	#set up the email server, via gmail
	server=smtplib.SMTP('smtp.gmail.com', 587)

	#start it
	server.ehlo()
	server.starttls()
	server.ehlo()

	#log in
	server.login(username, password)
	print type(message)
	#send the email
	server.sendmail("Your friends at kit", emails, message.as_string())

	#quit the server
	server.quit()

(prompts, rownumbers)= prompts_to_list()
send_message(select_prompt_and_remove_from_list(prompts, rownumbers))
