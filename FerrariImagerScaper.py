import sys
import os
import requests
import urllib
from bs4 import BeautifulSoup
from pathlib import Path

HOMEPAGE = "https://www.ferrari.com/en-EN/formula1/cover-arts"
urlList = []
imageList = []

if __name__ == '__main__':

   print(sys.executable)

   if len(sys.argv) > 1:
       localOutputDirectory = sys.argv[1]
       Path(localOutputDirectory).mkdir(parents=True, exist_ok=True)
       isDirectory = os.path.isdir(localOutputDirectory)
       #print('Path points to a Directory:', isDirectory)
       if isDirectory:
           print("Directory is good")
       else:
           print("Directory is bad")
           quit()
   else:
       localOutputDirectory = ""

   page = requests.get(HOMEPAGE)
   soup = BeautifulSoup(page.content, "html.parser")

   print("Scraping Ferrari Website for F1 Race Cover Art")

   job_elements = soup.find_all("a", class_="BoxGrid__item__1tjOz5cT")

   for job_element in job_elements:
       link_url = job_element["href"]
       urlList.append(link_url)

   res = [*set(urlList)]

   print("Number of URLS Found: " + str(len(res)))

   for url in res:
       #print(url)
       imagePage = requests.get(url)
       soup = BeautifulSoup(imagePage.content, "html.parser")

       job_elements = soup.find_all("img", class_="Img__image__1RV_fMUN")
       for job_element in job_elements:
           link_url = job_element["src"]
           imageList.append(link_url)

   res =  [*set(imageList)]
   res.remove("/formula1/static/assets/img/placeholder.jpg")

   print("Total Images Found: " + str(len(res)))

   icount = 1
   for i in res:
       urllib.request.urlretrieve(i, localOutputDirectory + f'ferrari_0{str(icount)}.png')
       print("Downloaded Image: " + i)
       icount += 1

   print("Number of Images Downloaded: " + str(icount - 1))
