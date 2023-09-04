#!/usr/bin/python3
from typing import List

# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpCond
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

from jw_page_navigation.PageNavigator import PageNavigator

class MailingHelper(PageNavigator):

    URL = 'https://mail.jwpub.org/owa/#path=/mail'

    async def load(self):
        self.driver.get(self.URL)
        await self._waitForUserLoggedIn()
        
    async def startNewMail(self):
        newDropdown = self.navWait.until(ExpCond.presence_of_element_located((By.XPATH, '//button[contains(@autoid,"_fce_1")]')))
        newDropdown.click()
        
    async def setBody(self, html):
        bodyEditor = self.navWait.until(ExpCond.presence_of_element_located((By.XPATH, '//div[contains(@autoid,"_z_n")]/child::div')))
        self.driver.execute_script(f"arguments[0].innerHTML = '{html}';", bodyEditor)
        bodyEditor.send_keys(' ')
        
        # String myText = (String) Toolkit.getDefaultToolkit().getSystemClipboard().getData(DataFlavor.stringFlavor); // extracting the text that was copied to the clipboard
        # input.sendKeys(myText);//passing the extracted text to the text field
        # input.send_keys("My text")
        

    async def setSubject(self, subject: str):
        subjectInput = self.navWait.until(ExpCond.presence_of_element_located((By.XPATH, '//input[contains(@autoid,"_mcp_c")]')))
        subjectInput.send_keys(subject)
        
    async def setTo(self, receiver: List[str]):
        accInput = self.navWait.until(ExpCond.presence_of_element_located((By.XPATH, '//input[contains(@autoid,"_fp_5")]')))
        accInput.send_keys('; '.join(receiver))
