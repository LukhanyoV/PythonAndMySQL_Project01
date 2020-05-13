#Lukhanyo Vakele
#Class 2

#get the database connection from the db_connection
from db_connection import *

#also import the file with the scripts
from program_scripts import *

#start the program
#check for the flag before starting the program
if start:
	#show the welcom screen 
	print("Welcome To LifeChoices online")
	print()
	#enter a loop 
	while True:
        #show the user options
		print()
		print("Choose the relevent option below")
		print("[1] Login to your account")
		print("[2] Register to your account")
		print("[3] Exit the program")
		#get the user input and check for errors
		try:
			option = int(input("Enter your option: "))
		#shout the error
		except:
			print("That was an invalid option, please try again")
		else:
			#do something cool and awesome with the user option
			#check if the user insert valid input
			if option in [1,2,3]:
				#if the user choose option 1 take the user to the login screen
				if option == 1:
					#calling the user login function
					login_cookies = login_user()
				#if the user choose option 2 take the user to the register screen
				if option == 2:
					#calling the register function
					register_user()
				#if the user choose option 3 end the program
				if option == 3:
					#before ending the program close the database connection
					db_connect.close()
					break
					
			#check if the user is logged in
			if len(login_cookies) != 0:
				#yes the user is logged in
				#display message for logged in users only
				print()
				print()
				print("Login was successful!\nEnjoy Your Day")

				#check the user role, if the user is admin show the admin option
				if "admin" in login_cookies:
					admin = True
					#welcome screen for the admin
					print("Wow you have got admin priviledges")
					#show them there commands
					show_admin_commands(login_cookies[0])
				else:
					#show the logout button
					print("[1] To logout")
					print()
					#logout the user only when they input the logout
					name = 0
					while name != "1":
						name = input("Enter your option: ")
					print()
					print("Good Bye, enjoy the rest of your day")
					#call the logout function
					logout_user(login_cookies[0])
					
#the else will be executed just in case the database connection failed
else:
	#end the program and apologize to user
	print("We are sorry, but our site is currently having some technical difficulties.")
	print("We might not be aware of this so please report it to our administrator.")
	print("admin@lifechoices.online")
