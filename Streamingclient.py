from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.INPUT)
GPIO.setup(24, GPIO.OUT)

PATH = "P:\Home\Kirche\Streaming\Streambox\Pogramm\chromedriver.exe"
driver = webdriver.Chrome(PATH)

while True:
    while GPIO.input(23) == 0:
    
    driver.get("https://rk-solutions-streamc.de/hohenacker/livestream.html")
    driver.maximize_window()
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]").click()
    
    while GPIO.input(23) == 1:
    
    status = 0
    while GPIO.input(23) == 0:
        GPIO.output(24, status)
        time.sleep(1)
        if status == 0: status = 1
        else status = 0
        
    driver.quit()
        
    while GPIO.input(23) == 1:


