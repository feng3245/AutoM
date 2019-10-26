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
sys.path.append('../')
from common import get_student_project_progress, handle_studentlink, answering_machine, email_out, setup_driver

driver = setup_driver('C:/Users/Automation/User Data')

try:
	driver.get("https://auth.udacity.com/sign-in")
	WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Sign in with Google")]')))
	
	login = driver.find_element_by_xpath('//div[contains(text(),"Sign in with Google")]')
	exclude = []
	with open('../excludes', 'r') as file:
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
	try:
		driver.get("https://hub.udacity.com/")
		WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
		
	except Exception as e:
		driver.get("https://hub.udacity.com/")
		WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))

	time.sleep(20)
	studentlinks = driver.find_elements_by_xpath('//span[contains(@class, "notification-badge_count")]/../../../..')
	studentlinks = [sl.get_attribute('href') for sl in studentlinks if '/conversations/community:personal-mentor' in sl.get_attribute('href')]
	studentlinks.reverse()

	badlinks = []
	if studentlinks:
		email_out(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], 'Following students need your attention: ',('<br/>'.join(studentlinks)))
	try:
		for sl in studentlinks:
			try:
				answering_machine(sl, driver)
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				with open('../exceptionssAFK', 'w') as file:
					file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
				badlinks.append(sl)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		with open('../exceptionssAFK', 'w') as file:
			file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
		driver.quit()
		raise e
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../exceptionssAFK', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
	driver.quit()
	raise e
with open('../badlinksanswermachine', 'w') as file:
	file.write('|'.join(badlinks))
driver.quit()
