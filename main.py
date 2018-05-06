
from pprint import pprint

from core import ImageClassifier
from core import CategoryClassifier
from core import Utility
from core.Utility import Session


#### dipendenze del webservice
import os.path
from flask import Flask, request, jsonify
from flask.templating import render_template
from flask.helpers import flash, send_from_directory


### inizializzazioni..
current_dir = os.path.dirname(os.path.realpath(__file__))
SESSION_FOLDER = current_dir + '/session'

ImageClassifier.MODEL_DIR = current_dir + '/imagenet/'

CategoryClassifier.NLTK_PATH = current_dir + '/nltk_data'
CategoryClassifier.init()

Session.setPath(SESSION_FOLDER)
########


app = Flask(__name__)

app.config.update(dict(
	SESSION_FOLDER=SESSION_FOLDER,
	SECRET_KEY="YOUR_SECRET_KEY"
))




@app.route("/api/hello")
def hello():
	return "Hello from AISearchImage!"


@app.route("/api/search/", methods=['POST'])
def first_step():

	#if request.method == 'POST':
		
	#cap = request.form['cap']
	#pprint("----------------------------------cap : " + cap)
		
	cap = request.form.get('cap')
	lat = request.form.get('lat')
	lng = request.form.get('lng')
	position = {'lat': lat, 'lng': lng, 'cap': cap}
	pprint('position')
	pprint(position)

	
	if 'img' in request.files:

		output = {}
		
		new_id = Utility.rand_id();
		s = Session(new_id)

		imgfile = request.files['img']
		s.saveImg(imgfile)
		s.set('position', position)

		######id_file_imgur = ImageUploader.upload_image( s.getPathImg() )
		
		######s.rename(id_file_imgur)
		
		
		
		
		
		imgfile = s.getPathImg()
		
		output["id_request"] = new_id
		output["recognition"] = ImageClassifier.run_inference_on_image(imgfile)

		## cerca la categoria associata, da gestire meglio...
		word_context = output["recognition"][0]["uid_wordnet"]

		output["category"] = CategoryClassifier.find_category( word_context ).split(".")[0]
		
		output["associated_objects"] = CategoryClassifier.get_associated_objects( output["category"] )

		output["services"] = CategoryClassifier.get_services_by_object( output["category"] )
		
		s.set("result", output)


		return jsonify(output)	


@app.route("/api/search/<id_request>")
def second_step(id_request):

	if not Session.existsSession(id_request) :
		return jsonify("Error, id_request not exists")
		

	action = request.args.get('action')
	if action == None :
		return jsonify("Error, define an action (as param)")
	
	
	s = Session(id_request)
	session_data = s.getAll()
	category = session_data["result"]["category"]
	#first_label = recognition_result["recognition"][0]["label"].split(", ")[0]
	

	#urlImage = 'https://i.imgur.com/' + id_request
	nameCrawlerService =  CategoryClassifier.get_crawler_service(category, action)
	
	pprint("nameCrawlerService : " + nameCrawlerService)
	#pprint("first_label : " + first_label)
	
	module = __import__("crawlers."+nameCrawlerService, fromlist=[nameCrawlerService])
	classCrawlerService = getattr(module, nameCrawlerService)
	crawler = classCrawlerService()


	#result = SearchCrawler.reverseImageSearch(urlImage, tag_url)
	result = {}
	result["data"] = crawler.run( s.getAll() )
	result["type_result"] = crawler.getTypeAction().name

	return jsonify(result)


@app.route("/api/search/<id_request>/<associated_obj>")
def second_step_associated(id_request, associated_obj):
	
	s = Session(id_request)
	
	category = s.get("result")["category"]
	
	tag_url = CategoryClassifier.get_tag_url_associated_obj(category, associated_obj)
	query = category + " " + associated_obj
	
	#result = SearchCrawler.simpleSearch(tag_url, query)
	result = 'MAGIC-STUB for associated object!!'
	
	return jsonify(result)



##################### WEB INTERFACE #########################

@app.route("/api/img/<id_request>")
def serve_img(id_request):
	return send_from_directory(app.config['SESSION_FOLDER'], id_request+"/"+id_request )

@app.route("/")
def index_action():
	return render_template("index.html")


@app.route("/search/<id_request>")
def first_search(id_request):
	
	if not Session.existsSession(id_request) :
		return render_template("error.html", message="Wrong id_request!!" )
	
	s = Session(id_request)
	
	result = s.getAll()
	result["result"]["first_label"] = result["result"]["recognition"][0]["label"].split(", ")[0]
	
	action = request.args.get('action')
	
	if action != None :
		result["result"]["action"] = action
		return render_template("search_action.html", data=result)
	

	return render_template("search_result.html", data=result)






if __name__ == "__main__":
    app.run(ssl_context=('ssl_files/cert.pem', 'ssl_files/key.pem'))