#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import random
import pyautogui
import csv
import os
from mysetup import MY_USER, MY_PASSWORD

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))+'/'
csv_path = ROOT_DIR+'EditorApp/posts.csv'

def image_name():
    # open the CSV file in read mode
    with open(csv_path, 'r') as file:
        # create a CSV reader object
        reader = csv.reader(file)
        # convert the CSV file to a list of lists
        rows = list(reader)
        for filename, caption in rows:
            return str(filename)

def caption():
    # open the CSV file in read mode
    with open(csv_path, 'r') as file:
        # create a CSV reader object
        reader = csv.reader(file)
        # convert the CSV file to a list of lists
        rows = list(reader)
        for filename, caption in rows:
            return str(caption)     

def delete_posted_image():
    # open the CSV file in read mode
    with open(csv_path, 'r') as file:
        # create a CSV reader object
        reader = csv.reader(file)
        # convert the CSV file to a list of lists
        rows = list(reader)
    # delete the first row of the list
    del rows[0]
    # open the CSV file in write mode
    with open(csv_path, 'w', newline='') as file:
        # create a CSV writer object
        writer = csv.writer(file)
        # write the remaining rows to the CSV file
        writer.writerows(rows)    

def short():
    time_short = random.randint(1, 4)
    return time_short

def mid():
    time_mid = random.randint(5, 7)
    return time_mid

def longer():
    time_long = random.randint(8, 10)
    return time_long


def images_path():
    image_path = ''
    for char in ROOT_DIR:
        if char == '/':
            image_path += '&'
        else:
            image_path += char   
    return str(image_path) + 'EditorApp&static&images&' 

image_path = images_path() + image_name()

s = Service(ROOT_DIR+'chromedrive')
options = Options()
driver = webdriver.Chrome(service= s, options=options)

# create action chain object
action = ActionChains(driver)

driver.get('https://www.instagram.com/')
print('Opening instagram.com')
time.sleep(longer())

username = driver.find_element('xpath',
                               '//*[@id="loginForm"]/div/div[1]/div/label/input')
username.send_keys(MY_USER)
print('username OK')
time.sleep(short())

password = driver.find_element('xpath',
                               '//*[@id="loginForm"]/div/div[2]/div/label/input')
password.send_keys(MY_PASSWORD)
print('password OK')
time.sleep(short())

password.send_keys(Keys.ENTER)
print('Login successful')
time.sleep(longer())

new_post = driver.find_element(by=By.XPATH, value="//*[local-name()='svg' and @aria-label='New post']")
new_post.click()
print('New post activated')
time.sleep(mid())

upload_button = driver.find_element(by=By.XPATH, value="//button[text()='Select from computer']")
upload_button.click()
print('Select from computer button')
time.sleep(mid())


with pyautogui.hold('shift'):
        pyautogui.hotkey('command', 'g')
time.sleep(short())
print('Wrinting image path')
pyautogui.write(image_path)
time.sleep(short())
pyautogui.press('enter')
time.sleep(short())
pyautogui.press('enter')
print('Image selected')
time.sleep(mid())

#NEXT button 1
next_1 = driver.find_element(by=By.XPATH, value="//div[@role='button' and text()='Next']")
next_1.click()
print('Next button 1')
time.sleep(short())

next_2 = driver.find_element(by=By.XPATH, value="//div[@role='button' and text()='Next']")
next_2.click()
print('Next button 2')
time.sleep(short())

add_text = driver.find_elements(by=By.XPATH, value="//*[local-name()='div' and @aria-label='Write a caption...']")[0]
ActionChains(driver).move_to_element(add_text).click().send_keys(caption()).perform()
print('Caption added')
time.sleep(mid())

share_button = driver.find_element(by=By.XPATH, value="//div[@role='button' and text()='Share']")
ActionChains(driver).move_to_element(share_button).click().perform()
print('Image shared sucsessfully')
time.sleep(longer())

#close_button = driver.find_element(by=By.XPATH, value="//div[@role='button' and @aria-label='Close']")
close_button = driver.find_element(by=By.XPATH, value="//*[local-name()='svg' and @aria-label='Close']")
close_button.click()
print('Post shared closed')
time.sleep(mid())

print(image_name() + ' deleted')
#Delete image and update CSV
os.remove(ROOT_DIR+'EditorApp/static/images/'+ image_name())
delete_posted_image()
print('Cleaning last post')
time.sleep(mid())

print('Closing the browser')
# Close the webdriver
driver.quit()



#pyautogui.press('escape')
#time.sleep(mid())

