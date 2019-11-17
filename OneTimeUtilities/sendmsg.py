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
from common import get_student_project_progress, handle_onetime_message, get_student_project_string, setup_driver

driver = setup_driver('C:/Users/Feng/AppData/Local/Google/Chrome/User Data')


try:
	driver.get("https://auth.udacity.com/sign-in")
	WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Sign in with Google")]')))
	
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
	driver.get("https://hub.udacity.com/")
	
	WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
	time.sleep(20)
	studentlinks = driver.find_elements_by_xpath('//a')
	studentlinks = [sl.get_attribute('href') for sl in studentlinks if '/conversations/community:personal-mentor' in sl.get_attribute('href')]
	studentlinks.reverse()
	activestudentlinks = driver.find_elements_by_xpath('//span[contains(@class, "notification-badge_count")]/../../../..')
	activestudentlinks = [sl.get_attribute('href') for sl in activestudentlinks if '/conversations/community:personal-mentor' in sl.get_attribute('href')]
	studentlinks = list(set(studentlinks) - set(activestudentlinks))
	
	visited = []
	
	
	try:
		for sl in studentlinks:
			try:
				handle_onetime_message(sl, driver, visited, exclude, sys.argv[1])
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				with open('../exceptionss', 'w') as file:
					file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		with open('../exceptionss', 'w') as file:
			file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
		driver.quit()
		raise e
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../exceptionss', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
	driver.quit()
	raise e



driver.quit()
