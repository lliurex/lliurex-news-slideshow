import os
import feedparser
import urllib.request
import tempfile
from bs4 import BeautifulSoup

from ainur.utils import dprint

feedparser._HTMLSanitizer.acceptable_elements.update(['iframe'])

class RSS:

	def __init__(self):
		self.file_list = []
		self.news_dict = {}

	def list_rss_file(self,directory=None):
		'''Test if path is a file or directoy and execute rss_file_true for every files'''
		try:
			self.file_list=[]
			news_extract={}
			url = "http://localhost/news/rss/"
			rss_decoded = tempfile.NamedTemporaryFile().name

			try:
				urllib.request.urlretrieve(url,rss_decoded)	
				del self.file_list[:]
				self.news_dict.clear()
				with open(rss_decoded,'rt',encoding='utf-8') as f:
					if 'rss' in f.read():
						self.file_list.append(rss_decoded)
			except Exception as e:
				print("[RSS](list_rss_file)Can't get RSS from URL: %s"%e)

			dprint( "List RSS files: %s"%self.file_list, "[RSS](rss_file_true)" )
			self.parse_rss_list(self.file_list)

		except Exception as e:
			print("[RSS](list_rss_file)Error: %s"%e)

	#def list_rss_file


	# Generate a list with rss files
	def rss_file_true (self,file):
		try:
			if file.endswith('.rss'):
				dprint (file,"RSS file:" )
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
				dprint ("Can't find rss file, please check it.")
			else:
				for file in file_list_to_parse:
					dprint("\n\n[parse_rss_list] Analizing: {file_name}".format(file_name=file))
					news_extracted = self.parse_rss_file(file)
					self.merge_news_dict(news_extracted)

		except Exception as e:
			print("[RSS][parse_rss_list]Error: %s"%e)

	#def parse_rss_list

	def parse_rss_file (self,rssfile):
		try:
			rss=feedparser.parse(rssfile)
			feed_entries=rss.entries
			dprint_values = {'title':rss.feed.title, 'link':rss.feed.link, 'length': len(feed_entries) }
			dprint('''
########################################
Detail from RSS
Title: {title}
Link: {link}
News Item Number: {length}
########################################'''.format(**dprint_values))

			entry_element=0
			element={}
			for entry in feed_entries:
				dprint("\n\nNEWS ITEM {entry_number}".format(entry_number=entry_element+1))
				dprint(entry)
				dprint("------------------------------")
				article_subtitle = entry.subtitle if 'subtitle' in entry else "None"
				if 'content' in entry:
					content = entry.summary
					content_type = entry.content.type if "type" in entry.content else "Null"
					content_base = entry.content.base if "base" in entry.content else "Null"
					content_value = entry.content.value if "value" in entry.content else "Null"
				else:
					content="None"

				dprint('''
Title: {0.title} - Link:[{0.link}]
Subtitle: {article_subtitle}
Id: {0.id}
Author: {0.author}
Published at: {0.published}
Updated: {0.updated}
Content: {content}
Content Type: {content_type}
Content Base: {content_base}
Content Value: {content_value}
Content XML: {content}
Description: {0.description}
				'''.format(entry,
					article_subtitle=article_subtitle,
					content=content,
					content_type=content_type,
					content_base=content_base,
					content_value=content_value))

				# Generate dictionary with content of news
				# parser content variable, because is a string
				dprint("------------------------------\nRESUME FROM THIS NEWS ITEM:")

				element[entry_element]={}
				soup=BeautifulSoup(content, "html.parser")
				element[entry_element]['title']=entry.title
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
					dprint ("Notice HTML: {}".format(element[entry_element]['text']))	
				else:
					#Twitter is a text in rss news
					for item in soup.find_all("p"):
						try:
							if soup.find_all("p") :
								element[entry_element]['text']='%s'%(item.text.strip())
								element[entry_element]['type']='text'
								dprint ("Notice Text: {}".format(item.text.strip()))
							else:
								element[entry_element]['text']='Not detected'
								dprint ("Notice Text: Not detected")
						except Exception as e:
							print("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
				
				# two checks are necessary to confirm or not type
				if soup.find_all("video"):
					if soup.find_all("video"):
						for item in soup.find_all("video"):
							try:
								element[entry_element]['video']=item['src']
								element[entry_element]['type']='video'
								dprint ("Notice Video: {}".format(item['src']))
							except Exception as e:
								dprint("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
					else:
						element[entry_element]['video']='Not detected'
						dprint ("Notice Video: Not detected")

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
								
								dprint ("Element Entry YouTube/iframe: {}".format(element[entry_element]))
								dprint ("Notice Iframe: {}".format(item))

							except Exception as e:
								dprint("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
					else:
						element[entry_element]['iframe']='Not detected'
						dprint ("Notice Iframe: Not detected")

				if soup.find_all("figure"):
					if soup.find_all("img"):
						# List of images add support to images gallery
						element[entry_element]['image']=[]
						element[entry_element]['type']='image'
						for item in soup.find_all("img"):
							try:
								element[entry_element]['image'].append(item['src'])
							except Exception as e:
								dprint("[RSS](parse_rss_file)(Class Beautiful)Error: %s"%e)
						dprint ("Notice Image: %s"%(element[entry_element]))
					else:
						element[entry_element]['image']='Not detected'
						if element[entry_element]['type'] == 'iframe':
							pass
						elif element[entry_element]['type'] == 'text':
							pass
						else:
							dprint ("Notice Image: Not detected")

				entry_element=entry_element+1

			dprint('\n\n')

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

	def get_entries(self):
		try:
			self.list_rss_file()
			dprint("RESUME FROM ALL NEWS ITEMS IN RSS MERGED TO MAKE SLIDESHOW")
			dprint("%s"%self.news_dict)
			
			return self.news_dict
			
		except Exception as e:
			print("[RSS](__init__)Error: %s"%e)
			return {}

	#def get_entries