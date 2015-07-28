messages=[]
import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from login import username, password

from email.mime.text import MIMEText
import smtplib
engine = create_engine("postgres://pmehzpfkeotntn:u4OXp20HhAef8TD8L9Hqk1LciC@ec2-174-129-21-42.compute-1.amazonaws.com:5432/d6ki3e1ckkv6f3")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class DevelopmentConfig(object):
    DATABASE_URI = "postgres://pmehzpfkeotntn:u4OXp20HhAef8TD8L9Hqk1LciC@ec2-174-129-21-42.compute-1.amazonaws.com:5432/d6ki3e1ckkv6f3"
    DEBUG = True

class Person(Base):
	__tablename__ = "kit_persons"

	id = Column(Integer, primary_key=True)
	name = Column(String(128), nullable=False)
	email = Column(String(128), nullable=False)
	groups_owned = relationship("Group", backref="kit_persons")

class Group(Base):
	__tablename__ = "groups"

	id = Column(Integer, primary_key=True)
	name = Column(String(128), nullable=False)
	creator_id = Column(Integer, ForeignKey('kit_persons.id'), nullable=False)
	
	persons = relationship("Person", secondary="groups_persons_association", backref="kit_persons")

groups_persons=Table('groups_persons_association', Base.metadata,
	Column('group_id', Integer, ForeignKey('groups.id')),
	Column('person_id', Integer, ForeignKey('kit_persons.id'))
	)

Base.metadata.create_all(engine)

def input_emails():
	self_name = raw_input("Who are you? ")
	self_email = raw_input("Your email: " )
	creator = session.query(Person).filter(Person.name==self_name, Person.email==self_email).first()
	if creator:
		creator_id = creator.id
	else:
		creator = Person(name=self_name, email=self_email)
		session.add(creator)
		session.commit()
		creator = session.query(Person).filter(Person.name==self_name, Person.email==self_email).first()
		creator_id = creator.id

	new_group="Y"
	while new_group == "Y":
		group_name = raw_input("What would you like to call your group? ")
		group = session.query(Group).filter(Group.name==group_name, Group.creator_id==creator_id).first()
		if group:
			group_id = group.id
			add_persons = raw_input("You already created this group. Would you like to add more members? Please type Y or N ")
			if add_persons == "N":
				print "Please rename your group"
				new_group = "Y"
				continue
		else:
			group = Group(name=group_name)
			print "I made a group", group
			group.creator_id = creator_id
			session.add(group)
			session.commit()
			group = session.query(Group).filter(Group.name==group_name, Group.creator_id==creator_id).first()
			group_id = group.id

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

		put_persons_in_database_and_group(group_id, names, emails)

		new_group = raw_input("Do you want to create another group? Type Y or N ").upper()
		while new_group not in ["Y", "N"]:
			new_group = raw_input("Please type Y or N ")


def put_persons_in_database_and_group(group_id, names, emails):
	for i in range(len(names)):
		new_user = session.query(Person).filter(Person.name==names[i], Person.email==emails[i]).first()
		if new_user:
			new_user.group = group_id
			continue
		new_user = Person(name=names[i], email=emails[i])
		print new_user, "new user"
		session.add(new_user)
		session.commit()


def create_message(msgtext, names, emails, subject):
	msgtext=persons[-1] + " and " + persons[-2] + ",\n" + msgtext
	for user in persons [::-3]:
		msgtext = user + ", " + msgtext
	msgtext = "Dear "+ msgtext
	#messages_sent += 1

	#make a new message
	message=MIMEText(msgtext)

	#fill it in
	message['Subject']=subject
	message['From']=names[0]
	message['To']=emails
	message['Reply-To']=emails

	#set up the email server, via gmail
	server=smtplib.SMTP('smtp.gmail.com', 587)

	#start it
	server.ehlo()
	server.starttls()
	server.ehlo()

	#log in
	server.login(username, password)

	#send the email
	server.sendmail("Your friends at kit", emails, message.as_string())

	#quit the server
	server.quit()

def get_persons_from_group(group_name):
	persons=session.query(Group).filter(Group.name==group_name).first().persons

	print persons
input_emails()
#send_message()
#get_persons_from_group("a")	
