# Auto Login - Cisco
import netifaces
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

import time
import os, platform

import logging
from logging import FileHandler, StreamHandler, Formatter

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))

fh = FileHandler('wifipump.log')
fh.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))

logger.addHandler(handler)
logger.addHandler(fh)

logger.debug("Auto Login - Cisco")




class AutoLogin:


    def __init__(self, username, password, ip):
        self.username = username
        self.password = password
        self.ip = ip
        s = Service('/home/q/PycharmProjects/pump/chromedriver')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(service=s, options=chrome_options) # select browser


    def CloseBrowser(self):
        self.driver.quit()
        logger.debug("[Status] : Close browser")

    def is_interface_up(self, wifiinterface):
        addr = netifaces.ifaddresses(wifiinterface)
        return netifaces.AF_INET in addr

    def Login(self):

       try:
            if self.is_interface_up("wls16f2"):
                driver = self.driver
                address = self.ip
                driver.get(address)
                try:
                    username_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'username')))
                    username_element.clear()
                    username_element.send_keys(self.username)
                    password_element = driver.find_element("xpath","//input[@name='password'][@type='Password']")
                    password_element.clear()
                    password_element.send_keys(self.password)
                    password_element.send_keys(Keys.RETURN)
                except:
                    logger.info("[Status] : Site is wrong")
                #driver.quit()
            else:
                logger.info("[Status] : Interface have not ip")
       except:
          print("[Status] : Interface is not present(up)")

    def LoginCheck(self):
        print("[Status] : Login Check")
        hostname = "77.88.8.8" # ip address to ping test 
        response = os.system("ping -c 5 -W 5 77.88.8.8")
        if response == 0:
            pingstatus = True
        else:
            pingstatus = False
        return pingstatus
        
# Setting ("username", "password", "hotspot_ip-address")
Auto = AutoLogin("", "", "http://1.1.1.1/")

while True:
    if Auto.LoginCheck():
        print("[Status] : Already login")
    else:
        logger.info("[Status] : Not logged in")
        Auto.Login()

