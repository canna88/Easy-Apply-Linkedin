import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import re
import json


class EasyApplyLinkedin:
    
    def __init__(self,data):
        """Parameter initialization"""
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Chrome(data['driver_path'])
    
    #This function click
    def func_click(self, time_sleep, name, path_a):
        try:
            time.sleep(time_sleep)
            label = str(f'{name}')
            name = self.driver.find_element_by_xpath(path_a)
            name.click()
            print(f"{label}: found")
        except NoSuchElementException:
            time.sleep(time_sleep)
            print(f"{label}: not found!")

    #This function click and write
    def func_click_write(self, credential,time_sleep, name, path_a):
        try:
            time.sleep(time_sleep)
            label = str(f'{name}')
            name = self.driver.find_element_by_xpath(path_a)
            name.click()
            name.clear()
            name.send_keys(credential)
            print(f"{label}: found")
        except NoSuchElementException:
            time.sleep(time_sleep)
            print(f"{label}: not found!")
    
    #This function click, write and push enter
    def func_click_write_enter(self, credential,time_sleep, name, path_a):
        try:
            time.sleep(time_sleep)
            label = str(f'{name}')
            name = self.driver.find_element_by_xpath(path_a)
            name.click()
            name.clear()
            name.send_keys(credential)
            time.sleep(time_sleep)
            name.send_keys(Keys.RETURN)
            print(f"{label}: found")
        except NoSuchElementException:
            time.sleep(time_sleep)
            print(f"{label}: not found!")
        
    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""
        # make driver go to the Linkedin login url
        self.driver.get('https://www.linkedin.com/checkpoint/rm/sign-in-another-account')
        self.func_click_write(self.email,4, 'login_email','/html/body/div/main/div[3]/div[1]/form/div[1]/input')
        self.func_click_write(self.password,4,'login_password','/html/body/div/main/div[3]/div[1]/form/div[2]/input')
        self.func_click(2, 'login', '/html/body/div/main/div[3]/div[1]/form/div[3]/button')
       
    def job_search(self):
        """This function goes to the 'Jobs" section and looks for all the jobs that matches the keyword and location"""
        self.func_click(2, 'jobs_page', '/html/body/div[6]/header/div/nav/ul/li[3]/a') # Click on jobs page
        self.func_click_write_enter(self.keywords,4, 'search_keywords',"//input[starts-with(@id,'jobs-search-box-keyword-id')]") # Write type of searched job
        self.func_click_write_enter(self.location,4, 'search_location',"/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]") # Write location
        
    def filter(self):
        """This fucntion filters all the job results by 'Easy Apply'"""
        self.func_click(2,'all_filters_button',"//button[starts-with(@aria-label,'Show all filters. Clicking this')]") # Click on all_filters_button
        self.func_click(2,'most_recent_button',"/html/body/div[3]/div/div/div[2]/ul/li[2]/fieldset/div/ul/li[1]/label/p/span[1]") # Click on most_recent_button
        self.func_click(2,'last_week_button',"/html/body/div[3]/div/div/div[2]/ul/li[3]/fieldset/div/ul/li[2]/label/p/span[1]") # Click on last_week_button
        self.func_click(2,'easy_apply_button',"//div[starts-with(@data-control-name,'filter_detail_select')]") # Click on easy_apply_button
        self.func_click(2,'remote_button_select',"/html/body/div[3]/div/div/div[2]/ul/li[7]/fieldset/div/ul/li[2]/label/p/span[1]") # Click on remote_button_select
        self.func_click(2,'hybrid_button_select',"/html/body/div[3]/div/div/div[2]/ul/li[7]/fieldset/div/ul/li[3]/label/p/span[1]") # Click on hybrid_button_select
        self.func_click(2,'apply_filters_button',"//button[starts-with(@aria-label,'Apply current filters to')]") # Click on apply_filters_button

    def count_vacancies_pages(self):
        """This function find the number of vancancies and pages"""
        #Number of vacancies
        container = self.driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[1]/div") #quando aggiorni, selezioni il box sulla bassa di scorrimento verticale
        total_results = self.driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[1]/header/div[1]/small/div")
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print('total_results_int',total_results_int)
        time.sleep(2)
        
        # Condizione per contare il numero di pagine
        if total_results_int > 25:        
            self.driver.execute_script('arguments[0].scrollTop = ((arguments[0].scrollHeight)*1.0)', container) #Scrolla la pagina fino alla fine in modo da contare il numero di pagine
            time.sleep(1)
            find_pages = self.driver.find_elements_by_class_name("artdeco-pagination__indicator.artdeco-pagination__indicator--number")
            total_pages = find_pages[len(find_pages)-1].text
            total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
        else:
            total_pages_int = 1      
        return total_pages_int
    
    def find_offers(self):
        """This function find all the offers through all the pages result and filtering"""
        time.sleep(2)
        container = self.driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[1]/div")
        
        # Scrolla il box delle pagine se in modo elnto in modo da caricare tutte e 25 le posizioni 
        for i in range(1, 11):
            value = i/10
            self.driver.execute_script('arguments[0].scrollTop = ((arguments[0].scrollHeight)*{})'.format(value), container)
            print(f"Percentuale caricamento listings: {value * 100}%")
            time.sleep(2)
      
        #Applying
        all_listings = self.driver.find_elements_by_css_selector(".job-card-container--clickable")
        i = 0
        for listing in all_listings:
            print("called")
            listing.click()
            
            time.sleep(3)
            # click on easy button apply            
            try:
                self.func_click(2,'in_apply',"/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/div/div/div/button/span")
            except NoSuchElementException:
                print('You already applied to this job, go to next...')
                pass
            time.sleep(1)
            
            # try to submit if submit application is available...
            try:
                self.func_click(2,'no_follow_button',"/html/body/div[3]/div/div/div[2]/div/div/form/footer/div[1]/label")
                self.func_click(2,'submit',"/html/body/div[3]/div/div/div[2]/div/div/form/footer/div[3]/button/span")
                self.func_click(2,'next_button',"/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button/span")
                self.func_click(2,'review_button',"/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]/span")
                self.func_click(2,'no_follow_button',"/html/body/div[3]/div/div/div[2]/div/div/form/footer/div[1]/label")
                self.func_click(2,'submit',"/html/body/div[3]/div/div/div[2]/div/div/form/footer/div[3]/button/span")
            except NoSuchElementException:
                pass
            
            try:
                self.func_click(3,'close_confirmation_page',"/html/body/div[3]/div/div/button")
                self.func_click(3,'discard_confirm',"/html/body/div[3]/div[2]/div/div[3]/button[1]/span")
            except NoSuchElementException:
                pass

            i = i + 1
            time.sleep(3)
            print(f"Visionate: {i}")
        
    def apply(self):
        """Apply to job offers"""
        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(2)
        self.job_search()
        time.sleep(2)
        self.filter()
        time.sleep(2)
        self.count_vacancies_pages()
        time.sleep(2)
        print(self.count_vacancies_pages())
        total_pages = self.count_vacancies_pages()
        print ("pagine totali: ",total_pages)
        
        for page in range(2,total_pages+1):
            time.sleep(2)
            print("Pagina caricata n.: ",page-1)
            self.find_offers()
            time.sleep(2)
            get_page = self.driver.find_element_by_xpath("//button[@aria-label='Page "+str(page)+"']")
            get_page.click()
            time.sleep(2)

if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()