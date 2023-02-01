# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import pandas as pd
import numpy

#%%

def get_jobs(new_jobs: list, work_loc):
    #specify driver path
    #DRIVER_PATH = '/home/johannes/Firefox/firefox'
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options= firefox_options)
    
    
    titles=[]
    companies=[]
    locations=[]
    ratings = []
    urls = []
    job_type = []
    
    
    for n in range(len(new_jobs)):
        start = len(titles)
        driver.get('https://indeed.com')
        driver.implicitly_wait(2)
        
        try:
            close_popup = driver.find_element("xpath","//*[@class='icl-CloseButton icl-Card-close']")
            close_popup.click() 
        except:
            None        
        
        search_title = driver.find_element("xpath", "//*[@id='text-input-what']")
        search_title.send_keys(new_jobs[n])
        
        if n == 0:
            search_location = driver.find_element("xpath", "//*[@id='text-input-where']")
            search_location.send_keys(work_loc)
    
        initial_search_button = driver.find_element("xpath", "//form[@id='jobsearch']/button")
        initial_search_button.click()
    
        driver.implicitly_wait(2) 
        
    
        for i in range(0,100):
            print(i)
            
            job_cards = driver.find_elements("xpath", "//*[contains(@class,'resultContent')]")
            
            for job in job_cards:
                job_type.append(new_jobs[n])
        
                #title = job.find_element("xpath",".//h2[@class='jobTitle jobTitle-newJob css-bdjp2m eu4oa1w0']").text
                title = job.find_element("xpath",".//h2[contains(@class,'jobTitle')]").text
                titles.append(title)
            
                loc = job.find_element("xpath",".//*[contains(@class,'companyLocation')]").text
                location = ''.join([i for i in loc if not i.isdigit()])
                location = location.strip()
                locations.append(location)
                
                company = job.find_element("xpath",".//*[contains(@class,'companyName')]").text
                companies.append(company)
                
                try:
                    rating = job.find_element("xpath",".//*[contains(@class,'ratingsDisplay')]").text
                    ratings.append(rating)
                except:
                    rating = "unknown"
                    ratings.append(rating)
                
                url = job.find_element("xpath",".//h2[contains(@class,'jobTitle')]/a[@href]")
                url = url.get_attribute("href")
                urls.append(url)
                
             
                
            try:
                next_button = driver.find_element("xpath","//*[contains(@aria-label,'Next Page')]")
                new_url = next_button.get_attribute("href")
                driver.get(new_url)
                driver.implicitly_wait(2)
                try:
                    close_popup = driver.find_element("xpath","//*[@class='icl-Modal']")
                    close_popup.click() 
                except:
                    None
            except:
                break
        end = len(titles)
        print(f"Added {start-end} jobs for {new_jobs[n]}")
    
    descriptions=[]
    for link in urls:
        driver.get(link)
        jd = None
        while jd is None:
            try:
                jd = driver.find_element("xpath",".//*[contains(@class,'jobsearch-jobDescriptionText')]").text
            except:
                print("exception")
                driver.quit()
                driver = webdriver.Firefox(options= firefox_options)
                driver.get(link)
                pass
        descriptions.append(jd)
        
    result = {'Title': titles, 'Company':companies, 'Location':locations, 'Ratings':ratings,'URL:s':urls, 'Description':descriptions, "Type":job_type}
    df = pd.DataFrame(result)
    
    return df
#%%
new_jobs = ['data science', 'data analytiker', '"data engineer"']


job_data = []
job_data.append(get_jobs(new_jobs, "Göteborg"))
print("Göteborg Completed")
job_data.append(get_jobs(new_jobs, "Stockholm"))
print("Stockholm completed")
job_data.append(get_jobs(new_jobs, "Malmö"))
print("Malmö completed")

#%%
final_data = pd.concat([job_data[0], job_data[1], job_data[2]], ignore_index = True, axis=0)

#%%
new_jobs = ['"data scientist"', '"data analytics"', '"data engineer"','"machine learning engineer"','"data analyst"', '"data science"']
job_data = get_jobs(new_jobs,"")

#%%




