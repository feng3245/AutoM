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
from common import setup_driver, upload_to_aws
import json

driver = setup_driver(sys.argv[1])
try:
	driver.get(sys.argv[2])
	WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"freebirdFormviewerViewItemsTextShortText freebirdFormviewerViewItemsTextDisabledText freebirdThemedInput")]')))
	requesterInfo = {}
	with open('../requesterInfo', 'r') as file:
		requesterInfo = eval(file.read())
	numResponses = int(driver.find_elements_by_xpath('//div[contains(@class,"freebirdFormeditorViewResponsesNavigationPositionText")]')[-1].get_attribute('innerHTML'))
	for _ in range(numResponses):
		WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"freebirdFormviewerViewItemsTextShortText freebirdFormviewerViewItemsTextDisabledText freebirdThemedInput")]')))
		answeredInfo = driver.find_elements_by_xpath('//div[contains(@class,"freebirdFormviewerViewItemsTextShortText freebirdFormviewerViewItemsTextDisabledText freebirdThemedInput")]')
		requesterInfo[answeredInfo[-1].get_attribute('innerHTML')] = [answeredInfo[0].get_attribute('innerHTML').rstrip('.'), answeredInfo[1].get_attribute('innerHTML')]
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//div[contains(@aria-label, "Next response")]'))
	with open('../requesterInfo', 'w') as file:
		file.write(json.dumps(requesterInfo))
	upload_to_aws('../requesterInfo', 'requester-info', 'requesterInfo', sys.argv[3], sys.argv[4])
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	with open('../requesterUpdateExceptions', 'w') as file:
		file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))

	driver.quit()

driver.quit()
