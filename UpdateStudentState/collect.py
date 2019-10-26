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




options = ChromeOptions()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--no-referrers')
options.add_argument('--user-data-dir=C:/Users/feng3245/AppData/Local/Google/Chrome/User Data')
driver = webdriver.Chrome(executable_path="c:/ChromeDriver/chromedriver.exe", chrome_options=options)

try:
    driver.get("https://auth.udacity.com/sign-in")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//img[@alt="google"]')))
    
    login = driver.find_element_by_xpath('//img[@alt="google"]')
    #temporarily not using it
    driver.execute_script("arguments[0].click();", login)
    #user = driver.find_element_by_xpath('//input[@type="email"]')
    #user.send_keys(Keys.NULL)
    #for c in 'axv@t.com':
    #    user.send_keys(c)
    #password = driver.find_element_by_xpath('//input[@type="password"]')
    #for c in 'derppass':
    #    password.send_keys(c)
    #driver.execute_script("arguments[0].click();",driver.find_element_by_xpath('//button[contains(text(),"Sign In")]'))
    time.sleep(5)
    driver.get("https://mentor-dashboard.udacity.com/mentorship/overview")
    time.sleep(30)
    students = [ste.text for ste in driver.find_elements_by_xpath('//p')]
    duedates = [duedate.text for duedate in driver.find_elements_by_xpath('//tr/td[5]')]
    enrolledstudents = [(s, d) for s, d in zip(students, duedates) if d != 'tbd']
    behindStudents = [es[0] for es in enrolledstudents if datetime.now() > datetime.strptime(es[1], '%b %d, %Y')]
    onTrackStudents = [es[0] for es in enrolledstudents if datetime.now() <= datetime.strptime(es[1], '%b %d, %Y')]
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    with open('../collect_exceptionss', 'w') as file:
        file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
    driver.quit()
    raise e
with open('../behindStudents', 'w') as file:
    file.write('|'.join(behindStudents))

with open('../onTrackStudents', 'w') as file:
    file.write('|'.join(onTrackStudents))

driver.quit()
