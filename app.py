from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import sys

from utils import scrape_departments, scrape_links, multiprocess

# Installing chrome driver for selenium
def driver_install():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

# Dumping the data to json file
def generate_json(result):
    with open("output2.json", "w") as output:
        output.write(json.dumps(result, indent=4))


if __name__ == "__main__":

    try:
        print("Step[1] : Driver Initialization...")
        print("Step[1] : Please note this step may take time to download and install the driver from internet.")
        print("Step[1] : Incase this step fails, we need to download the driver locally and then manually set the driver.")
        driver = driver_install()
    except:
        print("Driver error. Please try again or manually download the driver.")
        sys.exit()
        

    # Cermati career website
    website = 'https://www.cermati.com/karir'

    # Scraping departments from career website
    try:
        print("Step[2] : Scraping all departments...")
        departments = scrape_departments(driver, website)
    except:
        print("Unknown error occurred due to changes in structure of website. Please try again.")
        sys.exit()


    # Scraping links for each department
    try:
        print("Step[3] : Scraping links for each department...")
        dept_links_mapping = scrape_links(driver, departments)
    except:
        print("Unknown error occurred due to changes in structure of website. Please try again.")
        sys.exit()

    
    # Multiprocessing all the job links
    try:
        print("Step[4] : Scraping all the job postings by multiprocessing...")
        print("Step[4] : Note : This step may take some time depending on hardware configurations")
        print("Step[4] : Please be patient")
        result = multiprocess(dept_links_mapping)
    except:
        print("Unknown error occurred due to changes in structure of website")
        print("or due to error in multiprocessing (dependency on hardware).")
        print("Please try again.")
        sys.exit()


    # Dumping the data into json file
    try:
        print("Step[5] : Generating json file...")
        generate_json(result)
    except:
        print("Unknown error occurred due to unsupported json format. Please try again.")
        sys.exit()


    print("All the job postings are successfully saved from Cermati Career website.")