from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests

CHROME_DRIVER_PATH = r"C:\Development\chromedriver-win64\chromedriver.exe"
FORM_LINK = "form_link"
ZILLOW_LINK="write the link from which you want to scrap the data"
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7"
}
response = requests.get(ZILLOW_LINK, headers=HEADERS)
zillow_html = response.text

soup = BeautifulSoup(zillow_html, "html.parser")
price_element = soup.select("article div div span")
price_list = []
for element in price_element:
    if element.get("data-test")=="property-card-price":
        print(element.getText().split('+'))
        price_list.append(element.getText().split('+')[0])
        # if '+' in element.getText():
        #     price = element.getText().split('+')[0]
        #     price_list.append(price)
        # else:
        #     price = element.getText().split('/')[0]
        #     price_list.append(price)


address_element = soup.find_all(name="address")
address_list = [element.getText() for element in address_element]
property_link_element = soup.select("li article div a")
property_links=[]

for i in property_link_element:
    if f"https://www.zillow.com{i.get('href')}" not in property_links:
        print(i.get('href'))
        if "https" in i.get('href'):
            property_links.append(i.get('href'))
        else:
            property_links.append(f"https://www.zillow.com{i.get('href')}")

property_links=list(dict.fromkeys(property_links))

print(len(price_list))
print(len(property_links), property_links)
print(len(address_list), address_list)
service = ChromeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)
for i in range(len(price_list)):
    price = price_list[i]
    address = address_list[i]
    property_link = property_links[i]
    driver.get(FORM_LINK)
    time.sleep(3)
    all_answers=driver.find_elements(By.CLASS_NAME,"whsOnd")
    address_answer = all_answers[0]

    address_answer.send_keys(address)
    time.sleep(2)

    price_answer=all_answers[1]

    price_answer.send_keys(price)
    time.sleep(2)


    property_link_answer=all_answers[2]
    property_link_answer.send_keys(property_link)
    time.sleep(2)
    submit_button=driver.find_element(By.CLASS_NAME,"NPEfkd")
    submit_button.click()
    time.sleep(3)

while True:
    pass




