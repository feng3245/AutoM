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
from common import get_student_project_progress, handle_studentlink, get_student_project_string, setup_driver

driver = setup_driver('C:/Users/ProjectGreeter/User Data', True)

try:
	exclude = []
	with open('../excludes', 'r') as file:
		exclude = file.read().replace('\n', '').split('|')
	with open('../StudentFailProjects', 'r') as file:
		failstudents = get_student_project_progress(file.read().replace('\n', ''))
	with open('../StudentsPassProjects', 'r') as file:
		successstudents = get_student_project_progress(file.read().replace('\n', ''))
	studentsinquestion = list(successstudents.keys())+list(failstudents.keys())
	if not studentsinquestion:
		driver.quit()
		sys.exit(0)
	studentsinquestion = [ ' '.join([s.split()[0], s.split()[1].title()[:1]]) if len(s.split()) >1 else s  for s in studentsinquestion]
	print(studentsinquestion)
	
	driver.get("https://hub.udacity.com/")
	time.sleep(10)
	if 'https://auth.udacity.com/sign-in' in driver.current_url:
		WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Sign in with Google")]')))
		user = driver.find_element_by_xpath('//input[@type="email"]')
		user.send_keys(Keys.NULL)
		for c in sys.argv[1]:
			user.send_keys(c)
		password = driver.find_element_by_xpath('//input[@type="password"]')
		password.send_keys(Keys.NULL)
		for c in sys.argv[2]:
			password.send_keys(c)
		password.send_keys(Keys.RETURN)
		driver.execute_script("arguments[0].click();",driver.find_element_by_xpath('//button[contains(text(),"Sign In")]'))

		time.sleep(20)
		print(driver.page_source)
		print(driver.current_url)
		try:
			driver.get("https://hub.udacity.com/")
			WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
			
		except Exception as e:
			print(driver.current_url)
			driver.get("https://hub.udacity.com/")
			WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
	
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
	time.sleep(20)
	studentlinks = driver.find_elements_by_xpath('//a['+" or ".join(["contains(.,'"+siq+"')" for siq in studentsinquestion])+']')
	studentlinks = [sl.get_attribute('href') for sl in studentlinks if '/conversations/community:personal-mentor' in sl.get_attribute('href')]
	studentlinks.reverse()
	activestudentlinks = driver.find_elements_by_xpath('//span[contains(@class, "notification-badge_count")]/../../../..')
	activestudentlinks = [sl.get_attribute('href') for sl in activestudentlinks if '/conversations/community:personal-mentor' in sl.get_attribute('href')]
	studentlinks = list(set(studentlinks) - set(activestudentlinks))
	visited = []
	badlinks = []
	greetings = []
	with open('../greetings', 'r') as file:
		greetings = file.read().replace('\n', '').split('|')
	
	greeting = greetings[0]
	
	with open('../greetings', 'w') as file:
		file.write('|'.join((greetings[1:]+[greeting])))

	

	try:
		with open('../answerupdateTracker', 'w+') as updateLogger:
			updateLogger.write('Students been looked at {}\r\n'.format('\r\n'.join(studentlinks)))
			for sl in studentlinks:
				try:
					handle_studentlink(sl, driver, visited, exclude, greeting, successstudents, failstudents, updateLogger)
				except Exception as e:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					with open('../answerupdateexceptions', 'w') as file:
						file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
					badlinks.append(sl)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		with open('../answerupdateexceptions', 'w') as file:
			file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
		with open('../StudentFailProjects', 'w') as file:
			file.write(get_student_project_string(failstudents))
		with open('../StudentsPassProjects', 'w') as file:
			file.write(get_student_project_string(successstudents))
		driver.quit()
		raise e
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../answerupdateexceptions', 'w') as file:
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
