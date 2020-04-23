from flask import Flask
from modules.parse_rss import RSS as renderizador

app = Flask(__name__)
mirenderizador = renderizador()

@app.route('/')
def mirender():
	slideshow_created=mirenderizador.start()
	print('')
	print('')
	print (slideshow_created)
	return (slideshow_created)
	
if __name__ == '__main__':
	app.run()
