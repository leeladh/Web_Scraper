import bs4 as bs
import schedule as sc
import urllib.request
from collections import defaultdict
import pandas as pd

def scrap(url):
	sauce = urllib.request.urlopen(url).read() # Opening the book store url
	soup = bs.BeautifulSoup(sauce, 'lxml') # Get the HTML code of url
	data = defaultdict(list) # To store scrapped data

	for ar in soup.find_all('article', class_='product_pod'):
		for im in ar.find_all('img'): # Get book cover image link
			data['Image Link'].append(url + im.get('src'))

		for pr in ar.find_all('p'):
			if 'star-rating' in pr['class']: # Get rating of the books
				data['Rating'].append(pr['class'][1])
			elif 'price_color' in pr['class']: # Get the price of the book
				data['Price'].append(pr.text)

		for ti in ar.find_all('h3'): # Get book title of book
			data['Book Title'].append(ti.text)

	# Saving the data in csv file.
	df = pd.DataFrame(data)
	df.to_csv('data.csv')


sc.every(4).hour.do(scrap('http://books.toscrape.com/'))
