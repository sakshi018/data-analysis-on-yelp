import re
import urllib
import urllib2
import string
import mechanize
import httplib2
from urlparse import urlparse
from bs4 import BeautifulSoup
from collections import OrderedDict


for i in range(1,2001):
	page = "business"+(str)(i)+".html"
	soup = BeautifulSoup(open(page))
	business = ""
	business = business + (str)(i) + ":" + "\n"
	linklist = []
	emails_ids = []
	try:
		name  = soup.find(id="bizInfoHeader").h1.text.encode('utf-8').strip()
		business = business + 'Business Name->' + name + '\n'
	except:
		business = business + 'Business Name->' + "N/A" + '\n'
		pass
	try:
		if soup.find(id="bizPhone") :
			phone = soup.find(id="bizPhone").text.encode('utf-8').strip()
			business = business + 'Business Phone->' + str(phone)+'\n'
		else:
			business = business + 'Business Phone->' + "N/A\n"
	except:
		business = business + 'Business Phone->' + "N/A\n"
		pass

	try:
		if soup.find(id="bizUrl") :
			url = soup.find(id="bizUrl").text.encode('utf-8').strip()
			url = 'http://' + url
			business = business + 'Business URL->' + str(url)
			mb = mechanize.Browser()
			mb.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
			mb.set_handle_robots(False)
			response = mb.open(url).read()
			soup2 = BeautifulSoup(response)
			links = soup2.findAll('a')	#ALL THE LINKS ARE STORED AS A LIST

			for link in links:
				if re.search('Contact*',str(link), re.IGNORECASE):
					try:
						strng = str(link['href']).strip()
						if strng[0] == '#':
							linklist.append( url+"/"+strng )
						elif re.search('http', strng, re.IGNORECASE):
							linklist.append(strng)
						elif strng[0] == '/':
							linklist.append(url+strng)
						elif strng[0].isalpha():
							linklist.append(url+'/'+strng)
					except Exception,e:
						pass

			linklist =  list(OrderedDict.fromkeys(linklist))
			for link in linklist:
					mb = mechanize.Browser()
					mb.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
					mb.set_handle_robots(False)
					try:
						response = mb.open(str(link)).read()
					except Exception,e:
						pass
					soup3 = BeautifulSoup(response)
					aTags = soup3.findAll('a')
					for aTag in aTags:
						try:
							if re.search('[^@]+@[^@]+\.[^@]+',str(aTag), re.IGNORECASE):
								emails_ids.append(aTag['href'])
						except Exception,e:
							pass
			emails_ids =  list(OrderedDict.fromkeys(emails_ids))

		else:
			business = business + 'Business URL->' + 'N/A'

	except Exception,e:
		pass

	print business
	print 'Contact URLs->' , linklist
	print 'E-Mail->' , emails_ids