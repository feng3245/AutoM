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
sys.path.append('../')
from config import *
from common import get_student_project_progress, handle_studentlink, get_student_project_string, setup_driver, is_mentee, clearBox
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
driver = setup_driver(sys.argv[1])
try:

	time.sleep(5)
	driver.get("https://zoom.us/meeting")
	time.sleep(20)
	login = None
	if EC.presence_of_element_located((By.XPATH, '//a[contains(text(),"Sign in with Google")]')):
		try:
			login = driver.find_element_by_xpath('//a[contains(text(),"Sign in with Google")]')
			driver.execute_script("arguments[0].click();", login)
			time.sleep(20)
		except:
			print('Well w/e')
	
	driver.get("https://zoom.us/meeting")
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"mtg-date")]')))	
	timesToday = [t.get_attribute('innerHTML') for t in driver.find_elements_by_xpath('//div[contains(@class,"mtg-date") and contains(text(),"Today")]/span')]
	if timesToday:
		callsToday = [t.get_attribute('innerText') for t in driver.find_elements_by_xpath('//div[contains(@class,"mtg-date") and contains(text(),"Today")]/ancestor::div[contains(@class, "clearfix")]/descendant::a[contains(@title,"Click to view meeting details")]')]
		
		localTime = (datetime.utcnow() - timedelta(hours=timezoneAdj)).strftime('%H:%M')	
		studentsWithUpCommingCall = [c.split('-')[-1] for t, c in zip(timesToday,callsToday) if (datetime.strptime(t,"%I:%M %p") - timedelta(hours=3)).strftime('%H:%M') < localTime ]
		
		if studentsWithUpCommingCall:
			driver.get("https://auth.udacity.com/sign-in")
			WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Sign in with Google")]')))
			
			login = driver.find_element_by_xpath('//div[contains(text(),"Sign in with Google")]')
			driver.execute_script("arguments[0].click();", login)
			time.sleep(20)
			driver.get("https://mentor-dashboard.udacity.com/mentorship/overview")
			WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'personal-mentor')]")))
			time.sleep(35)
			
			for student in studentsWithUpCommingCall:
				try:
					student_url = driver.find_element_by_xpath('//a[contains(text(),"'+student+'.") and contains(@href, "personal-mentor")]').get_attribute('href')
				except:
					continue
				driver.get(student_url)
				WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(),"'+mentorName+'")]')))
				WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//textarea[@id="userInput"]')))
				lastMsg = ''
				try:
					lastMsg = driver.find_elements_by_xpath('//a[contains(text(),"'+mentorName+'")]/ancestor::div[contains(@class, "user-message_container")]/descendant::div[contains(@class,"markdown-renderer")]/p')[-1].get_attribute('innerText')
				except:
					print('cant find last message')
					continue
				if not is_mentee(driver):
					continue
				
				if "Hi, just want to give you a heads up that we have a schedule meeting within a few hours." in lastMsg:
					continue
				messageinput = driver.find_element_by_xpath('//textarea[@id="userInput"]')
				clearBox(messageinput)
				messageinput.send_keys(Keys.NULL)
				time.sleep(3)
				for c in "Hi, just want to give you a heads up that we have a schedule meeting within a few hours.":
					messageinput.send_keys(c)
				time.sleep(1)
				messageinput.send_keys(Keys.RETURN)
				time.sleep(3)
				driver.get("https://mentor-dashboard.udacity.com/mentorship/overview")
				WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'personal-mentor')]")))
				time.sleep(35)
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../zoomreminderexceptionss', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))

	driver.quit()

driver.quit()
