#!/usr/bin/env python3
import os
import shutil
import tempfile
#from jinja2 import Environment
#from jinja2.loaders import FileSystemLoader

class AUTOSLIDESHOW():

	#file_slideswhow="/www/var/slideshow/carrusel/kiosco_slideshow.html"
	file_slideswhow=tempfile.NamedTemporaryFile().name
	install_dir='/var/www/slideshow/modules/'
	template=install_dir+"slideshow_template.html"
	css=install_dir+"style_slideshow.css"
	
	def initialize (self,file=file_slideswhow):
		try:
			
			file_dir=os.path.dirname(file)
			file_dir_extras=file_dir+'/modules'
			if not os.path.exists(file_dir):
				os.makedirs(file_dir)
				#print("Directory not exists, generate it...")

			if not os.path.exists(file_dir_extras):
				os.makedirs(file_dir_extras)
				#print("Directory not exists, generate it...")

			if os.path.isfile(file):
				os.remove(file)
			css_file=file_dir_extras+'/style_slideshow.css'
			shutil.copyfile(self.css,css_file)

			#shutil.copyfile(self.template,self.file_slideswhow)
			inputfile = open(self.template,'rt',encoding='utf-8').readlines()
			write_file = open(self.file_slideswhow,'w',encoding='utf-8')
			for line in inputfile:
				write_file.write(line)
			write_file.close()

		except Exception as e:
			print("[AUTOSLIDESHOW](initialize)Error: %s"%e)

	#def initialize



	def add_elements (self,dict):
		try:
			self.initialize()
			if len(dict) > 0:
				for element in dict:
					print(element)
					if 'text' in dict[element]['type']:
						self.text(dict[element])
					elif 'image' in dict[element]['type']:
						self.image(dict[element])
					elif 'video' in dict[element]['type']:
						self.video(dict[element])
					elif 'iframe' in dict[element]['type']:
						self.iframe(dict[element])
					elif 'youtube' in dict[element]['type']:
						self.youtube(dict[element])
			else:
				dict={}
				dict[0]={}
				dict[0]['title']='No news detected'
				dict[0]['type']='text'
				dict[0]['text']="Please review your RSS file. Actually we can't find it or it's empty"
				self.text(dict[0])
				
			self.write_css(self.file_slideswhow,self.css)
			return (self.read_slideshow(self.file_slideswhow))

		except Exception as e:
			print("[AUTOSLIDESHOW](add_elements)Error: %s"%e)

	# def add_elements



	def text(self,element):
		try:
			list=[]
			list.append('<div class="mySlides mySlides_txt fade" style="background-color: yellow">'+"\n")
			list.append('<p class="author">%s</p>'%element['title']+"\n")
			list.append('<q>%s</q>'%element['text']+"\n")
			list.append('</div>'+"\n")

			self.write_slideshow(self.file_slideswhow,list)

		except Exception as e:
			print("[AUTOSLIDESHOW](text)Error: %s"%e)
	#def text


	def image(self,list_images):
		try:
			list=[]
			for element in list_images['image']:
				list.append('<div class="mySlides fade">'+"\n")
				list.append('<img src="{}" style="width:100%">'.format(element)+"\n")
				list.append('<div class="text_top">%s</div>'%list_images['title']+"\n")
				list.append('</div>'+"\n")

			self.write_slideshow(self.file_slideswhow,list)
		except Exception as e:

			print("[AUTOSLIDESHOW](image)Error: %s"%e)
	#def image


	def video(self,element):
		try:
			list=[]
			list.append('<div class="mySlides fade">+"\n"')
			list.append('<video id="video" width="800" height="600" allowfullscreen autoplay muted>'+"\n")
			list.append('<source src="%s" type="video/ogg" />'%element['video']+"\n")
			list.append('<div class="text_top">%s</div>'%element['title']+"\n")
			list.append('</video>'+"\n")
			list.append('</div>'+"\n")

			self.write_slideshow(self.file_slideswhow,list)
		except Exception as e:
			print("[AUTOSLIDESHOW](video)Error: %s"%e)
	#def text


	def youtube(self,element):
		try:
			list=[]
			print(1111111111)
			list.append('<div id="player" class="mySlides fade"></div>'+"\n")
			print(22222222)
			self.write_slideshow(self.file_slideswhow,list)
			print(333333333)
			self.write_slideshow_youtube(self.file_slideswhow,element)
		except Exception as e:
			print("[AUTOSLIDESHOW](iframe)Error: %s"%e)
	#def youtube
	
	def iframe(self,element):
		try:
			list=[]
			list.append('<div class="mySlides fade">'+"\n")
			list.append('%s'%element['iframe']+"\n")
			list.append('<div class="text_top">%s</div>'%element['title']+"\n")
			list.append('</div>+"\n"')

			self.write_slideshow(self.file_slideswhow,list)
		except Exception as e:
			print("[AUTOSLIDESHOW](iframe)Error: %s"%e)
	#def iframe
	
	def write_css (self,file,file_css):
		try:
			inputfile = open(file,'rt',encoding='utf-8').readlines()
			write_file = open(file,'w',encoding='utf-8')
			css_lines=open(file_css,'rt',encoding='utf-8').readlines()
			for line in inputfile:
				write_file.write(line)
				if '<head>' in line:
					write_file.write("<style>")
					for line_css in css_lines:        
						#write_file.write(item + "\n") 
						write_file.write(line_css)
					write_file.write("</style>")
			write_file.close()

		except Exception as e:
			print("[AUTOSLIDESHOW](write_slideshow)Error: %s"%e)
	#def write_slideshow


	def write_slideshow (self,file,list):
		try:
			print (4444444)
			inputfile = open(file,'rt',encoding='utf-8').readlines()
			write_file = open(file,'w',encoding='utf-8')
			for line in inputfile:
				write_file.write(line)
				if '<div class="slideshow-container">' in line:
					for item in list:        
						#write_file.write(item + "\n") 
						write_file.write(item)
			write_file.close()

		except Exception as e:
			print("[AUTOSLIDESHOW](write_slideshow)Error: %s"%e)
	#def write_slideshow
	
	def write_slideshow_youtube(self,file,element):
		try:
			print(555555)
			inputfile = open(file,'rt',encoding='utf-8').readlines()
			write_file = open(file,'w',encoding='utf-8')
			for line in inputfile:
				if 'onYouTubeIframeAPIReady()' in line:
					write_file.write("var player;\n")
					write_file.write(line)
					write_file.write("player = new YT.Player('player', {")
					write_file.write("height: '%s',"%element['height'])
					write_file.write("width: '%s',"%element['width'])
					write_file.write("videoId: '%s',"%element['id'])
					write_file.write("events: {")
					write_file.write("'onStateChange': function(env){ if (env.data == 0) {alert ('Hola Dani')}; }")
					write_file.write("}")
					write_file.write("});")
				else:
					write_file.write(line)
			write_file.close()

		except Exception as e:
			print("[AUTOSLIDESHOW](write_slideshow)Error: %s"%e)
	#def write_slideshow_youtube
	
	
	def read_slideshow (self,file):
		try:
			slide_show_generated=''
			lines = open(file,'rt',encoding='utf-8').readlines()
			for line in lines:
				slide_show_generated=slide_show_generated+line
				
			return slide_show_generated
			
		except Exception as e:
			print("[AUTOSLIDESHOW](read_slideshow)Error: %s"%e)
	#def read_slideshow



	def __init__(self):
		try:
			pass
		except Exception as e:
			print("[__init__]Error: %s"%e)

	#def __init__

AUTOSLIDESHOW()