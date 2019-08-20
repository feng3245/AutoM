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
    exclude = []
    with open('../excludes', 'r') as file:
        exclude = file.read().replace('\n', '').split('|')
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
    try:
        driver.get("https://hub.udacity.com/")
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
        
    except Exception as e:
        driver.get("https://hub.udacity.com/")
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))

    time.sleep(20)
    studentlinks = driver.find_elements_by_xpath('//a')
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

    try:
        for sl in studentlinks:
            try:
                driver.get(sl)
                time.sleep(5)
                WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Feng L. profile image"]')))
                if driver.find_element_by_xpath('//p[contains(text(),"Mentee")]'):
                    studentname = driver.find_element_by_xpath('//h2').text
                    if studentname not in exclude and studentname not in visited:
                        print(studentname)
                        visited.append(studentname)
                        WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, '//div[@data-user-message="true"]')))
                        nmessages = len(driver.find_elements_by_xpath('//div[@data-user-message="true"]'))
                        messageinput = driver.find_element_by_xpath('//textarea[@id="userInput"]')
                        
                        if nmessages == 2 and driver.find_elements_by_xpath('//a[contains(text(),"{0}.")]'.format(studentname)):
                            print(studentname + ' first correspondence')
                            convomessages = driver.find_elements_by_xpath('//div[@data-user-message="true"]/div[3]/div/div/div/p')
                            if '?' not in str(convomessages[-1].text) and len(convomessages[-1].text.split()) <= 7:
                                messageinput.send_keys(keys.null)
                                for c in 'you got it :D':
                                    messageinput.send_keys(c)
                                messageinput.send_keys(Keys.RETURN)
                                continue
                        if [conts for conts in driver.find_elements_by_xpath('//h6') if 'TODAY' in conts.text or 'YESTERDAY' in conts.text]:
                            continue
                        if nmessages <= 1:
                            print(studentname + ' is new')
                            messageinput.send_keys(Keys.NULL)
                            for c in greeting.format(studentname.split()[0].title()):
                                messageinput.send_keys(c)
                            messageinput.send_keys(Keys.RETURN)
                            continue
                        lastcontact = [conts for conts in driver.find_elements_by_xpath('//h6') if str(datetime.now().year) in conts.text ][-1].text
                        if (datetime.now() - datetime.strptime(lastcontact, '%B %d, %Y')).days > 7:
                            messageinput.send_keys(Keys.NULL)
                            for c in greeting.format(studentname.split()[0].title()):
                                messageinput.send_keys(c)
                            messageinput.send_keys(Keys.RETURN)
                            continue
                            print(studentname + ' hasn\'t been contacted for a while is new')
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                with open('../exceptionss', 'w') as file:
                    file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
                badlinks.append(sl)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        with open('../exceptionss', 'w') as file:
            file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
        driver.close()
        raise e
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    with open('../exceptionss', 'w') as file:
        file.write(''+str(e)+' ' + str(exc_tb.tb_lineno))
    driver.close()
    raise e
with open('../badlinks', 'w') as file:
    file.write('|'.join(badlinks))

driver.close()
