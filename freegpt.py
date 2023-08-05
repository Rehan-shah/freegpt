from typing import Any, List, Mapping, Optional
from selenium import webdriver

import time

from selenium.webdriver.common.by import By




driver = webdriver.ChromiumEdge()



driver.get("https://gpt-gm.h2o.ai/")

time.sleep(7)

login_btn = driver.find_element(By.XPATH , "/html/body/div[2]/div/div/div/form/button")
login_btn.click()

time.sleep(4)


def send_prompts(prompt):
    time.sleep(2)
    textarea = driver.find_element(By.XPATH , '//*[@id="app"]/div[1]/div/div[2]/form/div/div/textarea')
    textarea.send_keys(prompt)

    enter_btn = driver.find_element(By.XPATH , '//*[@id="app"]/div[1]/div/div[2]/form/div/button')
    enter_btn.click()

    time.sleep(3)
    while True:
        time.sleep(1)
        try : 
            countiune_btn = driver.find_element(By.XPATH ,'//*[@id="app"]/div[1]/div/div[2]/div[1]/button')
            countiune_btn.text
        except:
            break;

    element = driver.find_elements(By.XPATH , "//div[@class='prose max-w-none dark:prose-invert max-sm:prose-sm prose-headings:font-semibold prose-h1:text-lg prose-h2:text-base prose-h3:text-base prose-pre:bg-gray-800 dark:prose-pre:bg-gray-900']")
    
    return element[-1].text



print("FREE GPT")

on = True
while(on):
    print(send_prompts(input('Enter prompt:')))
