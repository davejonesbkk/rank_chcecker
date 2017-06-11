#To do

#Take keywords from local txt file
#Get target URLs from local txt file
#Search Google US for rankings from user keywords - need to include waits
#Save Google ranking position for keywords and URLs

#Get keywords and URLs from sheet on Google Drive
#Upload search results to sheet on Google Drive
#Email results and sheet to Mark

#Optimise for speed - use Yield?

import argparse, requests, csv, urllib, time
from bs4 import BeautifulSoup

#def get_serps():

def get_data(keywords_file, urls_file):

	

	with open(keywords_file, 'r') as kf:
		keywords = kf.readlines()

	keywords = [x.strip() for x in keywords]

	with open(urls_file, 'r') as uf:
		urls = uf.readlines()

	urls = [x.strip() for x in urls]

	print keywords
	print urls 

	get_serps(keywords, urls)

def get_serps(keywords, urls):

	print 'Getting SERP results now...'

	counter = 0

	search_engine = 'https://www.google.com/search?hl=en&q='

	results = []

	parsed_results = []

	final_urls = []

	while counter != 3:


		resp = requests.get(search_engine+keywords[0]+'&start='+str(counter)+'0')
		bsoup = BeautifulSoup(resp.text, 'lxml')

		for link in bsoup.find_all('a'):
			results.append(link.get('href'))


		for i in results:
			if i[0:6] == '/url?q':
				parsed_results.append(i)


		for p_url in parsed_results:
			if 'webcache' in p_url:
				parsed_results.remove(p_url)


		for i in parsed_results:
			head, sep, tail = i.partition('&sa=')
			final_urls.append(head.lstrip('/url?q='))

		print final_urls

		counter += 1

		print 'Going to next page of SERPs'
		time.sleep(3)

	#print final_urls


	to_file(final_urls)

def to_file(final_urls):

	print 'Saving to file'

	serps = open('serps.csv', 'wb')
	writer = csv.writer(serps, delimiter=',')
	for val in final_urls:
		writer.writerow([val])
	serps.close()




def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('keywords_file', help='Enter the file name of your keywords')
	parser.add_argument('urls_file', help='Enter the file name of your target URLs')
	args = parser.parse_args()

	keywords_file = args.keywords_file
	urls_file = args.urls_file

	get_data(keywords_file, urls_file)




if __name__ == '__main__':
	main()



