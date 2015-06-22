messages=[]
import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgres://pmehzpfkeotntn:u4OXp20HhAef8TD8L9Hqk1LciC@ec2-174-129-21-42.compute-1.amazonaws.com:5432/d6ki3e1ckkv6f3")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class DevelopmentConfig(object):
    DATABASE_URI = "postgres://pmehzpfkeotntn:u4OXp20HhAef8TD8L9Hqk1LciC@ec2-174-129-21-42.compute-1.amazonaws.com:5432/d6ki3e1ckkv6f3"
    DEBUG = True

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	name = Column(String(128), nullable=False)
	email = Column(String(128), nullable=False)
	groups_owned = relationship("Group", backref="users.id")

class Group(Base):
	__tablename__ = "groups"

	id = Column(Integer, primary_key=True)
	name = Column(String(128), nullable=False)
	creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	users = relationship("User", secondary="groups_users_association", backref="users")

groups_users=Table('groups_users_association', Base.metadata,
	Column('group_id', Integer, ForeignKey('groups.id')),
	Column('user_id', Integer, ForeignKey('users.id'))
	)

def input_emails():
	self_name = raw_input("Who are you? ")
	self_email = raw_input("Your email:" )

	creator = session.query(User).filter(User.name==self_name, User.email==self_email).first()
	print "yo"
	if creator:
		creator_id = creator.id
	else:
		creator = User(name=self_name, email=self_email)
		session.add(creator)
		session.commit(creator)
		creator = session.query(User).filter(name=self_name, email=self_email).first()
		creator_id = creator.id

	new_group="Y"
	while new_group == "Y":
		group_name = raw_input("What would you like to call your group? ")
		group = sesson.query(Group).filter(name=group_name, creator_id=creator_id).first()
		if group:
			group_id = group.id
			add_users = raw_input("You already created this group. Would you like to add more users? Please type Y or N ")
			if add_users == "N":
				print "Please rename your group"
				new_group = "Y"
				continue
		else:
			group = Group(name=group_name, creator_id=creator_id)
			session.add(group)
			session.commit()
			group = sesson.query(Group).filter(name=group_name, creator_id=creator_id).first()
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

		put_users_in_database_and_group(group_id, names, emails)

		new_group = raw_input("Do you want to create another group? Type Y or N ").upper()
		while new_group not in ["Y", "N"]:
			new_group = raw_input("Please type Y or N ")


def put_users_in_database_and_group(group_id, names, emails):
	for i in range(len(names)):
		new_user == session.query(User).filter(name=names[i], email=emails[i]).first()
		if new_user:
			new_user.group = group_id
			continue
		new_user = Users(names[i], emails[i])
		session.add(new_user)
		session.commit()



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
	message=users[-1] + " and " + users[-2] + ",\n" + message
	for user in users [::-3]:
		message = user + ", " + message
	message = "Dear "+ message
	messages_sent += 1


input_emails()
	
