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
from config import *
from common import get_student_project_progress, handle_studentlink, get_student_project_string, setup_driver

driver = setup_driver(dailyAnswerProfileLocation)


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
	WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="'+mentorName+' profile image"]')))
	time.sleep(20)
	studentlinks = []
	with open('../badlinks', 'r') as file:
		studentlinks = file.read().replace('\n', '').split('|')
	visited = []
	badlinks = []
	greetings = []
	with open('../greetings', 'r') as file:
		greetings = file.read().replace('\n', '').split('|')
	
	greeting = greetings[0]
	
	with open('../greetings', 'w') as file:
		file.write('|'.join((greetings[1:]+[greeting])))
	
	failstudents = {}
	successstudents = {}
	
	with open('../StudentFailProjects', 'r') as file:
		failstudents = get_student_project_progress(file.read().replace('\n', ''))
	with open('../StudentsPassProjects', 'r') as file:
		successstudents = get_student_project_progress(file.read().replace('\n', ''))
	try:
		for sl in studentlinks:
			try:
				handle_studentlink(sl, driver, visited, exclude, greeting, successstudents, failstudents)
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				with open('../exceptionss', 'w') as file:
					file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
				badlinks.append(sl)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		with open('../exceptionss', 'w') as file:
			file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
		with open('../StudentFailProjects', 'w') as file:
			file.write(get_student_project_string(failstudents))
		with open('../StudentsPassProjects', 'w') as file:
			file.write(get_student_project_string(successstudents))
		driver.quit()
		raise e
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../exceptionss', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
	driver.quit()
	raise e
with open('../badlinks', 'w') as file:
	file.write('|'.join(badlinks))

with open('../StudentFailProjects', 'w') as file:
	file.write(get_student_project_string(failstudents))
with open('../StudentsPassProjects', 'w') as file:
	file.write(get_student_project_string(successstudents))



driver.quit()
