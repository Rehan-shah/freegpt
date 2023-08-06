from flask import Flask , request
import time
from selenium.webdriver.common.by import By
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
import pyperclip
app = Flask(__name__)


driver = webdriver.Edge()



driver.get("https://gpt-gm.h2o.ai/")


login_btn = driver.find_element(By.XPATH , '//*[@id="app"]/div/div[1]/div/div/div/form/button')
login_btn.click()




def send_prompts(prompt):
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

    element = driver.find_elements(By.XPATH , "//div[@class='prose max-w-none dark:prose-invert max-sm:prose-sm prose-headings:font-semibold prose-h1:text-lg prose-h2:text-base prose-h3:text-base prose-pre:bg-gray-800 dark:prose-pre:bg-gray-900']")
    print("done") 
    return element[-1].text





@app.post("/chatgpt")
def chatgpt():
    data = request.json
    try : 
        prompt = data["prompt"]
    except KeyError:
        return {"error": "No prompt provided"}, 400

    return {"message": send_prompts(prompt)}, 200

@app.errorhandler(404) 
def invalid_route(e): 
    return {"error": "Invalid route"}, 404


if __name__ == "__main__":
    app.run(debug=True)
