from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
import sys, os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common import get_student_project_progress, handle_studentlink, get_student_project_string, change_message

options = ChromeOptions()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--no-referrers')
options.add_argument('--user-data-dir=C:/Users/Feng/AppData/Local/Google/Chrome/User Data')
driver = webdriver.Chrome(executable_path="c:/ChromeDriver/chromedriver.exe", chrome_options=options)
driver.maximize_window()

driver.get("https://auth.udacity.com/sign-in")
WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Sign in with Google")]')))

login = driver.find_element_by_xpath('//div[contains(text(),"Sign in with Google")]')
exclude = []
with open('excludes', 'r') as file:
	exclude = file.read().replace('\n', '').split('|')
#temporarily not using it
driver.execute_script("arguments[0].click();", login)
#user = driver.find_element_by_xpath('//input[@type="email"]')
#user.send_keys(Keys.NULL)
#for c in 'axv@t.com':
#	user.send_keys(c)
#password = driver.find_element_by_xpath('//input[@type="password"]')
#for c in 'derppass':
#	password.send_keys(c)
#driver.execute_script("arguments[0].click();",driver.find_element_by_xpath('//button[contains(text(),"Sign In")]'))
time.sleep(5)
driver.get("https://hub.udacity.com/")
WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="'+mentorName+' profile image"]')))
time.sleep(20)
studentlinks = []
with open('badlinks', 'r') as file:
	studentlinks = file.read().replace('\n', '').split('|')
visited = []
badlinks = []
greetings = []
with open('greetings', 'r') as file:
	greetings = file.read().replace('\n', '').split('|')

greeting = greetings[0]

with open('greetings', 'w') as file:
	file.write('|'.join((greetings[1:]+[greeting])))

failstudents = {}
successstudents = {}

with open('StudentFailProjects', 'r') as file:
	failstudents = get_student_project_progress(file.read().replace('\n', ''))
with open('StudentsPassProjects', 'r') as file:
	successstudents = get_student_project_progress(file.read().replace('\n', ''))
    
change_message('https://hub.udacity.com/conversations/community:conversation:10428339352-3535828681?contextType=profile&profileId=3535828681', driver, ''+mentorName+'', 'linked in', 'linkedin')
time.sleep(20)