#!/usr/bin/python3
from subprocess import getoutput
import asyncio
from os import makedirs

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpCond
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

class PageNavigator:

    URL = 'https://jw.org/de'
    userName = None
    password = None
    driver = None

    def __init__(self, firefoxProfilePath: str, downloadDir: str = None):
        options = Options()
        snapFirefoxBinary = getoutput("find /snap/firefox -name firefox").split("\n")[-1]
        geckodriverBinary = getoutput("find /snap/firefox -name geckodriver").split("\n")[-1]
        if "No such file or directory" not in snapFirefoxBinary:
            print(f"Using snap Firefox. Binary: {snapFirefoxBinary}, Gecko binary {geckodriverBinary}")
            options.binary_location = snapFirefoxBinary
        else:
            # options.binary_location = "/usr/bin/firefox"
            geckodriverBinary = None
            print("Using regular (non snap) Firefox")
        # options.add_argument("--kiosk") 
        print("firefoxProfilePath "+firefoxProfilePath)
        print("In case of firefox startup problems: Delete profile dir. Run 2 times, first start on new profile may fail.")
        makedirs(firefoxProfilePath, exist_ok=True, mode=0o700)
        ## webdriver.FirefoxProfile(firefoxProfilePath) is ignoring profile path on some snap firefox versions, use -profile arg instead
        options.add_argument("-profile")
        options.add_argument(firefoxProfilePath)
        ## To check if profile path is used, open about:support in firefox

        options.set_preference('browser.download.folderList', 2) # custom location
        options.set_preference('browser.download.manager.showWhenStarting', False)
        options.set_preference('browser.link.open_newwindow', 3) # new tab in current window
        if downloadDir is not None:
            options.set_preference('browser.download.dir', downloadDir)
            # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        
            # handle print dialog, block system dialog and save as pdf
            options.set_preference("print_printer", "Mozilla Save to PDF")
            options.set_preference("print.always_print_silent", True)
            options.set_preference("print.show_print_progress", False)
            options.set_preference('print.save_as_pdf.links.enabled', True)
            options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)
            options.set_preference('print.printer_Mozilla_Save_to_PDF.print_to_filename',
                                   downloadDir+"/printed.pdf")
        options.set_preference("browser.startup.page", 0)
        self.driver = webdriver.Firefox(
            service = Service(executable_path = geckodriverBinary),
            options = options)
        self.navWait = WebDriverWait(self.driver, 20)

    def setCredentials(self, userName, password):
        """
        userName and password may be None, will wait for manual login
        """
        self.userName = userName
        self.password = password

    async def navigateTo(self, url: str):
        self.driver.get(url)

    async def navigateToHub(self):
        """
        navigates to hub.jw.org/home/en
        """
        self.driver.get(self.URL)
        asyncio.create_task(self._acceptCookie())
        
        # acceptCookie()
        loginBtn = self.driver.find_element(By.XPATH, '//a[contains(@href,"hub.jw.org/home/") and contains(@class,"siteFeaturesItem")]')
        loginBtn.click()
        # login will open new tab
        self.driver.switch_to.window(self.driver.window_handles[1])
        await self._waitForUserLoggedIn()

    async def _expandSideNav(self):
        contextNavBtn = self.driver.find_element(By.CLASS_NAME, "side-nav__context-link")
        if not contextNavBtn.is_displayed():
            self.driver.find_element(By.CLASS_NAME, "top-nav__hamburger").click()
        self.navWait.until(ExpCond.presence_of_element_located((By.CLASS_NAME, "side-nav__context-link")))

    async def _navWithBtnForUrl(self, urlPart, className = None):
        if (className is not None):
            query = '//a[contains(@href,"'+urlPart+'") and contains(@class,"'+className+'")]'
        else:
            query = '//a[contains(@href,"'+urlPart+'")]'
        self.navWait.until(ExpCond.presence_of_element_located((By.XPATH, query))).click()

    async def _waitForUserLoggedIn(self):
        loginWait = WebDriverWait(self.driver, 120);
        hubStartPageCond = ExpCond.presence_of_element_located((By.XPATH, '//h1[contains(@class,"top-nav__title")]'))
        mailerStartPageCond = ExpCond.presence_of_element_located((By.XPATH, '//div[contains(@class,"o365cs-nav-topItem")]'))
        ## wait for login prompt or any of start-page items if already logged in
        inputOrTitle = loginWait.until(ExpCond.any_of(
            # hub is username, mailer is userNameInput
            ExpCond.element_to_be_clickable((By.XPATH, '//input[@autocomplete="username" or @id="userNameInput"]')),
            hubStartPageCond,
            mailerStartPageCond));

        if inputOrTitle.tag_name == "input":
            if self.userName is not None:
                usernameInput = self.driver.find_element(By.XPATH, '//input[@autocomplete="username" or @id="userNameInput"]')
                usernameInput.send_keys(self.userName)
                # hub is submit-button, mailer is nextButton
                self.driver.find_element(By.XPATH, '//*[@id="submit-button" or @id="nextButton"]').click()
            print("##### Please login now! #####")
            loginWait.until(hubStartPageCond)
            print("Login complete")
        else:
            print("Already logged in.")

    async def _acceptCookie(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            consentBtn = wait.until(ExpCond.presence_of_element_located((By.CLASS_NAME, 'lnc-acceptCookiesButton')))
            consentBtn.click()
        except Exception:
            print("No cookie banner found")
