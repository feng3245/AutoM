from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys, os
import time
from datetime import datetime
import smtplib

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
		
    

def answering_machine(sl, driver):
	driver.get(sl)
	time.sleep(5)
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@data-user-message="true"]')))
	if not driver.find_element_by_xpath('//p[contains(text(),"Mentee")]'):
		return
	messageinput = driver.find_element_by_xpath('//textarea[@id="userInput"]')
	for c in 'It appears that your mentor Feng L. is currently unavailable but rest assured your questions will be answered in due time!':
		messageinput.send_keys(c)
	messageinput.send_keys(Keys.RETURN)
	return

def email_out(smtpsrv, user, password, sendto, subject, msgbody):
	smtpserver = smtplib.SMTP(smtpsrv,587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(user, password)
	header = 'To:' + sendto + '\r\n' + 'From: ' + user + '\r\n' + 'Subject:{0} \r\n'.format(subject)
	msgbody = header + msgbody
	smtpserver.sendmail(user, sendto, msgbody)
	smtpserver.close()
	
def handle_studentlink(sl, driver, visited, exclude, greeting, projectpasses = {}, projectfails = {}):
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
			
			if studentname.split()[0] in projectpasses:
				studentprojects = [erp.text for erp in driver.find_elements_by_xpath('//ul[contains(@class, "project-list")]/li/p')]
				for pp in projectpasses[studentname.split()[0]]:
					if any([(sp in pp) for sp in studentprojects]):
						for c in 'Just saw a notice that your submission for {0} got approved. Nice job keep up the good work :)'.format(pp):
							messageinput.send_keys(c)
						messageinput.send_keys(Keys.RETURN)
						projectpasses[studentname.split()[0]].remove(pp)
						if not projectpasses[studentname.split()[0]]:
							del projectpasses[studentname.split()[0]]
						return
			
			if studentname.split()[0] in projectfails:
				studentprojects = [erp.text for erp in driver.find_elements_by_xpath('//ul[contains(@class, "project-list")]/li/p')]
				for fp in projectfails[studentname.split()[0]]:
					if any([(sp in fp) for sp in studentprojects]):
						for c in 'Just saw reviewer had some change requests on {0}. Let me know if you needed some help'.format(pp):
							messageinput.send_keys(c)
						messageinput.send_keys(Keys.RETURN)
						projectfails[studentname.split()[0]].remove(fp)
						if not projectfails[studentname.split()[0]]:
							del projectfails[studentname.split()[0]]
						return
			
			if nmessages == 2 and driver.find_elements_by_xpath('//a[contains(text(),"{0}.")]'.format(studentname)):
				convomessages = driver.find_elements_by_xpath('//div[@data-user-message="true"]/div[3]/div/div/div/p')
				if '?' not in str(convomessages[-1].text) and len(convomessages[-1].text.split()) <= 7:
					messageinput.send_keys(keys.null)
					for c in 'you got it :D':
						messageinput.send_keys(c)
					messageinput.send_keys(Keys.RETURN)
					return

			if [conts for conts in driver.find_elements_by_xpath('//h6') if 'TODAY' in conts.text or 'YESTERDAY' in conts.text]:
				return
			if nmessages <= 1:
				messageinput.send_keys(Keys.NULL)
				for c in greeting.format(studentname.split()[0].title()):
					messageinput.send_keys(c)
				messageinput.send_keys(Keys.RETURN)
				return
			lastcontact = [conts for conts in driver.find_elements_by_xpath('//h6') if str(datetime.now().year) in conts.text ][-1].text
			if (datetime.now() - datetime.strptime(lastcontact, '%B %d, %Y')).days > 7:
				messageinput.send_keys(Keys.NULL)
				for c in greeting.format(studentname.split()[0].title()):
					messageinput.send_keys(c)
				messageinput.send_keys(Keys.RETURN)
				return
	return