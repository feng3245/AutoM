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
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
driver = setup_driver(sys.argv[1])
try:
	driver.get("https://auth.udacity.com/sign-in")
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Sign in with Google")]')))
	
	login = driver.find_element_by_xpath('//div[contains(text(),"Sign in with Google")]')
	driver.execute_script("arguments[0].click();", login)
	time.sleep(5)
	driver.get("https://zoom.us/meeting/schedule")
	time.sleep(20)
	login = None
	if EC.presence_of_element_located((By.XPATH, '//a[contains(text(),"Sign in with Google")]')):
		try:
			login = driver.find_element_by_xpath('//a[contains(text(),"Sign in with Google")]')
			driver.execute_script("arguments[0].click();", login)
			time.sleep(20)
		except:
			print('Well w/e')
	requestedInfo = {}
	with open('../requestedInfo', 'r') as file:
		requestedInfo = eval(file.read())
	for requester in requestedInfo:
		driver.get("https://zoom.us/meeting/schedule")
		driver.execute_script("arguments[0].value = '1:1 -"+requestedInfo[requester][1]+'-'+requestedInfo[requester][0]+"';",driver.find_element_by_id('topic'))
		currentTime = datetime.strptime(requestedInfo[requester][2],'%H:%M %a, %d %b %Y')
		driver.execute_script("arguments[0].value = '"+currentTime.strftime('%m/%d/%Y')+"';", driver.find_element_by_id('start_date'))
		driver.execute_script("arguments[0].click();",driver.find_element_by_id('start_time'))
		time.sleep(10)
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//span[contains(text(),"'+currentTime.strftime('%I:%M').lstrip('0')+'")]'))
		driver.execute_script("arguments[0].click();", driver.find_element_by_id('start_time_2'))
		time.sleep(10)
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//span[contains(text(),"'+currentTime.strftime('%p')+'")]'))
		driver.execute_script("arguments[0].click();", driver.find_element_by_id('timezone'))
		time.sleep(5)
		timezoneString = 'Eastern Time'
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//span[contains(text(),"'+timezoneString+'")]'))
		driver.execute_script("arguments[0].value = '0';", driver.find_element_by_id('duration_hr'))
		driver.execute_script("arguments[0].value = '30';", driver.find_element_by_id('duration_min'))
		driver.execute_script("arguments[0].click();", driver.find_element_by_id('option_video_host_on'))
		driver.execute_script("arguments[0].click();", driver.find_element_by_id('option_video_participant_on'))
		driver.execute_script("arguments[0].click();", driver.find_element_by_id('option_jbh'))
		driver.execute_script("arguments[0].click();", driver.find_element_by_id('option_waiting_room'))
		driver.execute_script("arguments[0].click();", driver.find_element_by_id('option_autorec'))
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//button[contains(text(),"Save")]'))
		WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.ID, 'copyInvitation')))
		copyinv = driver.find_element_by_id('copyInvitation')
		ActionChains(driver).move_to_element(copyinv).click().perform()
		WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.ID, 'invite_email')))
		zoomInvite = driver.find_element_by_id('invite_email').get_attribute('innerHTML')
		subprocess.run("clip", universal_newlines=True, input=zoomInvite)
		time.sleep(2)
		driver.get("http://study-hall.udacity.com/")
		WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
		try:
			student_url = driver.find_element_by_xpath('//a/descendant::p[contains(text(),"'+requestedInfo[requester][0]+'")]/ancestor::a[contains(@href, "personal-mentor")]').get_attribute('href')
		except:
			continue
		driver.get(student_url)
		WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
		messageinput = driver.find_element_by_xpath('//textarea[@id="userInput"]')
		messageinput.send_keys(Keys.NULL)
		messageinput.send_keys(Keys.CONTROL, 'v')
		time.sleep(1)
		messageinput.send_keys(Keys.RETURN)
		time.sleep(3)
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../zoomscheduleexceptionss', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))

	driver.quit()

driver.quit()
