'''Using Python Selenium and the URL https://labour.gov.in/ and do the following tasks given below:-
1.) Go to the menu whose name is "Documents" and "Download the monthly progress report.
2.) Go to the menu whose name is "media , where you will find a sib-menu  whose name is :photo Gallery. 
Your task is to sownload the 10 photos from the webpage and store them in a folder.
 kindly create tyhe folder using Python only.'''
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import os
import requests
import shutil
from selenium.common.exceptions import WebDriverException
from time import sleep

class Labour:

    def __init__(self):
        self.url = "https://labour.gov.in/"
        self.download_folder = "E:\\Automationtesting\\Task\\Task\\Default_Downloads" # Setting default download folder
        os.makedirs(self.download_folder, exist_ok=True)
        self.set_firefox_options()
        self.driver = None

    def set_firefox_options(self):
        self.options = Options()
        self.options.set_preference("browser.download.folderList", 2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", self.download_folder)
        self.options.set_preference("browser.download.useDownloadDir", True)
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        self.options.set_preference("pdfjs.disabled", True)

    def open_url(self):
        try:
            self.driver = webdriver.Firefox(options=self.options, service=Service(GeckoDriverManager().install()))
            self.driver.maximize_window()
            self.driver.get(self.url)
            print(f"Opening URL successful")
            sleep(4)
        except WebDriverException as e:
            print(f"Error opening URL: {e}")

    def click_document(self):
        try:
            # Selecting new folder for downloading pdf monthly reports
            self.download_folder = "E:\\Automationtesting\\Task\\Task\\Download_pdf"       
            os.makedirs(self.download_folder, exist_ok=True)
            self.set_firefox_options() 

            element_document = self.driver.find_element(By.XPATH, '//*[@id="nav"]/li[7]/a')
            monthly_prog_report = self.driver.find_element(By.XPATH, '//*[@id="nav"]/li[7]/ul/li[2]/a')
            ActionChains(self.driver)\
                .move_to_element(element_document)\
                .pause(3)\
                .move_to_element(monthly_prog_report)\
                .click()\
                .perform()
            print(f"Clicking August month report successful")
            sleep(5)

            report = self.driver.find_element(by=By.XPATH, value='/html/body/section[3]/div/div/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/a')
            ActionChains(self.driver).move_to_element(report).click().perform()

            alert = self.driver.switch_to.alert
            alert.accept()
            print(f"PDF report downloaded successfully in folder: {self.download_folder}")

        except WebDriverException as e:
            print(f"Error clicking document: {e}")


    def click_media_photogallery(self):
        try:
            element_media = self.driver.find_element(By.XPATH, '/html/body/nav/div/div/div/ul/li[10]/a')
            element_phot_gallery = self.driver.find_element(By.XPATH, '/html/body/nav/div/div/div/ul/li[10]/ul/li[2]/a')
            ActionChains(self.driver).move_to_element(element_media).move_to_element(element_phot_gallery).click().perform()
            print("Successfully clicked photo gallery")
            sleep(4)
            self.image_elem()
        except WebDriverException as e:
            print(f"Error clicking media photo gallery: {e}")

    def image_elem(self):
        try:
            # Selecting optinons for Downloading image files
            self.download_folder = "E:\\Automationtesting\\Task\\Task\\Download_Image"        
            os.makedirs(self.download_folder, exist_ok=True)
            self.set_firefox_options()

            image_url_lst = []
            image_elements = self.driver.find_elements(By.XPATH, '//tbody/tr/td/div/div/img[@src]')
            for image_element in image_elements:
                source_url = image_element.get_attribute("src")
                image_url_lst.append(source_url)

            image_name_lst = []
            image_names = self.driver.find_elements(By.XPATH, '//tbody/tr/td/div/span/a')
            for image_name in image_names:
                image_text = image_name.text
                sanitized_name = self.sanitize_image_name(image_text)
                image_name_lst.append(sanitized_name)

            print("Name sanitized successfully")

            for i in range(10):
                self.download_image(image_url_lst[i], image_name_lst[i])
                print(f"{i+1} {image_url_lst[i]}, {image_name_lst[i]}")
                
        except WebDriverException as selenium_error:
            print(f"Error processing image elements: {selenium_error}")

    def sanitize_image_name(self, image_name):
        sanitized_name = image_name.replace(' ', '_')
        sanitized_name = ''.join(c for c in sanitized_name if c.isalnum() or c in ('-', '_'))
        return sanitized_name

    def download_image(self, image_url, image_name):
        try:
            image_name = f"{image_name}.jpg"
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(os.path.join(self.download_folder, image_name), 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                print(f"Downloaded image '{image_name}' successfully")
        except (requests.RequestException, OSError) as e:
            print(f"Error downloading image: {e}")

    def shutdown(self):
        if self.driver:
            self.driver.quit()
    

try:
    labour = Labour()

    labour.open_url()

    labour.click_document()

    labour.click_media_photogallery()

finally:
    labour.shutdown()
