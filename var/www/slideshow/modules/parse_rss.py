import os
import feedparser
feedparser._HTMLSanitizer.acceptable_elements.update(['iframe'])
#feedparser._HTMLSanitizer.acceptable_elements.update(['html'])
#feedparser._HTMLSanitizer.acceptable_elements.update(['head'])
#feedparser._HTMLSanitizer.acceptable_elements.update(['title'])
import urllib.request
import webbrowser
import tempfile
import subprocess
from modules.AUTOSLIDESHOW import AUTOSLIDESHOW

from bs4 import BeautifulSoup

class RSS:

	file_list=[]
	news_dict={}
	debug = True
	server=subprocess.check_output('n4d-client -m get_variable -c VariablesManager -a SRV_IP', shell=True, encoding='UTF-8').strip()
	#server="10.3.0.254"
	#server="192.178.1.77"

	def dprint (self,msg=''):
		try:
			debug = True
			if debug:
				print ("%s"%msg)

		except Exception as e:
			print("[RSS](dprint) Error: %s"%e)
	#def dprint



	#Test if path is a file or directoy and execute rss_file_true for every files
	def list_rss_file (self,directory=None):
		try:
			self.file_list=[]
			news_extract={}
			url = "http://"+self.server+"/news/rss/"
			rss_decoded=tempfile.NamedTemporaryFile().name

			try:
				urllib.request.urlretrieve(url,rss_decoded)
				del self.file_list[:]
				self.news_dict.clear()
				with open(rss_decoded,'rt',encoding='utf-8') as f:
					if 'rss' in f.read():
						self.file_list.append(rss_decoded)

			except Exception as e:
				print("[RSS](list_rss_file)Can't get RSS from URL: %s"%e)

			self.dprint("[RSS](rss_file_true) List RSS files: %s"%self.file_list)
			self.parse_rss_list(self.file_list)

		except Exception as e:
			print("[RSS](list_rss_file)Error: %s"%e)

	#def list_rss_file


	# Generate a list with rss files
	def rss_file_true (self,file):
		try:
			if file.endswith('.rss'):
				self.dprint ("RSS file: %s"%file)
				self.file_list.append(file)
				
		except Exception as e:
			print("[RSS](rss_file_true) Error: %s"%e)

	#def list_rss_file



	# merge all rss news file in only one dict
	def merge_news_dict (self,news_extracted):
		try:
			index=len(self.news_dict)
			if len(news_extracted) > 0:
				for item in news_extracted:
					self.news_dict[index]=news_extracted[item]
					index=index+1

		except Exception as e:
			print("[RSS](merge_news_dict) Error: %s"%e)

	#def merge_news_dict



	def parse_rss_list(self,file_list_to_parse):
		try:
			#print (file_list_to_parse)
			if len(file_list_to_parse) == 0:
				self.dprint ("Can't find rss file, please check it.")
			else:
				for file in file_list_to_parse:
					self.dprint('')
					self.dprint('')
					self.dprint("[parse_rss_list] Analizing: %s"%file)
					news_extracted=self.parse_rss_file(file)
					self.merge_news_dict(news_extracted)

		except Exception as e:
			print("[RSS][parse_rss_list]Error: %s"%e)

	#def parse_rss_list

	def parse_rss_file (self,file):
		try:
			rss=feedparser.parse(file)
			feed_entries=rss.entries
			self.dprint('')
			self.dprint("########################################")
			self.dprint('Detail from RSS')
			self.dprint("Title: %s"%rss.feed.title)
			self.dprint("Link: %s"%rss.feed.link)
			self.dprint("News Item Number: %s"%len(feed_entries))
			self.dprint("########################################")



			entry_element=0
			element={}
			for entry in feed_entries:
				self.dprint()
				self.dprint('')
				self.dprint('NEWS ITEM %s:'%(entry_element+1))
				self.dprint(entry)
				self.dprint("------------------------------")
				article_title = entry.title
				if 'subtitle' in entry:
					article_subtitle=entry.subtitle
				else:
					article_subtitle="None"
				article_link = entry.link
				article_id=entry.id
				article_author=entry.author
				article_description = entry.description
				article_published_at = entry.published # Unicode string
				article_updated=entry.updated
				article_published_at_parsed = entry.published_parsed # Time object
				if 'content' in entry:
					content = entry.summary
					try: 
						content_type = entry.content.type
					except Exception as e:
						content_type = "Null"
					try:
						content_base = entry.content.base
					except Exception as e:
						content_base = "Null"
					try:
						content_value = entry.content.value
					except Exception as e:
						content_value = "Null"
				else:
					content="None"

				self.dprint ("Title: {} - Link:[{}]".format(article_title, article_link))
				self.dprint("Subtitle: {}".format(article_subtitle))
				self.dprint("Id: {}".format(article_id))
				self.dprint("Author: {}".format(article_author))
				self.dprint ("Published at: {}".format(article_published_at))
				self.dprint ("Updated: {}".format(article_updated))
				self.dprint("Content: {}".format(content))
				self.dprint("Content Type: {}".format(content_type))
				self.dprint("Content Base: {}".format(content_base))
				self.dprint("Content Value: %s"%(content_value))
				self.dprint("Content XML: %s"%(content))
				self.dprint("Description: %s"%article_description)

				# Generate dictionary with content of news
				# parser content variable, because is a string
				self.dprint("------------------------------")
				self.dprint ('RESUME FROM THIS NEWS ITEM:')
				element[entry_element]={}
				soup=BeautifulSoup(content, "html.parser")
				element[entry_element]['title']=article_title
				element[entry_element]['type']="None"

				html=False
				for item in soup:
					if 'kg-card-begin: html' in item or 'kg-card-begin: markdown' in item:
						html=True
						break
				if html:
					element[entry_element]['text']=''
					for item in soup:
						if 'kg-card-begin: html' not in item and 'kg-card-end: html' not in item and 'kg-card-begin: markdown' not in item and 'kg-card-end: markdown' not in item:
							try:
								element[entry_element]['text']=element[entry_element]['text']+'%s'%(item)
							except Exception as e:
								print("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
					element[entry_element]['type']='html'
					self.dprint ("Notice HTML: {}".format(element[entry_element]['text']))	
				else:
					#Twitter is a text in rss news
					for item in soup.find_all("p"):
						try:
							if soup.find_all("p") :
								element[entry_element]['text']='%s'%(item.text.strip())
								element[entry_element]['type']='text'
								self.dprint ("Notice Text: {}".format(item.text.strip()))
							else:
								element[entry_element]['text']='Not detected'
								self.dprint ("Notice Text: Not detected")
						except Exception as e:
							print("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
				
				# two checks are necessary to confirm or not type
				if soup.find_all("video"):
					if soup.find_all("video"):
						for item in soup.find_all("video"):
							try:
								element[entry_element]['video']=item['src']
								element[entry_element]['type']='video'
								self.dprint ("Notice Video: {}".format(item['src']))
							except Exception as e:
								self.dprint("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
					else:
						element[entry_element]['video']='Not detected'
						self.dprint ("Notice Video: Not detected")

				# two checks are necessary to confirm or not type
				# support to YouTube and Vimeo
				if soup.find_all("iframe"):
					if soup.find_all("iframe"):
						for item in soup.find_all("iframe"):
							try:
								if 'youtube' in item['src']:
									element[entry_element]['type']='youtube'
									element[entry_element]['src']=item['src']
									if 'embed/' in item['src']:
										element[entry_element]['id']=item['src'].split("embed/")[1].split("?")[0]
									else:
										element[entry_element]['id']=None
									element[entry_element]['width']=item['width']
									element[entry_element]['height']=item['height']
								else:
									element[entry_element]['iframe']=item
									element[entry_element]['type']='iframe'
								
								self.dprint ("Element Entry YouTube/iframe: {}".format(element[entry_element]))
								self.dprint ("Notice Iframe: {}".format(item))

							except Exception as e:
								self.dprint("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
					else:
						element[entry_element]['iframe']='Not detected'
						self.dprint ("Notice Iframe: Not detected")

				if soup.find_all("figure"):
					if soup.find_all("img"):
						# List of images add support to images gallery
						element[entry_element]['image']=[]
						element[entry_element]['type']='image'
						for item in soup.find_all("img"):
							try:
								element[entry_element]['image'].append(item['src'])
							except Exception as e:
								self.dprint("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
						self.dprint ("Notice Image: %s"%(element[entry_element]))
					else:
						element[entry_element]['image']='Not detected'
						if element[entry_element]['type'] == 'iframe':
							pass
						elif element[entry_element]['type'] == 'text':
							pass
						else:
							self.dprint ("Notice Image: Not detected")

				entry_element=entry_element+1
			#self.dprint('')
			#self.dprint('')
			#self.dprint('RSS RESUME ELEMENT: %s'%element)
			self.dprint('')
			self.dprint('')

			return element
			
		except Exception as e:
			print("[RSS](parse_rss_file)Error: %s"%e)

	#def parse_rss_file


	def parse_rss_other(self,rss_url):
		try:
			#Read feed xml data
			news_feed = feedparser.parse(rss_url) 

			#Flatten data
			df_news_feed=json_normalize(news_feed.entries)

			#Read articles links
			print(df_news_feed.link.head())

		except Exception as e:
			print("[RSS](parse_rss_other)Error: %s"%e)

	#def parse_rss_other





	def start (self):
		try:
			#directory_rss_ghost="/home/daduve/Desarrollo/kiosco_news"
			self.list_rss_file()
			print ("RESUME FROM ALL NEWS ITEMS IN RSS MERGED TO MAKE SLIDESHOW")
			print ("%s"%self.news_dict)
			autoslideshow=AUTOSLIDESHOW()
			slideshow_created=autoslideshow.add_elements(self.news_dict)
			
			return(slideshow_created)
			
		except Exception as e:
			print("[RSS](__init__)Error: %s"%e)

	#def start

RSS()
