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
import json
driver = setup_driver(sys.argv[1], False)

try:
	driver.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#search/label%3Acalendly")
	time.sleep(20)
	driver.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#search/label%3Acalendly")
	WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Hi Feng Liu, A new event has been scheduled.")]')))
	time.sleep(20)
	requesterInfo = {}
	requestedInfo = {}
	with open('../requesterInfo', 'r') as file:
		requesterInfo = eval(file.read())
	paragraphs = [p.get_attribute("innerText") for p in driver.find_elements_by_xpath('//span[contains(text(), "Hi Feng Liu, A new event has been scheduled.")]')]
	dates = [t.get_attribute("innerText").split('-')[1].strip() for t in driver.find_elements_by_xpath('//span/span[contains(text(), "New Event: ")]')]

	for paragraph, date in zip(paragraphs, dates):
		if datetime.strptime(date,'%H:%M %a, %d %b %Y') > datetime.now() and datetime.strptime(date,'%H:%M %a, %d %b %Y') < (datetime.now()+timedelta(hours = 24)):						
			requestedInfo[paragraph.split('Invitee Email:')[-1].split('Event Date/Time')[0].strip()]=requesterInfo[paragraph.split('Invitee Email:')[-1].split('Event Date/Time')[0].strip()]
	with open('../requestedInfo', 'w') as file:
		file.write(json.dumps(requestedInfo))		
			
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../email_read_meeting_exceptionss', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
	driver.quit()

driver.quit()
