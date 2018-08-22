import os
import lxml
import urllib.request
from bs4 import BeautifulSoup
import json
from string import ascii_lowercase
import requests
import sys
from selenium import webdriver
import time
import cv2
import numpy as np
import threading
import math

base_image_url = 'https://medpix.nlm.nih.gov'
driver = webdriver.Firefox(executable_path=r'C:\geckodriver.exe')
driver.get('https://medpix.nlm.nih.gov/search?allen=false&allt=false&alli=true&query=MRI')
SCROLL_PAUSE_TIME = 6
scroll_end=0


# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")


while True:
	try:
	   # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	    # Wait to load page
	    time.sleep(SCROLL_PAUSE_TIME)

	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    scroll_end+=1
	    print(scroll_end)
	    if scroll_end==23:
	    	break
	    	last_height = new_height
	except Exception as e:
		print(str(e))

time.sleep(5)
# htmlSource = driver.page_source
print('Done scrolling')
elements = driver.find_elements_by_xpath("//img[@class]")

print('Done finding')

li = []
for i in  elements:
	li.append(i.get_attribute("src"))

print('Done appending')

print(len(li))


def getMri(start, end):
	print("Started worker for range :", start, "to", end)
	for i in range(start, end):
		try:
			url = li[i]
			request = urllib.request.Request(url)
			response = urllib.request.urlopen(request)
			binary_str = response.read()
			byte_array = bytearray(binary_str)
			numpy_array = np.asarray(byte_array, dtype="uint8")
			image = cv2.imdecode(numpy_array, cv2.IMREAD_UNCHANGED)
			cv2.imwrite("images/" + '{:04d}'.format(i) + '.png', image)
			print("Saved " + '{:04d}'.format(i) + '.png')
		except Exception as e:
			print(str(e))

# For multithreading
# start_time = time.time()
# thread_count = 4
# image_count = 2246
# thread_list = []

# for i in range(thread_count):
# 	start = math.floor(i * image_count / thread_count) + 1
# 	end = math.floor((i + 1) * image_count / thread_count) + 1
# 	thread_list.append(threading.Thread(target=getMri, args=(start, end)))

# for thread in thread_list:
# 	thread.start()

# for thread in thread_list:
# 	thread.join()


# end_time = time.time()
# print("Done")
# print("Time taken : " + str(end_time - start_time) + "sec")

				
start_time = time.time()
for i in range(len(li)):
    try:
        req = urllib.request.Request(li[i])
        response = urllib.request.urlopen(req)
        rr = response.read()
        ba = bytearray(rr)
        image = np.asarray(ba, dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
        cv2.imwrite("images/" + '{:04d}'.format(i) + ".png", image)
        print("Saved " + '{:04d}'.format(i) + ".png")
    except Exception as e:
        print("Error Occured for Mri " + '{:04d}'.format(i))
        print(str(e))

end_time = time.time()
print("Done")
print("Time Taken = ", end_time - start_time, "sec")
