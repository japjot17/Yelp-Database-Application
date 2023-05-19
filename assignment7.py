

#
#
# For testing SQL Server connection in CSIL through pyodbc connection (using Windows Authentication)
#
# Author: Johnny Zhang
#
# You should run this program on a CSIL Windows system. (verified with Python 3.6.2 64bit)
#
# Last modified @ 2020.06.02, 2018.03.27
#
#  verified with Python 3.7.7 64bit & SQL Server 2019, 2020.06.02
#
# There is no need to modify this program before using.
#
# (the default database has been setup for you)
#
#

import pyodbc
import datetime
import random
import string
import datetime

conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')

#create cursor object
cursor = conn.cursor()

business_id = 'JapjotsBusinessID'
name = 'JapjotsRestaruant'
address = '1234 Japjot Ave'
city = 'Surrey'
postal_code = 'V3Y6G1'
stars = None
review_count = 0 

Values = [business_id, name, address, city, postal_code, stars, review_count]
#print(Values)



#INSERT into business VALUES('JapjotsBusinessID', 'JapjotsRestaruant','1234 Japjot Ave','Surrey','V3Y6G1', null, 0)
#SQLCommand = ('INSERT into business(business_id, name, address, city, postal_code, stars, review_count) VALUES (?, ?,?,?,?,?,?) ')


#use cursor object to run sql query
#cursor.execute(SQLCommand, Values)
#conn.commit()


# to validate the connection, there is no need to change the following line
cursor.execute('SELECT username,passphrase from dbo.helpdesk')
row = cursor.fetchone()
while row:
    #print ('SQL Server standard login name = ' + row[0])
    #print ('The password for this login name = ' + row[1])
    row = cursor.fetchone()




#  This program will output your CSIL SQL Server standard login,
#  If you see the output as s_<yourusername>, it means the connection is a success.
#  
#  You can now start working on your assignment.
# 

logged_in_user = ""


#login function

def login():
    global logged_in_user
    username = input("Please enter a valid userID: ")


   
    #select * from user_yelp where user_id = '__hr-GtD9qh8_sYSGTRqXw'
    #friend 'r3QexFIhBXBT99canAgVEg' '_0euf-z6-Rb7PwUTdC50Dg'

    


   #__qZrCESIQTMEtXTIhcXsw

    loginQuery = "SELECT * FROM user_yelp WHERE user_id = ?"

    cursor.execute(loginQuery, username)

    row = cursor.fetchone()

    

    if row is not None:
        print("Login Successful")
        logged_in_user = username
        return True
    else: 
        print("Wrong username")
        return False


def interfaceMenu():
    logged_in = False 
    #while logged_in is false prompt user for login
    while not logged_in:
        logged_in = login()
        if not logged_in:
            print('Please try logging in again')

    
 


    while True:
        print("Main Menu: ")
        print("1: Search Business ")
        print("2: Search Users ")
        print("3: Make a Friend ")
        print("4: Write a Review ")
        print("5: Exit ")
        print("User: "+logged_in_user)

        choice = input("Enter the function you would like to call (Ex. 1 for Search Business...): ")
        print("you chose number "+ choice)
        if choice == '1':
            search_business()


        elif choice == '2':
            search_users()

        elif choice == '3':
            make_friend()

        elif choice == '4':
            write_review()

        elif choice == '5':
            print("Exit Application...")
            #exit while loop
            return
        else:
            print("Invalid choice. Please try again.")

        

def search_business():
    print("Search business function")
    city = input("Enter the City: ")
    name = input("Enter the name(or part of the name): ")
    min_stars = input("minimum number of stars(1-5 or leave blank for any): ")
    max_stars = input("maximum number of stars(1-5 or leave blank for any): ")

    if min_stars == "":
        min_stars = "0"
    if max_stars == "":
        #print("5 stars")
        max_stars = "5"

    #while min_stars.isdigit() and max_stars.isdigit() and int(min_stars) > int(max_stars)


   


    

    search_query = "SELECT * FROM business WHERE lower(name) LIKE '%" + name +"%' AND stars BETWEEN "+min_stars+" AND "+max_stars
    if city != "":
        search_query+= " AND city = '"+city+"'"
    search_query+= "ORDER BY name"
    print(search_query)

    cursor.execute(search_query)

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No results found")
    else:
        print("Search Results")
        print("")
        i = 1
        for row in rows:
            print(str(i)+")")
            print("Business_id = " + row[0])
            print("Name = " + row[1])
            print("Address = "+ row[2])
            print("City = " + row[4])
            print("Stars = "+ str(row[5]))
            i= i+1
            print(" ")
            print("------------------------------")

    
    

 
   

            




def search_users():

    #get filters
    name = input("Enter the name of user: ")
    useful = input("Useful (yes/no): ").lower()
    funny = input("Funny (yes/no): ").lower()
    cool = input("Cool (yes/no): ").lower()

    


    user_query = "SELECT * FROM user_yelp WHERE name LIKE '%" + name  + "%'"
    if useful == "yes":
        user_query+= " AND useful > 0"
    else:
        user_query+=" AND useful = 0"

    if funny == "yes":
        user_query+= " AND funny > 0"
    else:
        user_query+= " AND funny = 0"
    if cool == "yes":
        user_query+= " AND cool > 0"
    else:
        user_query+= " AND cool = 0"
    user_query+= " Order by name"

    print(user_query)

    cursor.execute(user_query)

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No Results Found")
        print("")
    else:
        print("")
        print("Search Results")
        print("")
        i = 1
        for row in rows:
            useful_value = "yes" if row.useful > 0 else "no"
            funny_value = "yes" if row.funny > 0  else "no"
            cool_value = "yes" if row.cool > 0  else "no"
            print(str(i)+")")
            print("User_id = " + row[0])
            print("Name = " + row[1])
            print("Date registered = " + str(row[3]))
            print("Useful = "+ useful_value)
            print("Funny = "+ funny_value )
            print("Cool = "+cool_value)

            i= i+1
            print("-------------------------")
        
        friendAnswer = input("Would you like to add a friend? ").lower()
        if friendAnswer == "yes":
            make_friend()
    
    






    

def make_friend():
    global logged_in_user

    #first checks if you are already friends with the user before adding them. If users are already friend the transaction won't go through
    friend_ID = input("Enter the user_ID of the user you would like to be friends with: ")

    friend_check = "SELECT * FROM friendship WHERE user_id = '"+logged_in_user+"' AND friend = '" +friend_ID+"'"
    #print(friend_check)


    cursor.execute(friend_check)


    row = cursor.fetchone()

    if row:
        print("Friendship already exists with this user")
    else:

        friend_add = "INSERT INTO Friendship (user_id, friend) VALUES (?,?)"
        cursor.execute(friend_add, (logged_in_user, friend_ID))
        print("You are now friends with this user ")
        print("")
    
    conn.commit()
    




def write_review():
    global logged_in_user

    business_id = input("Enter the business ID of the business you want to review: ")


    #checks to see if business you're reviewing exists
    while True:
        business_search = "SELECT * FROM Business WHERE business_id = ?"
        cursor.execute(business_search,business_id)
        existing_business = cursor.fetchone()

        if existing_business:
            break
        else:
            print("Entered an invalid business_id. Please try again ")
            business_id = input("Enter the business ID of the business you want to review: ")
        
    stars = int(input("Enter the number of stars(1-5): "))

    while True:
        review_ID = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(19))
        print("reviewID = " + review_ID)
        cursor.execute("SELECT * FROM Review WHERE review_id = '"+review_ID+"'")
        existing_review = cursor.fetchone()

        if not existing_review:
            break
    #todays_date = datetime.date.today()
    #print(todays_date)

    #review_query= "INSERT INTO review (review_id,user_id,business_id,stars,useful, funny, cool, date) VALUES (?,?,?,?,?,?,?,?)"
    review_query = "INSERT into review (review_id, user_id, business_id, stars) VALUES (?,?,?,?)"



    review_values = [review_ID, logged_in_user, business_id, stars]

    cursor.execute(review_query, review_values)
    print("Review recorded successfully")
    print("")

    #update_query = "UPDATE business SET review_count = (SELECT COUNT(*) FROM review WHERE business_id = ? ), stars = (SELECT AVG(stars) FROM review WHERE business_id = ?) WHERE business_id = ? "
    #update_values = [business_id, business_id, business_id]
    #cursor.execute(update_query,update_values)
    conn.commit()





    

 







interfaceMenu()

     
cursor.close()
conn.close()

