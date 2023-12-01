from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import multiprocessing

def scrape_departments(driver, website):
    driver.get(website)

    # Click on view all jobs button on current page
    all_jobs = driver.find_element(By.XPATH, '//button[@class = "btn btn-secondary btn-lg search-bar-btn"]')
    all_jobs.click()

    # Scrape all departments from website
    departments = driver.find_element(By.XPATH, '//select[@id = "job-department"]')
    departments = departments.text.strip()
    departments = departments.split('\n')
    n = len(departments)
    departments = {departments[i]:[] for i in range(1,n)}

    return departments



def scrape_links(driver, departments):
    dept_links_mapping = departments

    while True:
        # Get the nextpage button
        nextpage = driver.find_element(By.XPATH, '//i[@class = "fa fa-angle-right"]')
        
        # Get all the jobs on current page
        jobs = driver.find_elements(By.XPATH, '//div[contains(@class,"page-job-list-wrapper")]')
        
        for job in jobs:

            # Scrape the url of each job posting
            url = job.find_element(By.TAG_NAME, 'a')
            job_url = url.get_attribute('href')

            # Scrape department for the job posting
            dep = job.find_elements(By.TAG_NAME, 'p')
            dep = dep[1].text

            # Add the job links to specific department
            dept_links_mapping[dep].append(job_url)

        lastpage = driver.find_elements(By.XPATH, '//button[@class = "arrow-icon"]')

        # To check for last page
        if lastpage[3].is_enabled() == False:
            driver.close()
            return (dept_links_mapping)
        
        # Go to next page
        nextpage.click()


def scrape_job_postings(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape title from url
    title = soup.find('h1', {'class' : 'job-title'})
    title = title.text

    # Scrape location from url
    location = soup.find('spl-job-location')
    location = location.get('formattedaddress')

    # Scrape job description from url
    job_desc = soup.find('div', {'itemprop' : 'responsibilities'})
    job_desc = job_desc.get_text(strip=True, separator='\n').splitlines()

    # Scrape qualifications from url
    qualification = soup.find('div', {'itemprop' : 'qualifications'})
    qualification = qualification.get_text(strip=True, separator='\n').splitlines()

    # Scrape posted date from url
    date_posted = soup.find('meta', {'itemprop' : 'datePosted'})
    date_posted = date_posted.get('content').split('T')[0]

    job_record = {
                "title" : title,
                "location" : location,
                "description" : job_desc,
                "qualification" : qualification,
                "posted date" : date_posted
            }

    return job_record


def multiprocess(dept_links_mapping):
    result = {}

    for dept, links in dept_links_mapping.items():
        result[dept] = []
        with multiprocessing.Pool(10) as p:
            result[dept] = p.map(scrape_job_postings, links)
        p.terminate()
        p.join()

    return result


