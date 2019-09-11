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
from common import get_student_project_progress, handle_studentlink, answering_machine

options = ChromeOptions()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--no-referrers')
options.add_argument('--user-data-dir=C:/Users/Automation/User Data')
driver = webdriver.Chrome(executable_path="c:/ChromeDriver/chromedriver.exe", chrome_options=options)
driver.maximize_window()
try:
	driver.get("https://auth.udacity.com/sign-in")
	WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//img[@alt="google"]')))
	
	login = driver.find_element_by_xpath('//img[@alt="google"]')
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
				answering_machine(sl, driver)
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
			file.write('')
		with open('../StudentsPassProjects', 'w') as file:
			file.write('')
		driver.close()
		raise e
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../exceptionss', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
	with open('../StudentFailProjects', 'w') as file:
		file.write('')
	with open('../StudentsPassProjects', 'w') as file:
		file.write('')
	driver.close()
	raise e
with open('../badlinks', 'w') as file:
	file.write('|'.join(badlinks))
with open('../StudentFailProjects', 'w') as file:
	file.write('')
with open('../StudentsPassProjects', 'w') as file:
	file.write('')
driver.close()
