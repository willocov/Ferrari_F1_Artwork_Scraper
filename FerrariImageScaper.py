# Ferrari F1 Artwork Image Scraper
# Created by William Covington
# Last Updated: 2022-11-07
# This script is used to download Ferrari's F1 Cover Art posters for each race weekend.
# Includes all races back to the 2019 season.
# Images will be saved to the same directory as this file by default.
# A optional local or absolute filepath may be passed as a parameter
# The directory will be created if it does not exist.

# Usage: python FerrariImageScraper.py [optional local or absolute path]
# Note: Make sure to include a '\' at the end or it's parent directory will be used, might fix later.

# Samples
# Same directory as file: python FerrariImageScraper.py
# Local Path:  python FerrariImageScraper.py output\
# Absolute Path: python FerrariImageScraper.py C:\Users\pythonTests\Downloads\

import sys
import os
import requests
import urllib
from bs4 import BeautifulSoup
from pathlib import Path

# These variables are derived from HTML elements on Ferrari's website and may change.
# ===================================================================================
# URL to the Cover Art homepage that displays a card view of all posters for each race weekend. Back to 2019 season.
HOMEPAGE = "https://www.ferrari.com/en-EN/formula1/cover-arts"

# The class name of each card in the homepage's card view
# The card's href element is used to access the webpage for it's race weekend, which contains the artwork
COVER_ART_CARD_VIEW_CLASS_NAME = "BoxGrid__item__1tjOz5cT"

# The class name of the image elements that contain the artwork
# the image element's src element is used to download the images
COVER_ART_IMAGE_CLASS_NAME = "Img__image__1RV_fMUN"
# ====================================================================================

if __name__ == '__main__':
    # Check if an output filepath was passed as parameter
    if len(sys.argv) > 1:
        # Filepath was passed, create a directory for it if necessary, then verify it exists.
        localOutputDirectory = sys.argv[1]
        Path(localOutputDirectory).mkdir(parents=True, exist_ok=True)
        isDirectory = os.path.isdir(localOutputDirectory)
        if isDirectory:
            # Directory exists, good to proceed
            print("Directory is good")
        else:
            # Failed to create directory, exit
            print("Directory is bad")
            quit()
    else:
        # No output filepath was passed as parameter, use same directory as this file
        localOutputDirectory = ""

    # Get the HTML data from Ferrari's Cover Art homepage
    print("Getting HTML data from Ferrari's Cover Art homepage")
    page = requests.get(HOMEPAGE)
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the URLs for each race's web page, adds URLs to a list
    print("Scraping Ferrari's Cover Art homepage for URLs to each race's web page")
    urlList = []
    job_elements = soup.find_all("a", class_=COVER_ART_CARD_VIEW_CLASS_NAME)
    for job_element in job_elements:
        link_url = job_element["href"]
        print("Found URL: " + link_url)
        urlList.append(link_url)

    # Remove any duplicates and print results
    print("Removing Duplicate Race URLs")
    urlList = [*set(urlList)]
    print("Number of Race URLS Found: " + str(len(urlList)))

    # Loop through the list of URLs, get the images from each race's webpage
    print("Scraping each race's webpage for artwork")
    imageList = []
    for url in urlList:
        print("Scraping: " + url)
        # Get the HTML data from each race's webpage
        imagePage = requests.get(url)
        soup = BeautifulSoup(imagePage.content, "html.parser")

        # Find all the image elements and get their src values, add their URLs to a list
        job_elements = soup.find_all("img", class_=COVER_ART_IMAGE_CLASS_NAME)
        for job_element in job_elements:
            link_url = job_element["src"]
            imageList.append(link_url)
            print("Found Image: " + link_url)

    # Remove duplicates
    imageList = [*set(imageList)]

    # Remove dummy image [TODO; FIND A BETTER WAY TO DO THIS]
    imageList.remove("/formula1/static/assets/img/placeholder.jpg")

    print("Total Images Found: " + str(len(imageList)))

    # Download images, each image has same name with an incremented number [TODO: ADD OPTION TO SET FILENAME]
    print("Downloading Images")
    filenameCounter = 1  # Used to add a number to the end of each filename (e.g. ferrari_01.png)
    for image in imageList:
        urllib.request.urlretrieve(image, localOutputDirectory + f'ferrari_0{str(filenameCounter)}.png')
        print("Downloaded Image: " + image)
        filenameCounter += 1

    print("Number of Images Downloaded: " + str(filenameCounter - 1))
