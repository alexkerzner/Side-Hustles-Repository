import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##### Input some info below:

day = 'Mon' #Should be one of Mon, Tue, Wed, Thu, Fri, Sat, or Sun
time1 = '6.00pm' ### For example. Times should be entered as strings in 12hr clock format with 'am' or 'pm' after.
time2 = '6.40pm'
time3 = None ### You can put a None data type for time2 and/or time3 if you only want to book one or two courts.

users = ['username1','username2','username3'] #Put your usernames here as strings
password = 'password' #I have the same password for all three. If you have different ones, just turn this into a list and adjust accordingly below. You just need to change all instances of "password" to "password[n]" and you'll be good.


#####

table_rows = [6.00, 6.40, 7.20, 8.00, 8.40, 9.20,10.00,10.40,11.20,12.00,12.40,1.20,2.00,2.40,3.20,4.00,4.40,5.20,6.00,6.40,7.20,8.00,8.40,9.20,10.00,10.40,11.20]

times = [time for time in [time1, time2, time3] if time != None]
clocks = []
rows = []

for n in range(len(times)):
    clock = float(times[n][:-2])
    if 'pm' in times[n]:
        rows.append(len(table_rows) - 1 - table_rows[::-1].index(clock))
    else:
        rows.append(table_rows.index(clock))
    rows[-1] += 1 #html starts counting at 1
    rows[-1] += 1 #First row of the table is just the court number


driver = webdriver.Chrome(executable_path = 'C:/Users/Owner/Desktop/chromedriver.exe') #Specify whatever path your driver is in here
driver.get('https://igniter.gigasports.com/home/login/mcmaster%20')

for n in range(len(times)):
    login_form = driver.find_element_by_id('loginForm')
    username_field = login_form.find_element_by_name('username')
    username_field.clear()
    username_field.send_keys(users[n])
    password_field = login_form.find_element_by_name('password')
    password_field.clear()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    driver.find_element_by_link_text('Bookings').click()

    XPath = "//input[contains(@value, '{day}')]".format(day=day)
    driver.find_element_by_xpath(XPath).click()

    if n == 0:
        for m in range(len(times)):
            for column in range(1,5): #If you're ok with using the IWC courts, then you can change the 5 to a 7 here, and adjust the next for loop accordingly.
                if 'Book' in driver.find_element_by_xpath('//tr[{row}]/td[{col}]'.format(row = rows[m], col = column)).text:
                    break
                    if column == 4:
                        print('Courts fully booked at {t}'.format(times[m]))
                        sys.exit()
    
    for column1 in [2,3,1,4]: #I prefer courts 2 and 3 to courts 1 and 4, so I specify this order.
        if 'Book' in driver.find_element_by_xpath('//tr[{row}]/td[{col}]'.format(row = rows[n], col = column1)).text:
            driver.find_element_by_xpath('//tr[{row}]/td[{col}]'.format(row = rows[n], col = column1)).find_element_by_link_text('Book').click()
            print('Court {courtnumber} booked at {booktime}'.format(courtnumber = column1, booktime = times[n]))
            break

    driver.find_element_by_class_name('fr').click()
    driver.find_element_by_link_text('Logout').click()
    driver.find_element_by_link_text('Log Out').click()


driver.quit()
