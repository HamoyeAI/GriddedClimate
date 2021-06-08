from __future__ import print_function
try:
    from time import sleep
    import pandas as pd
    import numpy as np
    import glob
    import os                     # OS module in Python provides functions for interacting with the operating system
    import requests               # requests module allows you to send HTTP requests 
    from requests import urllib3  # HTTP client for Python, thread safety, connection pooling, client-side SSL/TLS verification, HTTP redirects
    from bs4 import BeautifulSoup # import the beautifulsoup library
    import os  # OS module in Python provides functions for interacting with the operating system
    import shutil   # This module helps in automating process of copying and removal of files and directories.
    import wget
    import subprocess
    from google.cloud import storage
    import google.cloud.storage
    # from oauth2client.service_account import ServiceAccountCredentials
    import datetime
    import re
    import io
    import json
    import sys
except Exception as e:
    print('Error : {} '.format(e))

"""
Put most code into a function or class.
Use __name__ to control execution of your code.
Create a function called main() to contain the code you want to run.
Call other functions from main().
"""

def GetRasterYears(url=None):
    # send a request to get the url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    year_list = []
    # loop through the links for all <a> anchor tags
    for link in soup.find_all('a'):
        # Check for the href attributes as well
        year_ = link.get('href')
        # Append the years to the list
        year_list.append(year_)

    # Create another new list to hold the number of years 
    each_year_list = []
    # Loop through the previous list excluding the first five elements which are not needed
    for new_year in year_list[5:]:
        # Remove the forward slash right in front of the different years
        new_year_ = new_year.replace('/', '')
        # And append the selected years to the new list
        each_year_list.append(new_year_)
        print("Completed getting the raster data number years")
    return each_year_list


def makenewdir(each_year_list):
    new_path = os.path.join(os.getcwd(), r'scrapped_data')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    for year in each_year_list:
        try:
            os.makedirs(os.path.join(new_path, year))
        except FileExistsError:
            pass
    return new_path


def fecthrasterurl(url):
    years_url = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for item_years in soup.find_all('td', class_="indexcolname"):
        item_year = item_years.find('a')
        item_link = item_year.get('href') if item_year else None
        data_url =  url + item_link
        print('Fetching:', data_url)
        years_url.append(data_url)
        years_new_list = years_url[1:]
    return years_new_list


def downloadwithwget(each_year_list, years_new_list, new_path):
    n = 0
    year_array = [y for y in each_year_list]
    link_path = [x for x in years_new_list]
    
    for n in range(len(each_year_list)):
        for i in range(len(link_path)):
            if link_path[i][-5:-1] == year_array[n]:
                new_url = link_path[i]
                years_containers = []
                new_url_lists = []
                
                r = requests.get(new_url)
                soup = BeautifulSoup(r.text, 'html.parser')

                for link in soup.find_all('td', class_="indexcolname"):
                    item_year = link.find('a')
                    item_lin = item_year.get('href') if item_year else None
                    years_containers.append(item_lin)
        
                for new_item_lk in years_containers:
                    new_data_url = new_url + new_item_lk
                    new_url_lists.append(new_data_url)
                    
                # sleep(5)
                for sillians in new_url_lists:
                    dest_file = new_path+"/{}".format(year_array[n])
                    # dest_file = "C://Users/Sillians/Desktop/Climate Change/scraped_raster_data/{}".format(year_array[n])
                    filename = dest_file + '/' + os.path.basename(sillians)
                    if not os.path.exists(filename):
                        wget.download(sillians, out=filename)
                
                n += 1
                i += 1
            else:
                break


african_dialy_url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p25/"
global_daily_url  = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p25/"


def main():
    """
    This is the docstring for the main() method in the scrapper-function.py module
    """
    # the url for african daily and global daily
    african_dialy_url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p25/"
    global_daily_url  = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p25/"


    each_year_list = GetRasterYears(url=african_dialy_url)
    new_path = makenewdir(each_year_list)
    years_new_list = fecthrasterurl(url=african_dialy_url)
    downloadwithwget(each_year_list, years_new_list, new_path)


if __name__ == '__main__':
    main()
