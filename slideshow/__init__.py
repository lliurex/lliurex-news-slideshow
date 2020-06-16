from flask import Blueprint
from parse_rss import RSS

exportmodule = Blueprint('slideshow', __name__, template_folder='templates')
myrss = Rss()

@exportmodule.route('/')
def carrusel_render():

	list_slides = myrss.get_entries()

	if len(list_slides) < 1:
		list_slides[0]={}
		list_slides[0]['title']='No news detected'
		list_slides[0]['type']='text'
		list_slides[0]['text']="Please review your RSS file. Actually we can't find it or it's empty"

	youtube_list = [ slide for slide in list_slides if slide['type'] == 'youtube' ]
	return render_template('slideshow/index.html', list_slides=list_slides, youtube_list=youtube_list)

	
	
if __name__ == '__main__':
	app.run()
