#Lukhanyo Vakele
#Class 2

#This file will handle the database connection
#first import the mysql and python connector
import mysql.connector as mysql

#check if the database connection was a success
try:
	#create the database connection
	db_connect = mysql.connect(host="localhost", port="3306", user="root", passwd="1234", database="lifechoicesonline")
#catch for any errors
except Exception as e:
	print("Error:",e)

#put a flag to check for any errors while connecting to the database
#I won\'t allow the main program to start with this
if db_connect:
	start = True
else:
	start = False
