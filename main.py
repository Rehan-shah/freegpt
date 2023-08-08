from os import listdir
from flask import Flask , request
import time
from requests import options
from selenium.webdriver.common.by import By
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
import pyperclip
app = Flask(__name__)
import uuid

list = {}


def send_prompts(prompt , driver):
    print(prompt)
    time.sleep(5)

    pyperclip.copy(prompt)
    textarea = driver.find_element(By.XPATH , '//*[@id="app"]/div[1]/div/div[2]/form/div/div/textarea')
    textarea.send_keys(Keys.COMMAND + "v")
    time.sleep(5)
    enter_btn = driver.find_element(By.XPATH , '//*[@id="app"]/div[1]/div/div[2]/form/div/button')
    enter_btn.click()

    time.sleep(3)
    while True:
        time.sleep(2)
        try : 
            countiune_btn = driver.find_element(By.XPATH ,'//*[@id="app"]/div[1]/div/div[2]/div[1]/button')
            countiune_btn.text
        except:
            break;

    elements = driver.find_elements(By.XPATH , "//div[@class='prose max-w-none dark:prose-invert max-sm:prose-sm prose-headings:font-semibold prose-h1:text-lg prose-h2:text-base prose-h3:text-base prose-pre:bg-gray-800 dark:prose-pre:bg-gray-900']")
    text = elements[-1].text

    try :
        code = driver.find_elements(By.TAG_NAME , "code")
        print("jell")
        code_text = code[-1].text
        code_attr = code[-1].get_attribute("class")
        text = text.replace(code_text , f"{code_attr}```" + code_text + "```")

    finally:
        return text



@app.get('/start')
def start(): 
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("https://gpt-gm.h2o.ai/")
    login_btn = driver.find_element(By.XPATH , '//*[@id="app"]/div/div[1]/div/div/div/form/button')
    login_btn.click()
    id = uuid.uuid1()
    list[str(id)] = driver
    print(list)
    return {"id" : id}, 200



@app.post("/chat")
def chatgpt():
    data = request.json
    print(list)
    try : 
        prompt = data["prompt"]
        id = data["id"]
    except KeyError:
        return {"error": "No prompt provided"}, 400

    try : 
        driver = list[id]
    except KeyError:
        return {"error": "Thread not on , pls add a thread"}, 400

    return {"message": send_prompts(prompt , driver=driver)}, 200

@app.post("/stop")
def stop():
    data = request.json
    try : 
        id = data["id"]
        driver = list[id]
    except KeyError:
        return {"error": "Not a eligible id provided"}, 400
    driver.quit()
    del list[id]
    return {"message": "Thread stopped"}, 200

@app.post("/instruct")
def instrcut():
    data = request.json
    try : 
        prompt = data["prompt"]
    except KeyError:
        return {"error": "No prompt provided"}, 400
    driver = webdriver.Edge()
    driver.get("https://gpt-gm.h2o.ai/")
    login_btn = driver.find_element(By.XPATH , '//*[@id="app"]/div/div[1]/div/div/div/form/button')
    login_btn.click()
    msg = send_prompts(prompt , driver)
    driver.quit()
    return {"message": msg}, 200
    


@app.errorhandler(404) 
def invalid_route(e): 
    return {"error": "Invalid route"}, 404


if __name__ == "__main__":
    app.run(debug=True)
