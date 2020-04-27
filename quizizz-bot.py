#!/usr/bin/env python3
import os, time, json, requests, sys, random, string, tkinter, subprocess, tempfile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#-------------------------------------------------------------------------#
global enabled
def randdelaygen(base,tf):
    if tf==True:
        mult=random.randint(15,50)
        delay=base+mult/10
    else:
        delay=base
    time.sleep(int(delay))
def waitForItem(driver, css, timeout=20):
    WebDriverWait(driver, timeout).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css)))

def find_answers(quizID):
    quizInfo = requests.get(f"https://quizizz.com/quiz/{quizID}/").json()
    answers = {}
    if "error" in quizInfo:
        print("[error] I couldn't find that quiz")
        exit()

    for question in quizInfo["data"]["quiz"]["info"]["questions"]:
        if question["type"] == "MCQ":
            if question["structure"]["options"][int(question["structure"]["answer"])]["text"] == "":
                # image answer
                answer = question["structure"]["options"][int(question["structure"]["answer"])]["media"][0]["url"]
            else:
                answer = question["structure"]["options"][int(question["structure"]["answer"])]["text"]
        elif question["type"] == "MSQ":
            # multiple answers
            answer = []
            for answerC in question["structure"]["answer"]:
                if question["structure"]["options"][int(answerC)]["text"] == "":
                    answer.append(question["structure"]["options"][int(answerC)]["media"][0]["url"])
                else:
                    answer.append(question["structure"]["options"][int(answerC)]["text"])
        questionID = question["structure"]["query"]["text"]
        answers[questionID.replace("&nbsp;"," ").replace(u'\xa0',u' ').rstrip().lower()] = answer.replace("&nbsp;"," ").rstrip().lower()
    return answers

def play(gamecode, name, randdelay):
    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'performance':'ALL' }
    driver = webdriver.Chrome(desired_capabilities=d)
    
    driver.get("https://quizizz.com/join/")
    print("[info] Starting game")
    waitForItem(driver,'.check-room-input')
    driver.find_element_by_css_selector('.check-room-input').send_keys(gamecode)
    driver.find_element_by_css_selector('.proceed-button').click()
    waitForItem(driver,'.check-player-input')
    driver.find_element_by_css_selector('.check-player-input').send_keys(name)
    driver.find_element_by_css_selector('.proceed-button').click()
    time.sleep(1)
    
    #find GameID
    print("[Info] Retrieving QuidID")
    with open('logs.txt', 'a') as f:
        for entry in driver.get_log('performance'):
            try:
                f.write(str(entry) + '\n')
            except Exception:
                pass
    with open('logs.txt', 'r') as inF:
        for line in inF:
            if 'recommend?quizId=' in line:
                s = line.split("recommend?quizId=",1)[1]
                GameID = s.split('"')[0]
                print("Found: " + GameID)
                print("You can visit https://quizizz.com/quiz/" + GameID + " for answer. (You will need a quizizz account)")
                break
    os.remove("logs.txt")
    #Random delay
    if randdelay[0].lower()=="y":
        enabled=True
    else:
        enabled=False
    #Continue play
    waitForItem(driver,'.skip-btn',timeout=20)
    time.sleep(0.5)
    driver.find_element_by_css_selector('.skip-btn').click()
    waitForItem(driver,'.game-start-btn',timeout=20)
    time.sleep(0.5)
    driver.find_element_by_css_selector('.game-start-btn').click()
    answers = find_answers(GameID)
    print("[info] answers found")
    time.sleep(2);
    while True:
        try:
            try:
                waitForItem(driver,'.question-text-color',timeout=20)
                waitForItem(driver,'.options-container',timeout=20)
                time.sleep(1)
            except TimeoutException:
                driver.quit()
                break
            try:
                questionAnswer = answers[driver.find_element_by_css_selector('.question-text-color').get_attribute('innerHTML').lower().replace("&nbsp;"," ")]
                choices = driver.find_element_by_css_selector('.options-container').find_elements_by_css_selector('.option')
                firstAnswer = True
                for answer in choices:
                    try:
                        if isinstance(questionAnswer, list):
                            # multiple select
                            if firstAnswer:
                                time.sleep(1)
                                firstAnswer = False
                            if answer.find_element_by_css_selector(".resizeable").get_attribute('innerHTML').lower() in questionAnswer:
                                answer.click()
                                time.sleep(4)
                                break
                        elif answer.find_element_by_css_selector(".resizeable").get_attribute('innerHTML').lower() == questionAnswer:
                            randdelaygen(0,enabled)
                            answer.click()
                            time.sleep(4)
                            break
                    except NoSuchElementException:
                        # Is an image
                        style = answer.find_element_by_css_selector(".option-image").get_attribute("style").lower()
                        if isinstance(questionAnswer, list):
                            # multiple select
                            for correctAnswer in questionAnswer:
                                if style in correctAnswer:
                                    answer.click()
                                    break
                        elif questionAnswer in style:
                            answer.click()
                            break
                if isinstance(questionAnswer, list):
                    driver.find_element_by_css_selector(".multiselect-submit-btn").click()
            except KeyError:
                print(driver.find_element_by_css_selector('.question-text-color').get_attribute('innerHTML').lower())
                for answer in driver.find_element_by_css_selector('.options-container').find_elements_by_css_selector('.option'):
                    print(answer.find_element_by_css_selector(".resizeable").get_attribute('innerHTML').lower())
                try:
                    print(answers[input("Manual search for answer - question >>> ").lower()])
                    input("Click the answer please then hit [enter]")
                except KeyError:
                    input("Manual search failed. Try clicking the correct answer then hit [enter]")
        except WebDriverException:
            try:
                driver.execute_script("location.reload()")
                followed_by = driver.execute_script(
                    "return window._sharedData.""entry_data.ProfilePage[0]."
                    "user.followed_by.count")
            except WebDriverException:
                print("Ignorable Error! If persists and question is not being answered, answer yourself")
                time.sleep(1)               
    driver.quit()

#CMD    
if __name__ == '__main__':
  
    play(input("#!/usr/bin/env python3
import os, time, json, requests, sys, random, string, tkinter, subprocess, tempfile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#-------------------------------------------------------------------------#
global enabled
def randdelaygen(base,tf):
    if tf==True:
        mult=random.randint(15,50)
        delay=base+mult/10
    else:
        delay=base
    time.sleep(int(delay))
def waitForItem(driver, css, timeout=20):
    WebDriverWait(driver, timeout).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css)))

def find_answers(quizID):
    quizInfo = requests.get(f"https://quizizz.com/quiz/{quizID}/").json()
    answers = {}
    if "error" in quizInfo:
        print("[error] I couldn't find that quiz")
        exit()

    for question in quizInfo["data"]["quiz"]["info"]["questions"]:
        if question["type"] == "MCQ":
            if question["structure"]["options"][int(question["structure"]["answer"])]["text"] == "":
                # image answer
                answer = question["structure"]["options"][int(question["structure"]["answer"])]["media"][0]["url"]
            else:
                answer = question["structure"]["options"][int(question["structure"]["answer"])]["text"]
        elif question["type"] == "MSQ":
            # multiple answers
            answer = []
            for answerC in question["structure"]["answer"]:
                if question["structure"]["options"][int(answerC)]["text"] == "":
                    answer.append(question["structure"]["options"][int(answerC)]["media"][0]["url"])
                else:
                    answer.append(question["structure"]["options"][int(answerC)]["text"])
        questionID = question["structure"]["query"]["text"]
        answers[questionID.replace("&nbsp;"," ").replace(u'\xa0',u' ').rstrip().lower()] = answer.replace("&nbsp;"," ").rstrip().lower()
    return answers

def play(gamecode, name, randdelay):
    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'performance':'ALL' }
    driver = webdriver.Chrome(desired_capabilities=d)
    
    driver.get("https://quizizz.com/join/")
    print("[info] Starting game")
    waitForItem(driver,'.check-room-input')
    driver.find_element_by_css_selector('.check-room-input').send_keys(gamecode)
    driver.find_element_by_css_selector('.proceed-button').click()
    waitForItem(driver,'.check-player-input')
    driver.find_element_by_css_selector('.check-player-input').send_keys(name)
    driver.find_element_by_css_selector('.proceed-button').click()
    time.sleep(1)
    
    #find GameID
    print("[Info] Retrieving QuidID")
    with open('logs.txt', 'a') as f:
        for entry in driver.get_log('performance'):
            try:
                f.write(str(entry) + '\n')
            except Exception:
                pass
    with open('logs.txt', 'r') as inF:
        for line in inF:
            if 'recommend?quizId=' in line:
                s = line.split("recommend?quizId=",1)[1]
                GameID = s.split('"')[0]
                print("Found: " + GameID)
                print("You can visit https://quizizz.com/quiz/" + GameID + " for answer. (You will need a quizizz account)")
                break
    os.remove("logs.txt")
    #Random delay
    if randdelay[0].lower()=="y":
        enabled=True
    else:
        enabled=False
    #Continue play
    waitForItem(driver,'.skip-btn',timeout=20)
    time.sleep(0.5)
    driver.find_element_by_css_selector('.skip-btn').click()
    waitForItem(driver,'.game-start-btn',timeout=20)
    time.sleep(0.5)
    driver.find_element_by_css_selector('.game-start-btn').click()
    answers = find_answers(GameID)
    print("[info] answers found")
    time.sleep(2);
    while True:
        try:
            try:
                waitForItem(driver,'.question-text-color',timeout=20)
                waitForItem(driver,'.options-container',timeout=20)
                time.sleep(1)
            except TimeoutException:
                driver.quit()
                break
            try:
                questionAnswer = answers[driver.find_element_by_css_selector('.question-text-color').get_attribute('innerHTML').lower().replace("&nbsp;"," ")]
                choices = driver.find_element_by_css_selector('.options-container').find_elements_by_css_selector('.option')
                firstAnswer = True
                for answer in choices:
                    try:
                        if isinstance(questionAnswer, list):
                            # multiple select
                            if firstAnswer:
                                time.sleep(1)
                                firstAnswer = False
                            if answer.find_element_by_css_selector(".resizeable").get_attribute('innerHTML').lower() in questionAnswer:
                                answer.click()
                                time.sleep(4)
                                break
                        elif answer.find_element_by_css_selector(".resizeable").get_attribute('innerHTML').lower() == questionAnswer:
                            randdelaygen(0,enabled)
                            answer.click()
                            time.sleep(4)
                            break
                    except NoSuchElementException:
                        # Is an image
                        style = answer.find_element_by_css_selector(".option-image").get_attribute("style").lower()
                        if isinstance(questionAnswer, list):
                            # multiple select
                            for correctAnswer in questionAnswer:
                                if style in correctAnswer:
                                    answer.click()
                                    break
                        elif questionAnswer in style:
                            answer.click()
                            break
                if isinstance(questionAnswer, list):
                    driver.find_element_by_css_selector(".multiselect-submit-btn").click()
            except KeyError:
                print(driver.find_element_by_css_selector('.question-text-color').get_attribute('innerHTML').lower())
                for answer in driver.find_element_by_css_selector('.options-container').find_elements_by_css_selector('.option'):
                    print(answer.find_element_by_css_selector(".resizeable").get_attribute('innerHTML').lower())
                try:
                    print(answers[input("Manual search for answer - question >>> ").lower()])
                    input("Click the answer please then hit [enter]")
                except KeyError:
                    input("Manual search failed. Try clicking the correct answer then hit [enter]")
        except WebDriverException:
            try:
                driver.execute_script("location.reload()")
                followed_by = driver.execute_script(
                    "return window._sharedData.""entry_data.ProfilePage[0]."
                    "user.followed_by.count")
            except WebDriverException:
                print("Ignorable Error! If persists and question is not being answered, answer yourself")
                time.sleep(1)               
    driver.quit()

#CMD    
if __name__ == '__main__':
  
    play(input("047579>>> "), input("username >>> "), input("Enable Delay? >>>")) >>> "), input("username >>> "), input("Enable Delay? >>>")) 

