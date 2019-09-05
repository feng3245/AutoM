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
from selenium.webdriver.common.action_chains import ActionChains



options = ChromeOptions()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--no-referrers')
options.add_argument('--user-data-dir=C:/Users/feng3245/AppData/Local/Google/Chrome/User Data')
driver = webdriver.Chrome(executable_path="c:/ChromeDriver/chromedriver.exe", chrome_options=options)

try:
	driver.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#search/label%3Ayourmentee+is%3Aunread")
	WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[@class="Dj"]')))
	menteePassProjects = []
	menteeFailProjects = []
	
	projectProgressParagraphs = driver.find_elements_by_xpath('//span[contains(text(), "Your mentee,") and contains(@class, "y2")]')
	for projectProgressParagraph in projectProgressParagraphs:
		projectprogText = projectProgressParagraph.text.split('Hi Feng, ')[1]
		if 'did not pass' in projectprogText:
			menteename = projectprogText.split('did not pass the')[0].replace('Your mentee', '').replace(',','').strip()
			menteeproject = projectprogText.split('did not pass the')[1].split('project')[0].strip()
			menteeFailProjects.append('{0}={1}'.format(menteename, menteeproject))
		elif 'passed' in  projectprogText:
			menteename = projectprogText.split('passed the')[0].replace('Your mentee', '').replace(',','').strip()
			menteeproject = projectprogText.split('passed the')[1].split('project')[0].strip()
			menteePassProjects.append('{0}={1}'.format(menteename, menteeproject))
	
	while driver.find_elements_by_xpath('//tr[contains(@class, "boomeranginlinebutton")]'):
		mails = driver.find_elements_by_xpath('//tr[contains(@class, "boomeranginlinebutton")]')
		driver.execute_script("arguments[0].click();",mails[-1])
		driver.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#search/label%3Ayourmentee+is%3Aunread")
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../email_read_exceptionss', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
	driver.close()
	raise e
with open('../StudentsPassProjects', 'w') as file:
	file.write('|'.join(menteePassProjects))

with open('../StudentFailProjects', 'w') as file:
	file.write('|'.join(menteeFailProjects))

driver.close()
