from selenium import webdriver
import time
import pandas as pd
import os
from pathlib import Path


# gets the raw data
def get_the_df(url):

    # setting up some paths
    chrome_driver = '/Users/jeremybixby/Desktop/drivers/chromedriver'
    downloads = '/Users/jeremybixby/Downloads/'

    # initiating the driver with the url for the page
    driver = webdriver.Chrome(chrome_driver)
    driver.get(url)

    # executing the get raw data button
    driver.maximize_window()
    button = driver.find_element_by_id('table-raw-data')

    # click the button and wait 5 seconds to download
    button.click()
    time.sleep(5)

    # gets the files in the downloads directory and gives you the newest first
    paths = sorted(Path(downloads).iterdir(), key=os.path.getmtime, reverse=True)

    # gets the most recently created file in the downloads folder
    the_path = paths[0]

    # opens and collects the pertinent data
    the_list = open_and_process_data(the_path)
    df_list = split_the_list(the_list)

    # defines the df off the list of lists
    df = pd.DataFrame(df_list)

    print(df)
    return df

def split_the_list(the_list):
    return_list = []
    for s in the_list:
        comps = s.split(',')
        return_list.append(comps)

    return return_list

# opens the file and reads the data into a list
def open_and_process_data(path):
    # the inputFile
    inputFile = open(path, 'r')
    list_of_data = []

    # only those lines we're interested in
    counter = 1
    linestart = 4
    lineend = 55

    # pull out the lines we're interested in
    for line in inputFile.readlines():
        if counter >= linestart and counter <= lineend:
            s1 = line.rstrip('\n')
            s2 = s1.strip('')
            list_of_data.append(s2)
        counter = counter + 1

    # closes the file
    inputFile.close()

    return list_of_data


# gets the df for further processing
df = get_the_df('https://www.kff.org/health-reform/state-indicator/state-activity-around-expanding-medicaid-under-the-affordable-care-act/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D')



