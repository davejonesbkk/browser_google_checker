

#Get keywords and target urls from local txt file 
#Use Selenium to open Google US in browser
#Scrape Google search results for target keyword(s)
#Download all search results from Google pages 1-4 to a txt file

import argparse, time, csv, requests, re, os
from os import listdir
from os.path import isfile, join
from urlparse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import pandas as pd


def init_browser(locale='en-us'):
	#initialize the Webdriver browser
	browser = webdriver.FirefoxProfile()
	browser.set_preference("general.useragent.override", "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0")
	browser.update_preferences()
	browser = webdriver.Firefox()
	browser.wait = WebDriverWait(browser, 5)
	return browser 



def open_search(browser, files_data):

	keywords = files_data[0]
	urls = files_data[1]

	#open Google with Selenium in Firefox
	browser.get('https://www.google.com/ncr')

	#Creat dictionary for storing all the keywords and their search results
	search_results = {}

	#Iterate over the keywords list and set each one up as the key in the dict
	#with empty list for the values
	for kw in keywords:
		search_results[kw] = []

	#iterate over the list of keywords
	for k in keywords:

		#create 3 empty lists for handling and cleaning the search results later
		initial_urls = []

		parsed_urls = []

		completed_links = []

		page_count = 0

		try:
			#wait for Google search box to appear and send the first keyword
			elem = browser.wait.until(EC.presence_of_element_located(
					(By.NAME, 'q')))
			print 'success'
			elem.send_keys(k)
			elem.send_keys(Keys.RETURN)
			time.sleep(5)

			#while loop for couting the Google search result pages
			while page_count != 10:


				html = browser.page_source

				soup = BeautifulSoup(html, "html.parser")

				#Look for search result urls with the 'cite' tag and add to the first list
				for s in soup.find_all('cite'):
					initial_urls.append(s)

				#change each saved url into a str and pass to the next list
				for i in initial_urls:
					parsed_urls.append(str(i))

				parsed_urls = [x for x in parsed_urls if not x.startswith('<cite class="_WGk')]


				#use regex to strip out unwanted characters from url results
				for  p in parsed_urls:

					p = re.search('(?<=\>)(.*?)(?=\<)', p)
					completed_links.append(p.group(0))


				#reset the first two lists so they can be re-used on the next page of results in the while loop
				initial_urls = []

				parsed_urls = []

				#Add a sleep to make sure everything is loaded before send click for the next page
				time.sleep(20)
				browser.find_element_by_link_text('Next').click()
				soup.clear()
				page_count += 1	
				time.sleep(5)

		

			#Iterate over the completed_links list adding the urls for each keyword to its value in
			#the above dictionary
			for cl in completed_links:
				search_results[k].append(cl)

		

			#Clear the Selenium 'elem' browser element so that the next keyword in the list can be inputted
			elem.clear()
			

		except TimeoutException:
			print('Box or button not found')

	print search_results

	print '#'
	print '#'
	print '.......'

	print 'Checking data...'

	sort_results(keywords, urls, search_results)
		

def sort_results(keywords, urls, search_results):


	"""
	for u in urls:
		print [i for i, y in enumerate(search_results.values()[0]) if y == u]

	for u in urls:
		print [i for i, y in enumerate(search_results.values()[1]) if y == u]

	for u in urls:
		print [i for i, y in enumerate(search_results.values()[2]) if y == u] 
	"""
	


	to_file(search_results)


def to_file(search_results):

	df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in search_results.iteritems()]))
	df.to_csv('serp_results.csv')


def get_data():

	parser = argparse.ArgumentParser()
	parser.add_argument('keywords_file', help='Enter the file name of your keywords')
	parser.add_argument('urls_file', help='Enter the file name of your target URLs')
	args = parser.parse_args()

	keywords_file = args.keywords_file
	urls_file = args.urls_file

	with open(keywords_file, 'r') as kf:
		keywords = kf.readlines()

	keywords = [x.strip() for x in keywords]

	with open(urls_file, 'r') as uf:
		urls = uf.readlines()

	urls = [y.strip() for y in urls]


	return keywords, urls


if __name__ == '__main__':
	files_data = get_data()
	browser = init_browser()
	open_search(browser, files_data)



	
