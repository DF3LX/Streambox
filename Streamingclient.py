from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
PATH = "P:\Home\Kirche\Streaming\Streambox\Pogramm\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://rk-solutions-streamc.de/hohenacker/livestream.html")
print(driver.title)
xpath = //*[@id="live"]/div[2]/div[1]/div[3]/svg[1]
search = driver.find_element_by_xpath(xpath)
search
print(search)
driver.maximize_window()


#driver.find_elements_by_class_name("fp-icon fp-playbtn").click()

time.sleep(5)

driver.quit()

