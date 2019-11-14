from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
import sys, os
import time
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
sys.path.append('../')
from common import setup_driver

driver = setup_driver('C:/Users/AutoEmailCheck/User Data', False)

try:
	driver.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#search/label%3Ayourmentee+is%3Aunread")
	time.sleep(20)
	driver.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#search/label%3Ayourmentee+is%3Aunread")
	WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "y2")]')))
	menteePassProjects = []
	menteeFailProjects = []
	time.sleep(20)
	paragraphs = [p.get_attribute("innerText") for p in driver.find_elements_by_xpath('//span[contains(text(), "Your mentee,") and contains(@class, "y2")]')]
	dates = [d.get_attribute("title") for d in driver.find_elements_by_xpath('//td[contains(@class,"xW") and contains(@class,"xY")]/span')]
	for paragraph, date in zip(paragraphs, dates):
		print(paragraph, date)
		if datetime.strptime(str(date), '%a, %b %d, %Y, %I:%M %p') > (datetime.now()-timedelta(hours = 12)):			
			
			if not 'Hi Feng, ' in paragraph:
				continue
			projectprogText = paragraph.split('Hi Feng, ')[1]
			
			if 'did not pass' in projectprogText:
				menteename = projectprogText.split('did not pass the')[0].replace('Your mentee', '').replace(',','').strip()
				menteeproject = projectprogText.split('did not pass the')[1].split('project')[0].strip().replace('Use Deep Learning to Clone Driving Behavior','Behavioral Cloning').replace('Traffic Sign Classification', 'Traffic Sign Classifier')
				menteeFailProjects.append('{0}={1}'.format(menteename, menteeproject))
			elif 'passed' in  projectprogText:
				menteename = projectprogText.split('passed the')[0].replace('Your mentee', '').replace(',','').strip()
				menteeproject = projectprogText.split('passed the')[1].split('project')[0].strip().replace('Use Deep Learning to Clone Driving Behavior','Behavioral Cloning').replace('Traffic Sign Classification', 'Traffic Sign Classifier')
				menteePassProjects.append('{0}={1}'.format(menteename, menteeproject))
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../email_read_exceptionss', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
	driver.quit()
	raise e
with open('../StudentsPassProjects', 'w') as file:
	file.write('|'.join(list(set(menteePassProjects))))

with open('../StudentFailProjects', 'w') as file:
	file.write('|'.join(list(set(menteeFailProjects)-set(menteePassProjects))))

driver.quit()
