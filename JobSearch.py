# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd

#%%

def get_jobs(new_jobs: list, work_loc):
    #Create firefox driver
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options= firefox_options)
    
    #Initialize lists for features to collect
    titles=[]
    companies=[]
    locations=[]
    ratings = []
    urls = []
    descriptions=[]
    job_type = []
    
    #Loop over all jobs in new_jobs list
    for n in range(len(new_jobs)):
        start = len(titles)
        driver.get('https://indeed.com')
        driver.implicitly_wait(2)
        
        #Close popup window if one exists
        try:
            close_popup = driver.find_element("xpath","//*[@class='icl-CloseButton icl-Card-close']")
            close_popup.click() 
        except:
            None        
        
        #Find search bar, enter job title
        search_title = driver.find_element("xpath", "//*[@id='text-input-what']")
        search_title.send_keys(new_jobs[n])
        
        #Enter specified work location
        if n == 0:
            search_location = driver.find_element("xpath", "//*[@id='text-input-where']")
            search_location.send_keys(work_loc)
        
        #Click search button
        initial_search_button = driver.find_element("xpath", "//form[@id='jobsearch']/button")
        initial_search_button.click()
    
        driver.implicitly_wait(2) 
        
    
        for i in range(0,100):
            
            #Find all job cards on current page
            job_cards = driver.find_elements("xpath", "//*[contains(@class,'resultContent')]")
            
            for job in job_cards:
                #Add type (job title searched) to current job
                job_type.append(new_jobs[n])
                
                #Find and add title of current job card
                title = job.find_element("xpath",".//h2[contains(@class,'jobTitle')]").text
                titles.append(title)
            
                #Find and add location of current job card
                loc = job.find_element("xpath",".//*[contains(@class,'companyLocation')]").text
                location = ''.join([i for i in loc if not i.isdigit()]) #Format location string
                location = location.strip() #Format location string
                locations.append(location)
                
                #Find and add company of current job card
                company = job.find_element("xpath",".//*[contains(@class,'companyName')]").text
                companies.append(company)
                
                #Check if rating exists, and if so add it to the list
                try:
                    rating = job.find_element("xpath",".//*[contains(@class,'ratingsDisplay')]").text
                    ratings.append(rating)
                except:
                    rating = "unknown"
                    ratings.append(rating)
                
                #Find and add URL of current job card
                url = job.find_element("xpath",".//h2[contains(@class,'jobTitle')]/a[@href]")
                url = url.get_attribute("href")
                urls.append(url)

            #Check if next page exists    
            try:
                next_button = driver.find_element("xpath","//*[contains(@aria-label,'Next Page')]")
                new_url = next_button.get_attribute("href") #Get URL of next page
                driver.get(new_url) #Open next page
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
    
    #Loop over URLs to open job-ads and scrape descriptions
    for link in urls:
        driver.get(link)
        jd = None
        while jd is None:
            try:
                jd = driver.find_element("xpath",".//*[contains(@class,'jobsearch-jobDescriptionText')]").text
            except: #If verify-human page, close and reopen link
                print("exception")
                driver.quit()
                driver = webdriver.Firefox(options= firefox_options)
                driver.get(link)
                pass
        descriptions.append(jd)
        
    result = {'Title': titles, 'Company':companies, 'Location':locations, 'Ratings':ratings,'URL:s':urls, 'Description':descriptions, "Type":job_type}
    df = pd.DataFrame(result) #put all lists together in one dataframe
    
    return df

#%%
new_jobs = ['"data scientist"', '"data analytics"', '"data engineer"','"machine learning engineer"','"data analyst"', '"data science"']
job_data = get_jobs(new_jobs,"")






