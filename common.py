from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import sys, os
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import boto3
from botocore.exceptions import NoCredentialsError
def is_mentee(driver):
	try:
		return driver.find_element_by_xpath('//p[contains(text(),"Mentee")]')
	except:
		return False
def upload_to_aws(local_file, bucket, s3_file, access_key, secret_key):
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def setup_driver(usrdir, headless = False):
	options = ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--ignore-ssl-errors')
	options.add_argument('--allow-running-insecure-content')
	options.add_argument('--disable-web-security')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--no-referrers')
	if headless:
		options.add_argument("--headless")
		options.add_argument("--window-size=1900,1080")
		options.add_argument('--no-sandbox')
		options.add_argument('--start-maximized')
	options.add_argument('--user-data-dir={0}'.format(usrdir))
	
	capabilities = DesiredCapabilities.CHROME.copy()
	capabilities['acceptSslCerts'] = True 
	capabilities['acceptInsecureCerts'] = True
	if headless:
		driver = webdriver.Chrome(desired_capabilities=capabilities, executable_path="c:/ChromeDriver/chromedriver.exe", chrome_options=options)
	
	if not headless:
		driver = webdriver.Chrome(executable_path="c:/ChromeDriver/chromedriver.exe", chrome_options=options)
		driver.maximize_window()
		
	return driver

def get_student_project_progress(studentprojectprogress):
	studentprjdict = {}
	if not studentprojectprogress:
		return studentprjdict
	for sp in studentprojectprogress.split('|'):
		if sp.split('=')[0] not in studentprjdict:
			studentprjdict[sp.split('=')[0]] = []
		studentprjdict[sp.split('=')[0]].append(sp.split('=')[1])
	return studentprjdict

def get_student_project_string(studentprojectprogressdic):
	if not studentprojectprogressdic:
		return ""
	return '|'.join(['|'.join([k+"="+m for m in studentprojectprogressdic[k]]) for k in studentprojectprogressdic])
		
def clearBox(inputbox):
	for i in range(len(inputbox.get_attribute('value'))):
		inputbox.send_keys(Keys.BACKSPACE)    

def answering_machine(sl, driver):
	driver.get(sl)
	time.sleep(5)
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@data-user-message="true"]')))
	if not is_mentee(driver):
		return
	messageinput = driver.find_element_by_xpath('//textarea[@id="userInput"]')
	clearBox(messageinput)
	for c in 'It appears that your mentor Feng L. is currently unavailable but rest assured your questions will be answered in due time!':
		messageinput.send_keys(c)
	messageinput.send_keys(Keys.RETURN)
	return

def email_out(smtpsrv, user, password, sendto, subject, msgbody):
	msg = MIMEText(msgbody,'html')
	msg['Subject'] = subject
	msg['From'] = user
	msg['To'] = sendto
	smtpserver = smtplib.SMTP(smtpsrv,587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(user, password)
	smtpserver.sendmail(user, sendto, msg.as_string())
	smtpserver.close()

def handle_onetime_message(sl, driver, visited, exclude, greeting):
	driver.get(sl)
	time.sleep(5)
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
	if not is_mentee(driver):
		return
	if driver.find_element_by_xpath('//p[contains(text(),"Mentee")]'):
		studentname = driver.find_element_by_xpath('//h2').text
		if studentname not in exclude and studentname not in visited:
			visited.append(studentname)
			WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@data-user-message="true"]')))
			messageinput = driver.find_element_by_xpath('//textarea[@id="userInput"]')
			clearBox(messageinput)
			messageinput.send_keys(Keys.NULL)
			for c in greeting:
				messageinput.send_keys(c)
			messageinput.send_keys(Keys.RETURN)
	
			
def handle_studentlink(sl, driver, visited, exclude, greeting, projectpasses = {}, projectfails = {}, logfile = None):
	driver.get(sl)
	time.sleep(5)
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
	if driver.find_element_by_xpath('//p[contains(text(),"Mentee")]'):
		studentname = driver.find_element_by_xpath('//h2').text
		if studentname not in exclude and studentname not in visited:
			visited.append(studentname)
			WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@data-user-message="true"]')))
			nmessages = len(driver.find_elements_by_xpath('//div[@data-user-message="true"]'))
			messageinput = driver.find_element_by_xpath('//textarea[@id="userInput"]')
			clearBox(messageinput)
			
			if nmessages == 2 and driver.find_elements_by_xpath('//a[contains(text(),"{0}.")]'.format(studentname)):
				convomessages = driver.find_elements_by_xpath('//div[@data-user-message="true"]/div[3]/div/div/div/p')
				if '?' not in str(convomessages[-1].text) and len(convomessages[-1].text.split()) <= 7:
					for c in 'you got it :D':
						messageinput.send_keys(c)
					messageinput.send_keys(Keys.RETURN)
					return
			if logfile:
				logfile.write("Current projects are {}.".format(','.join([erp.text for erp in driver.find_elements_by_xpath('//ul[contains(@class, "project-list")]/li/p')])))
			if [conts for conts in driver.find_elements_by_xpath('//h6') if 'TODAY' in conts.text or 'YESTERDAY' in conts.text]:
				return
			#The hack will fix some time
			if logfile:
				WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "project-list")]/li/p')))
			if ' '.join(studentname.split()[:-1]) in projectpasses:
				studentprojects = [erp.text for erp in driver.find_elements_by_xpath('//ul[contains(@class, "project-list")]/li/p')]
				for pp in projectpasses[' '.join(studentname.split()[:-1])]:
					if any([(sp in pp) for sp in studentprojects]):
						for c in 'Just saw a notice that your submission for {0} got approved. Nice job keep up the good work :)'.format(pp):
							messageinput.send_keys(c)
						messageinput.send_keys(Keys.RETURN)
						projectpasses[studentname.split()[0]].remove(pp)
						if not projectpasses[studentname.split()[0]]:
							del projectpasses[studentname.split()[0]]
						return			
			passstudent =[k for k in projectpasses.keys() if studentname.title() in k.title()][0] if  [k for k in projectpasses.keys() if studentname.title() in k.title()] else ''
			
			if logfile:
				logfile.write('{} is the dictionary\r\n'.format(projectpasses))
				logfile.write('{} is the student\r\n'.format(studentname))
				logfile.write('{} is the student passing\r\n'.format(passstudent))
			
			if len(passstudent) > 0:
				studentprojects = [erp.text for erp in driver.find_elements_by_xpath('//ul[contains(@class, "project-list")]/li/p')]
				if logfile:
					logfile.write('Student have projects {}\r\n'.format(','.join(studentprojects)))
				for pp in projectpasses[passstudent]:
					if logfile:
						logfile.write('{} passed {}\r\n'.format(passstudent, pp))
					if any([(sp in pp) for sp in studentprojects]):
						if logfile:
							logfile.write('{} is one of {}\r\n'.format(pp, ','.join(studentprojects)))
						for c in 'Just saw a notice that your submission for {0} got approved. Nice job keep up the good work :)'.format(pp):
							messageinput.send_keys(c)
						messageinput.send_keys(Keys.RETURN)
						projectpasses[passstudent].remove(pp)
						if not projectpasses[passstudent]:
							del projectpasses[passstudent]
						return
			
			
			if ' '.join(studentname.split()[:-1]) in projectfails:
				studentprojects = [erp.text for erp in driver.find_elements_by_xpath('//ul[contains(@class, "project-list")]/li/p')]
				for fp in projectfails[' '.join(studentname.split()[:-1])]:
					if any([(sp in fp) for sp in studentprojects]):
						for c in 'Just saw reviewer had some change requests on {0}. Let me know if you needed some help'.format(fp):
							messageinput.send_keys(c)
						messageinput.send_keys(Keys.RETURN)
						projectfails[studentname.split()[0]].remove(fp)
						if not projectfails[studentname.split()[0]]:
							del projectfails[studentname.split()[0]]
						return
			failstudent = [k for k in projectfails.keys() if studentname.title() in k.title()][0] if [k for k in projectfails.keys() if studentname.title() in k.title()] else ''
			if logfile:
				logfile.write('{} is the student failing\r\n'.format(failstudent))
			if len(failstudent) > 0:
				studentprojects = [erp.text for erp in driver.find_elements_by_xpath('//ul[contains(@class, "project-list")]/li/p')]
				if logfile:
					logfile.write('Student have projects {}\r\n'.format(','.join(studentprojects)))				
				for fp in projectfails[failstudent]:
					if logfile:
						logfile.write('{} failed {}\r\n'.format(failstudent, fp))				
					if any([(sp in fp) for sp in studentprojects]):
						if logfile:
							logfile.write('{} is one of {}\r\n'.format(fp, ','.join(studentprojects)))					
						for c in 'Just saw reviewer had some change requests on {0}. Let me know if you needed some help'.format(fp):
							messageinput.send_keys(c)
						messageinput.send_keys(Keys.RETURN)
						projectfails[failstudent].remove(fp)
						if not projectfails[failstudent]:
							del projectfails[failstudent]
						return
			if nmessages <= 1:
				messageinput.send_keys(Keys.NULL)
				for c in greeting.format(studentname.split()[0].title()):
					messageinput.send_keys(c)
				messageinput.send_keys(Keys.RETURN)
				return
			lastcontact = [conts for conts in driver.find_elements_by_xpath('//h6') if (str(datetime.now().year) in conts.text) or (str(datetime.now().year-1) in conts.text) ][-1].text
			if (datetime.now() - datetime.strptime(lastcontact, '%B %d, %Y')).days > 7:
				messageinput.send_keys(Keys.NULL)
				for c in greeting.format(studentname.split()[0].title()):
					messageinput.send_keys(c)
				messageinput.send_keys(Keys.RETURN)
				return
	return

def change_message(sl, driver, msgusr, oldmsg, newmsg):
	driver.get(sl)
	time.sleep(5)
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(),"{0}")]'.format(msgusr))))
	if not is_mentee(driver):
		return
	lastMsg = driver.find_elements_by_xpath('//a[contains(text(),"{0}")]'.format(msgusr))[0]
	hover = ActionChains(driver).move_to_element(lastMsg)
	hover.perform()
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "display-user-message_menuContainer")]')))

	toolsmenu = driver.find_elements_by_xpath('//div[contains(@class, "display-user-message_menuContainer")]')[-1]
	hover = ActionChains(driver).move_to_element(toolsmenu)
	hover.click().perform()
	editbtn = driver.find_elements_by_xpath('//button[contains(@title, "Edit")]')[-1]
	hover = ActionChains(driver).move_to_element(editbtn)
	hover.click().perform()
	editinput = driver.find_elements_by_xpath('//textarea')[0]
	currentMsg = editinput.get_attribute('innerHTML')
	if not oldmsg in currentMsg:
		return
	removeindex = currentMsg.index(oldmsg)
	editinput.send_keys(Keys.NULL)
	for _ in range(len(currentMsg) - removeindex):
		editinput.send_keys(Keys.ARROW_LEFT)
	for _ in range(len(oldmsg)):
		editinput.send_keys(Keys.DELETE)
	for c in newmsg:
		editinput.send_keys(c)
	savebtn = driver.find_elements_by_xpath('//span[contains(text(), "Save")]')[0]
	driver.execute_script("arguments[0].click();", savebtn)
	return
def normalize_schedules(scheduled_events):
	eventTracker = {}
	for email, t, eventCode in scheduled_events:
		if eventCode in ('New Event', 'Updated'):
			eventTracker[email] = t
		else:
			if email in eventTracker:
				del eventTracker[email]
	return [(em, eventTracker[em]) for em in eventTracker]