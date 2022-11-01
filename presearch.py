import csv
import getpass
import random
import requests
import selenium
import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

service = Service("chromedriver.exe")
users_directory = f"C:\\Users\\{str(getpass.getuser())}\\AppData\\Local\\Google\\Chrome\\User Data"

with open("user_profiles.csv") as csvuserdata:
    chrome_users = list(csv.reader(csvuserdata))

with open("keywords.csv") as searchdata:
    searches = list(csv.reader(searchdata))

def telegram_bot_sendtext(bot_message):
    
    bot_token = '5265962620:AAFXV0dRhyCXGlXU3r2BZnhKgR59HMnHCrg'
    bot_chatID = '207699330'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

global users_count
global search_count
users_count, search_count = 0, 0

def report():
    my_message = f"Performed {search_count} searches for {users_count} users at server 02."   ## Customize your message
    telegram_bot_sendtext(my_message)


def main():

        for user in chrome_users:
            print(user[0])
            options = Options()
            options.add_argument("--user-data-dir=" + users_directory)
            print("--user-data-dir=" + str(users_directory))
            options.add_argument("--profile-directory=" + user[0])
            print(("--profile-directory=" + user[0]))
            options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(options=options, service=service)
            driver.get("https://www.presearch.org/")
            time.sleep(3)

            driver.find_element(By.ID, "search").clear()
            print(f'Starting presearch for profile {user[0]}')
            driver.find_element(By.ID, "search").send_keys(searches[random.randint(1, 66)])
            time.sleep(5)

            driver.find_element(By.CLASS_NAME, "btn-default").click()
            time.sleep(7)

            for i in range(random.randint(32, 37)):
                driver.find_element(By.NAME,"q").clear()
                time.sleep(random.randint(2, 17))
                print(f'Presearch #{i} for profile {user[0]}')
                driver.find_element(By.NAME,"q").send_keys(searches[random.randint(1, len(searches))])
                time.sleep(random.randint(1, 3))
                driver.find_element(By.CLASS_NAME,"text-primary-500").click()
                time.sleep(random.randint(5, 25))
                global search_count
                search_count+=1
            global users_count
            users_count+=1

            driver.close()
            time.sleep(3)
        report()
        search_count = 0
        users_count = 0



schedule.every().day.at("08:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
# main()