from flask import Blueprint, render_template
from ainur.modules.slideshow.parse_rss import RSS

exportmodule = Blueprint('slideshow', __name__, template_folder='templates')
myrss = RSS()

@exportmodule.route('/')
def carrusel_render():

	list_slides = myrss.get_entries()

	if len(list_slides) < 1:
		list_slides[0]={}
		list_slides[0]['title']='No news detected'
		list_slides[0]['type']='text'
		list_slides[0]['text']="Please review your RSS file. Actually we can't find it or it's empty"

	youtube_list = [ list_slides[slide] for slide in list_slides if list_slides[slide]['type'] == 'youtube' ]
	return render_template('slideshow/index.html', list_slides=list_slides, youtube_list=youtube_list)

	
	
if __name__ == '__main__':
	app.run()
