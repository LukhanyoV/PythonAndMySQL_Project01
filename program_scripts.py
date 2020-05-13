#Lukhanyo Vakele

#import the database connection
from db_connection import *
#for the time and date
from datetime import datetime

#initiaize the fake cookies as an empty array
login_cookies = []

#make my own count rows function because num_rows() is easier to remember
def num_rows(array):
	rows = 0
	for row in array:
		rows += 1
	return rows

#register the user function 
def register_user():
	#initialize the cursor
	cursor = db_connect.cursor()
	print()
	print("Register here")
	print()
	#note to self on what to do
	#first check if the username is already taken
	#tell the user to register with a different username if already taken
	#check for empty fields
	#IF THE REGISTRATION FAILS SEND THE USER BACK TO THE MAIN MENU
	try:
		full_name = input("Enter the full name: ")
		username = input("Enter the username: ")
		password = input("Enter your new password: ")
	except Exception as e:
		print("Error occured:",e)
	else:
		#check if usename already exist
		check = "SELECT username FROM users WHERE username = %s"
		val = (username, )
		cursor.execute(check, val)
		rows = cursor.fetchall()
		if num_rows(rows) != 1:
			#prepare the statements
			sql = "INSERT INTO users (full_name, username, password) VALUES (%s, %s, %s)"
			value = (full_name, username, password)
			#execute the database
			cursor.execute(sql, value)
			#make finale
			db_connect.commit()
			#success message
			print()
			print("Accoount has been successfully created!")
			print()
		else:
			#tell the user that the username already exists
			print()
			print("This username is already taken")
			print()


#login the user function 
def login_user():
	#initialize the cursor
	cursor = db_connect.cursor()
	print()
	print("Login the user")
	print()
	#note to self on what to do 
	#check if the username or password is wrong
	#for security purposes don\'t give them any hints like
	#telling them if the which was field corresponds to the database

	#IF THE LOGIN FAILS SEND THE USER BACK TO THE MAIN MENU
	try:
		#start the program
		username = input("Enter the username: ")
		password = input("Enter your new password: ")
	except Exception as e:
		print("Error occured:",e)
	else:
		#prepare the statements
		sql = "SELECT * FROM users WHERE username = %s AND password = %s AND active = %s"
		value = (username, password, "yes")

		#execute the database
		cursor.execute(sql, value)
		
		count = cursor.fetchall()

		#check if a match was found
		if cursor.rowcount == 1:
			cookies = [count[0][0], count[0][1], count[0][2], count[0][3], count[0][4]]
			#Log this session to the users log db
			insert_log(cookies[0])
			return cookies
		else:
			print()
			print("Invalid username and password combination")
			print()
			return []
		#make finale
		db_connect.commit()


#show the admin functions 
def show_admin_commands(id):
	while True:
		print()
		print("These are the admin commands")
		print()
		print("[1] Grab the list of people who are have signed in")
		print("[2] Grab the list of people who are where in but signed out")
		print("[3] Register a new user")
		print("[4] Delete user from the system")
		print("[5] Upgrade user privilesges")
		print("[6] Downgrade user privileges")
		print("[7] Logout")
		print()
		#take the user option from the keyboard
		try:
			option = int(input("Choose your option admin: "))
		except Exception as e:
			print("Error: ",e)
		else:
			#choose the options
			if option in [1,2,3,4,5,6,7]:
				#perfom admin tasks according to option

				#admin option 1 show the admin this
				if option == 1:
					logged_in_users()
				
				#admin option 2 show the admin users who have logged out
				if option == 2:
					logged_out_users()

				#admin option 3 allow admin to register new user
				if option == 3:
					admin_register_user()

				#admin option 4 allow admin to delete user from system
				if option == 4:
					admin_delete_user()

				#admin upgrade the user privileges
				if option == 5:
					upgrade_user()

				#admin downgrade the user privileges
				if option == 6:
					downgrade_user()

				#admin option 5 exit the loop
				if option == 7:
					logout_user(id)
					break
			#case out of range:
			else:
				print("You have given an invalid option")

#logout the user function
def logout_user(id):
	#the logout function will just use an UPDATE clause
	#to UPDATE the timeOut field WHERE timeOut NULL
	print()
	print("logging out")
	print()
	#update the database so that we can know when the user logged out
	update_log(id)
	#destroy the session cookies
	login_cookies = []

#SHOW LOGGED ON USERS
def logged_in_users():
	#the cursor
	cursor = db_connect.cursor()
	#the date for the today
	date = datetime.now().strftime("%Y-%m-%d")
	#select all the users who have not signed out
	command2 = "SELECT * FROM userslogs WHERE date=%s AND timeOut IS NULL"
	value = (date, )
	cursor.execute(command2, value)

	#grab the results
	results = cursor.fetchall()

	#check if any available today 
	if num_rows(results) != 0:
		#loop through the results to print them on new lines
		print("This is the list of people who have signed in for today")
		for row in results:
			#well how about I print each element of those results too in a prettier formart
			#do the pretty printout
			print("ID: ",row[1])
			print("DATE: ",row[2])
			print("Time in: ",row[3])
			print("Time out:",row[4])
			#let me just put in blank line to separate the results
			print()
	else:
		#tell the admin that no one has logged out for today
		print("No one has logged in for today")
		#this function ends here

	#finalize this function
	db_connect.commit()

#SHOW LOGGED OUT USERS
def logged_out_users():
	#the cursor
	cursor = db_connect.cursor()
	#the date for the today
	date = datetime.now().strftime("%Y-%m-%d")
	#select all the users who have not signed out
	command3 = "SELECT * FROM userslogs WHERE date=%s AND timeOut IS NOT NULL"
	value = (date, )
	cursor.execute(command3, value)

	#grab the results
	results = cursor.fetchall()

	#check if any available today 
	if num_rows(results) != 0:
		#loop through the results to print them on new lines
		print("This is the list of people who had signed out today")
		for row in results:
			#well how about I print each element of those results too in a prettier formart
			#do the pretty printout
			print("ID: ",row[1])
			print("DATE: ",row[2])
			print("Time in: ",row[3])
			print("Time out:",row[4])
			#let me just put in blank line to separate the results
			print()
	else:
		#tell the admin that no one has logged out for today
		print()
		print("No one has logged out for today")
		print()
		#this function ends here

	#finalize this function
	db_connect.commit()

#FUNCTION FOR ADMIN TO ADD NEW USER TO THE SYSTEM
def admin_register_user():
	#initialize the cursor
	cursor = db_connect.cursor()
	print()
	print("Admin register here")
	print()
	#note to self on what to do
	#first check if the username is already taken
	#tell the user to register with a different username if already taken
	#check for empty fields
	#IF THE REGISTRATION FAILS SEND THE USER BACK TO THE MAIN MENU
	try:
		full_name = input("Enter the full name: ")
		username = input("Enter the username: ")
		password = input("Enter your new password: ")
		admin = input("Make user admin (Y/N): ")
	except Exception as e:
		print("Error occured:",e)
	else:
		#prepare the statements
		sql = "SELECT * FROM users WHERE username = %s"
		value = (username, )

		#execute the database
		cursor.execute(sql, value)
		
		count = cursor.fetchall()

		#check if a match was found
		if num_rows(count) != 1:
			if admin in ["Y", "y", "N", "n"]:
				#check if should add as admin 
				if admin in ["Y", "y"]:
					role = "admin"
				else:
					role = "standard"
			
			#prepare the statements
			command3 = "INSERT INTO users (full_name, username, password, role) VALUES (%s, %s, %s, %s)"
			value = (full_name, username, password, role)
			#execute the command
			cursor.execute(command3, value)
			#make finale
			db_connect.commit()
			#success message
			print("Accoount has been successfully created!")
		else:
			print("The username is already taken")

#FUNCTION FOR ADMIN TO REMOVE USER FROM THE SYSTEM
def admin_delete_user():
	#initialize the cursor
	cursor = db_connect.cursor()
	
	try:
		#start the program
		username = input("Enter the username: ")
	except Exception as e:
		print("Error occured:",e)
	else:
		#prepare the statements
		sql = "SELECT id FROM users WHERE username = %s"
		value = (username, )

		#execute the database
		cursor.execute(sql, value)
		
		count = cursor.fetchall()

		#check if a match was found
		if num_rows(count) == 1:
			id = count[0][0]
			#make account in active
			cursor.execute("UPDATE users SET active = %s WHERE id = %s", ("no", id))
			#make the changes final
			db_connect.commit()
			#success message
			print("The account has been deleted")
		else:
			print("Username not found")

#WHEN THE USER LOGS IN WRITE DOWN IN THE LOG TABLE
def insert_log(id):
	# INSERT INTO userslogs (id, date, timeIn) VALUES (id, CURRENT_DATE, CURRENT_TIME);
	#the cursor
	cursor = db_connect.cursor()
	#prepare the statements
	date = datetime.now().strftime("%Y-%m-%d")
	time = datetime.now().strftime("%H:%M:%S")
	command5 = "INSERT INTO userslogs (id, date, timeIn) VALUES (%s, %s, %s)"
	values = (id, date, time)
	#execute the command
	cursor.execute(command5, values)
	#make finale
	db_connect.commit()
	#success message
	print("Start session has been logged")

#WHEN THE USER LOGS OUT WRITE DOWN IN THE LOG TABLE
def update_log(id):
	# UPDATE userslogs SET timeOut = CURRENT_TIME WHERE id = id AND timeOut IS NULL;
	#the cursor
	cursor = db_connect.cursor()
	#prepare the statements
	timeOut = datetime.now().strftime("%H:%M:%S")
	command6 = "UPDATE userslogs SET timeOut = %s WHERE id = %s AND timeOut IS NULL"
	values = (timeOut, id)
	#execute the command
	cursor.execute(command6, values)
	#make finale
	db_connect.commit()
	#success message
	print("End session has been logged")

#ADMIN USER PRIVILEDGES
#ADMIN MAKE ANY USER ADMIN
def upgrade_user():
	#create the cursor 
	cursor = db_connect.cursor()

	try:
		#get the username you want to make admin 
		username = input("Enter the username you want to make admin: ")
	except Exception as e:
		print("Error occured:",e)
	else:
		#check if the username exists first
		#execute the check
		cursor.execute("SELECT username FROM users WHERE username=%s", (username, ))
		#count the rows
		count = cursor.fetchall()

		if num_rows(count) == 1:
			#prepare the statements
			command7 = "UPDATE users SET role=%s WHERE username=%s"
			values = ("admin", username)
			#execute the command
			cursor.execute(command7, values)
			#commit the recent changes
			db_connect.commit()
			#print the success message
			print("The user has been upgraded to admin")
		else:
			#the user was not found it could be a spelling error in the username or white spacing
			#but either way lets just tell them that the username isn't found and also it would be
			#a great time to tell them the username is case sensitive
			print("The username was not found, please check for any kind of spelling error and also note the username is case sensitive")


#ADMIN MAKE ANY USER STANDARD USER
def downgrade_user():
	#create the cursor 
	cursor = db_connect.cursor()

	try:
		#get the username you want to make standard 
		username = input("Enter the username you want to make standard: ")
	except Exception as e:
		print("Error occured:",e)
	else:
		#check if the username exists first
		#execute the check
		cursor.execute("SELECT username FROM users WHERE username = %s", (username, ))
		#count the rows
		count = cursor.fetchall()

		if num_rows(count) == 1:
			#prepare the statements
			command7 = "UPDATE users SET role=%s WHERE username=%s"
			values = ("standard", username)
			#execute the command
			cursor.execute(command7, values)
			#commit the recent changes
			db_connect.commit()
			#print the success message
			print("The user has been downgraded to standard user")
		else:
			#the user was not found it could be a spelling error in the username or white spacing
			#but either way lets just tell them that the username isn't found and also it would be
			#a great time to tell them the username is case sensitive
			print("The username was not found, please check for any kind of spelling error and also note the username is case sensitive")

		
