messages=[]
import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(app.config["DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class DevelopmentConfig(object):
    DATABASE_URI = "postgres://pmehzpfkeotntn:u4OXp20HhAef8TD8L9Hqk1LciC@ec2-174-129-21-42.compute-1.amazonaws.com:5432/d6ki3e1ckkv6f3"
    DEBUG = True

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	email = Column(String(128))

class Group(Base):
	__tablename__ = "groups"

	id = Column(Integer, primary_key=True)
	name = Column(String(128))

groups_users=Table('groups_users_association', Base.metadata,
	Column('group_id', Integer, ForeignKey('groups.id'))
	Column('user_id', Integer, ForeignKey('users.id'))
	)

def input_emails():
	self_name = raw_input("Who are you? ")
	self_email = raw_input("Your email:" )

	new_group="Y"
	while new_group == "Y":
		group_name = raw_input("What would you like to call your group? ")
		names = [self_name]
		emails = [self_email]
		new_friend = "Y"
		while new_friend == "Y":
			friend_name = raw_input("Please enter the name of a friend you'd like to keep in touch with: ")
			friend_email = raw_input("Your friend's email: ")
			names.append(friend_name)
			emails.append(friend_email)
			new_friend = raw_input("Do you want to add another friend to this group? Type Y or N ").upper()
			while new_friend not in ["Y", "N"]:
				new_friend = raw_input("Please type Y or N ")

		put_group_in_database(group_name, names, emails)

		new_group = raw_input("Do you want to create another group? Type Y or N ").upper()
		while new_group not in ["Y", "N"]:
			new_group = raw_input("Please type Y or N ")


def put_users_and_group_in_database(group_name, names, emails):
	for i in range(len(names)):
		new_user = Users(names[i], emails[i])



def send_message(msgtext, emails):
	#make a new message
	message=MIMEText(msgtext)

	#fill it in
	message['Subject']="Your monthly checkin!"
	message['From']="your friends at kit"
	message['To']=emails

	#set up the email server, via gmail
	server=smtplib.SMTP('smtp.gmail.com', 587)

	#start it
	server.ehlo()
	server.starttls()
	server.ehlo()

	#log in
	server.login("SPAMEMAIL@gmail.com", "ASddweew")

	#send the email
	server.sendmail("Your friends at kit", emails, message.as_string())

	#quit the server
	server.quit()

def create_message(messages_sent, users):
	message=messages[messages_sent]
	message=users[-1] + " and " + users[-2] ",\n" + message
	for user in users [::-3]:
		message = user + ", " + message
	message = "Dear "+ message
	messages_sent += 1



	