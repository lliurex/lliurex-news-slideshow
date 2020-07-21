from flask import Blueprint, render_template, send_file
from ainur.modules.slideshow.parse_rss import RSS
from json import load as json_load
import os

exportmodule = Blueprint('slideshow', __name__, template_folder='templates', static_folder='static')
myrss = RSS()

@exportmodule.route('/')
def carrusel_render():

	list_slides = myrss.get_entries()

	if len(list_slides) < 1:
		list_slides[0] = {}
		list_slides[0]['title']='No news detected'
		list_slides[0]['type']='text'
		list_slides[0]['text']="Please review your RSS file. Actually we can't find it or it's empty"

	config = {'slide_timeout':10, 'background_color':'#6eb9d0','title_size':75,'description_size':50,'background_selected':'solid', "transition":"fade"}
	if os.path.exists('/etc/lliurex-news/slideshow.conf'):
		with open('/etc/lliurex-news/slideshow.conf','r') as fd:
			config = json_load(fd)

	youtube_list = [ list_slides[slide] for slide in list_slides if list_slides[slide]['type'] == 'youtube' ]
	return render_template('slideshow/index.html', list_slides=list_slides, youtube_list=youtube_list, config=config)


@exportmodule.route('/background_image', methods=['GET', 'POST'])
def background_image():
    if os.path.exists('/var/lib/lliurex-news/slideshow_background.png'):
        return send_file('/var/lib/lliurex-news/slideshow_background.png')
    return ''
