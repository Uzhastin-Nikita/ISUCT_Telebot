import re
import os.path
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class ISUCT:
    URL = 'https://www.isuct.ru/'
    last_key = ""
    lastkey_file = ""

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file

        if (os.path.exists(lastkey_file)):
            self.last_key = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.last_key = self.get_lastkey()
            f.write(self.last_key)
            f.close()
    
    def new_post(self):
        r = requests.get(self.URL)
        html = BS(r.content, 'html.parser')
        
        new = []
		items = html.select('.tiles > .items > .item > a')
		for i in items:
			key = self.parse_href(i['href'])
			if(self.lastkey < key):
				new.append(i['href'])   

        return new

    def info(self, uri):
		link = self.host + uri
		r = requests.get(link)
		html = BS(r.content, 'html.parser')

		# remove some stuff
		remels = html.select('.article.article-show > *')
		for remel in remels:
			remel.extract()
        
        parse_info = {
            	"id": self.parse_href(uri),
                "title": html.select('.article-title > a')[0].text,
			    "link": link,
                "excerpt": html.select('.article.article-show')[0].text[0:200] + '...'

        };

    def get_lastkey(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		items = html.select('.tiles > .items > .item > a')
		return self.parse_href(items[0]['href'])

	def parse_href(self, href):
		result = re.match(r'\/show\/(\d+)', href)
		return result.group(1)

	def update_lastkey(self, new_key):
		self.lastkey = new_key

		with open(self.lastkey_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(new_key))
			f.truncate()

		return new_key  

        