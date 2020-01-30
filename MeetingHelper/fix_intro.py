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
from common import get_student_project_progress, handle_studentlink, get_student_project_string, setup_driver, change_message

driver = setup_driver('C:/Users/IntroFix/User Data')
try:
	driver.get("https://auth.udacity.com/sign-in")
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Sign in with Google")]')))
	
	login = driver.find_element_by_xpath('//div[contains(text(),"Sign in with Google")]')
	studentlinksLastCheck = []
	with open('../studentLinksPrior', 'r') as file:
		studentlinksLastCheck = file.read().replace('\n', '').split('|')
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
	studentlinks = driver.find_elements_by_xpath('//a[contains(@href, "personal-mentor")]')
	studentlinks = [sl.get_attribute('href') for sl in studentlinks]
	with open('../studentLinksPrior', 'w') as file:
		file.write('|'.join(studentlinks))
	studentlinks = list(set(studentlinks) - set(studentlinksLastCheck))
	try:
		for sl in studentlinks:
			change_message(sl, driver, sys.argv[1], sys.argv[2], sys.argv[3])
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		with open('../fixlinkExceptions', 'w') as file:
			file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
		driver.quit()
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../fixlinkExceptions', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))

	driver.quit()

driver.quit()
