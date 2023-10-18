'''Using Python selenium and the URL https://www.cowin.gov.in you have to:-
1)Click on the Create FAQ and partners: anchor tags present on the Home page open two new windows.
2) Now, you have to fetch the opened windows/ Frame Id and display the same on the console.
3)kndly close the two windows and come back to the Hoe page also.'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Cowin:

    def __init__(self):
        self.url = "https://www.cowin.gov.in/"
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.original_window = None
        self.windows = []

    def open_website(self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
            sleep(4)
        except NoSuchElementException as selenium_error:
            print(f"Opening website {self.url} failed: {selenium_error}")

    def shutdown(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error while shutting down WebDriver: {str(e)}")

    # 1)Click on the Create FAQ and partners: anchor tags present on the Home page open two new windows.
    def click_button(self):
        try:
            # Wait for the FAQ link to be clickable
            faq = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "FAQ")))
            faq.click()
            sleep(2)
            # Wait for the Partners link to be clickable
            partner = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navbar"]/div[4]/div/div[1]/div/nav/div[3]/div/ul/li[5]/a')))
            partner.click()
            sleep(2)
        except NoSuchElementException as selenium_error:
            print(f"Clicking links on {self.url} failed: {selenium_error}")

    #2) Fetching the opened windows/ Frame Id and display the same on the console.
    def window_id(self):
        try:
            self.original_window = self.driver.current_window_handle
            self.windows = self.driver.window_handles
            for window in self.windows:
                if window != self.original_window:
                    self.driver.switch_to.window(window)     # fetching the window on the screen
                    sleep(3)
                    current_url = self.driver.current_url
                    if current_url == "https://www.cowin.gov.in/faq" :
                        print("\t FAQ URL : ",current_url, "\n\t Window ID: ",window)   # Display Fetched url and window ID
                    elif current_url == "https://www.cowin.gov.in/our-partner":
                        print("\t Partners: ",current_url," \n\t Window ID : ", window)
                
                sleep(3)
            self.driver.switch_to.window(self.original_window)
        except NoSuchElementException as selenium_error:
            print(f"switching to window{window} or closing the window failed exception{selenium_error}")

    #closing the two windows and come back to the Hoe page also
    def close_window(self):
        try:
            
            for window in self.windows:
                if window != self.original_window:
                    self.driver.switch_to.window(window)
                    sleep(3)
                    self.driver.close()
                    print(f"Closing window successfull")

            self.driver.switch_to.window(self.original_window)
        except NoSuchElementException as selenium_error:
            print(f"Closing window {window} error {selenium_error}")


# requirements of the question
try:
    cowin = Cowin()

    cowin.open_website()

    cowin.click_button() 

    cowin.window_id()

    cowin.close_window()
finally:
    cowin.shutdown()
