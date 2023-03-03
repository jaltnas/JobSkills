# JobScraper.py
Job Scraper for Data Science, Data Analysis and Data Engineering in Sweden

This code scrapes the Indeed job site for job postings related to data science, data analysis and data engineering in Sweden.
Prerequisites

This code was written in Python 3. You will need to install the following packages:

    Selenium
    pandas

You will also need to install the appropriate driver for your browser. In this code, we are using Firefox, so you will need to download the Firefox driver from the following link:

https://github.com/mozilla/geckodriver/releases

Make sure you add the driver to your system PATH.
## How to use

To use this code, you will need to call the get_jobs function and pass in two arguments:

    new_jobs: a list of job titles to search for. In this code, we are searching for the following job titles: "data scientist", "data analytics", "data engineer", "machine learning engineer", "data analyst", and "data science".
    work_loc: the location where you want to search for jobs. In this code, we are not specifying a location, so the search will be done for all locations in Sweden.

The function will return a Pandas DataFrame containing the following information for each job posting:

    Title
    Company
    Location
    Ratings
    URL:s
    Description
    Type (the job title searched)

## How it works

The code uses the Selenium package to automate a Firefox browser to search for job postings on Indeed. For each job posting found, the code extracts the title, company, location, ratings (if available), URL, and job description. The code then returns a Pandas DataFrame containing all the collected information.

Note that the code waits for two seconds after loading each page to allow all elements to load, and it will only scrape up to 100 pages for each job search. This can be changed in the for i in range(0,100): line.













# JobSkills
Exploring job postings related to data science and data analytics - which skills are requested on the swedish market

Topics related to keywords "education" and/or "degree".
![image](https://user-images.githubusercontent.com/119524062/218262704-e4273d6d-725f-4d8e-a48c-5da13c8f362e.png)
![image](https://user-images.githubusercontent.com/119524062/218262720-21e47bad-bb46-463d-8223-c9e666c3d3e4.png)

Topics related to keywords "skills" and "tools", with obvious separation of topics concerning data engineering, data analytics and data science.

Data engineering:
![image](https://user-images.githubusercontent.com/119524062/218262863-c1bcbfa5-8f07-4ede-b7fc-765e6f377bac.png)
![image](https://user-images.githubusercontent.com/119524062/218262888-e4a19962-8c24-48c2-a2c6-67e17766fa48.png)


Data analytics:
![image](https://user-images.githubusercontent.com/119524062/218262869-61f04d06-0e18-4df3-854e-84f3ef83d1ec.png)

Data science: 
![image](https://user-images.githubusercontent.com/119524062/218262896-ee3f8e6f-a6c6-4c23-8064-bb3c38ab2c46.png)
![image](https://user-images.githubusercontent.com/119524062/218262918-48c83183-a145-4440-a479-276de1cf33a2.png)

DevOps:
![image](https://user-images.githubusercontent.com/119524062/218262926-4e7ebc3b-eed5-4221-bfaf-3aede2f5bf4f.png)

