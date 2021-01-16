# Installation of clarifai in "spyder"/"anaconda terminal": pip install clarifai

# Importing needed libraries:
# 1- Clarifai API libraries:
from clarifai.rest import ClarifaiApp

# 2- Dealing with files library:
import os
import shutil



# Gets the current path of the folder that the code is in (I put this in so that you don't have to change the code everytime you want to run this on a different computer/server):
current_directory = os.getcwd()

# Gets the seperator for the filepath (e.g. / , // , \ , \\) so that this program will be able to work on Linux, Mac and Windows:
seperator = os.sep

# Important folders and paths that we will be using a lot (The first 3 can be changed):
IMPORT_FOLDER = 'AllPhotos'
UPLOAD_FOLDER = 'NatureOrWeather'
UPLOAD_FOLDER_2 = 'everything_else'
abs_dir = current_directory+seperator+IMPORT_FOLDER
nature_dir = current_directory+seperator+UPLOAD_FOLDER
everything_dir = current_directory+seperator+UPLOAD_FOLDER_2

#Lists of nature and weather indicating keywords and a list of keywords that nullify the photo from being a nature photo:
nature_tags = ["iceberg","arctic","raindrop","glacier",'foam',"calamity","horizontal plane","horizontal","hay","drop","smoke","freshness","wet","beach","cave","cliff",'flora','dew',"coast",'cloud',"countryside","ocean","field",'sun',"sunny","clouds","cloudy","water","sea","sky","clear","forest","hill","desert","environment","lake","mountain","island","land","meadow","rainforest","river","valley","volcano","rain","rainy","cold","hot","hurricane","wild","grass","flower","flowers","tree","trees","leaf","mud","sand","smog","wood","no people","rock","rocks","wind","windy","scenery","shrubs","soil","waterfall","wave","autumn","winter","summer","Earth","ice","flood","spring","fall","sunshine","bay","no person","burnt","trunk","sunbeam","nature","dawn","branch","growth","landscape", "tornado","snow","lightning","galaxy","meteorology","thunderstorm","livestock","agriculture","frost","garden","farm","noon","sandstone","fog","lawn","backyard","mist","windshield","danger","condensation","downpour","hot spring","bright","seashore","outdoors","fair weather","cyclone","weather","grow","skyline","Crater","daylight","wooden","rainbow","travel","storm","steam","sunset","season","dry","tourism","icee","snowstorm","panoramic","flame","blue sky","explosion","thunder","eruption","dust","snowy","ash","dusk","air pollution","frozen","climate change","pollution","canyon","heat","rural","arson","arid","wreck","air","waterfront","destruction","lava","surf","mountain peak","park","lapland","H2O","spray","frosty","underwater","grassland","light","melting","bark","seascape","atmosphere","tropical","geology","wildfire","open field","cloudiness","stream","hayfield","outside","cloudscape","dark","evening","cityscape","silhouette","sight","illuminated","landmark","high","trip (journey)","tallest","fungus","exploration","window","bomb","missile","yard","harbor","side view","purity","cropland","eerie","vehicle window","scenic","haze","geyser","rescue","flower arrangement","aircraft","melt","courtyard","icy","ski resort","snowdrift","rush","snow-white","frosty weather","snowflake","ground","tide","drip","flow","liquid","ripple","stone","bubble","midair","geothermal","hole","droplet","splash","geological formation","horizon","backlit","space","moon","shadow","astronomy","charcoal","burn","campfire","coal","charcoal","evergreen","eclipse","full moon","snowscape","global warming","chilled","dune","silhouetted","icicle","glazed","Earth surface","dirty","marine","Greenland","windmill","turbine","docklands","planet","constellation","celestial","universe","astrology","low tide","quiet","solar system","comet","pier","solar","stellar","Jupiter","aerial","openair","marina","submarine","lush","climb","farmhouse","suburb","thermal","crop","bud","sill","earthquake","aquatic","boiling liquid","farmland"]
nullifying_tags = ['person','girl','boy','man','woman', 'adult','architecture','people','wildlife','cat','dog','animal','fur','house','building','technology','car','vehicle','transportation','bus',"wheel","mammal","industry","chair","train station","transportation system","food","furniture","family","home","cattle","church","auto racing","cooking","street","canine","ocean cruise","apartment","urban","skyscraper","bridge","pavement","pet","insect","accident","hotel","tower","bird","town","police","crowd","construction worker","roof","traffic","cow","portrait","festival","vacation","business","road","downtown","luxury","hike","restaurant","adventure","zoo","soccer","modern","city","pool","medicine","truck","ferry","leisure","art","illustration","vector","christmas tree","prey","indoors","Christmas",'son','athlete','love','scientist','club','smile','birthday','cowman','baby','room','teacher','party','shirtless','femme','brunette','child','class','painter','recreation','body','laughing','headshot','eyeglasses','beer','ballet dancer','cyclist','eye','cowboy','joy','adolescence','enjoyment','herdsman','swimming pool','paw','groom','sports fan','blond','school','youth','nightclub','wedding','guy','coffee','rum','tea','goalkeeper','quarterback','whisky','model','tequila','vectors','swimming','beautiful','lady','fighter','driver','jogger','singer','classroom','hiking','uniform','little','World Wide Web','drink','ingredients','graph','young','actress','rally','lips','camper','liquor','cocktail','bar','actor','puppy','friendship','concert','nude','face','swimmer','togetherness','winery','adolescent','facial expression','telephone','biker','squad','offspring','skater','group together','bride','military','golfer','musician','referee','nightlife','pitcher','sunglasses','football player','kitten','tourist','racer','army','poolside','runner',"relaxation",'celebration','couple','stadium','alcohol','bomber','wear','ballerina','student',"rider","bridle","fun","fashion","horse","equestrian","umbrella","handmade","design","table","creativity","desktop","plastic","bucket","decoration","tent","war","domestic","cavalry","mare","bedroom","audience","samurai","dancer","songwriter","flamenco","instrument","thief","gin","guitarist","writer","vodka","soda","profile"]

# The file extenxions that are allowed in the program(you can add to them/remove some from the list depending on your needs):
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','mp4','mov'])

# A function that returns True if the file is allowed in the program (has one of the allowed extensions) or not:
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# A funciton that uses the API and moves the images according to their tags
def predicting():
	for filename in os.listdir(abs_dir):

		# Checks if the photo/video's extension is one of the allowed extension. If it isn't it prints The file extension isn't allowed:
		if allowed_file(filename):

			# Image or video's absolute path:
			abs_file = current_directory+seperator+IMPORT_FOLDER+seperator+filename
			
			# Returns True if the file in that path exists and if not it prints The file path does't exist:
			if os.path.isfile(abs_file) == True:
				tags= []
				nullifying_tags_found=[]
				total = []
				if filename.rsplit('.', 1)[1].lower() == 'mp4' or filename.rsplit('.', 1)[1].lower() == 'mov':

					# This line uses the model to predict what is in the video using the file path for the video(If you want it to predict by url use: model.predict_by_url(url='INSERT_URL_HERE', is_video=True, sample_ms=1000) ):
					response = model.predict_by_filename(abs_file, is_video=True, sample_ms=1000)
					i=1
					for frame in response['outputs'][0]['data']['frames']:
						print("All the keywords for frame number "+str(i)+" in the file " +filename+" are : [",end="")
						i+=1
						for concept in frame['data']['concepts']:
							print(concept["name"],end=', ')
							# Checks if the predicted tag is in the list of nullifying keywords. If it is, it adds the photo to the everything_else folder:
							if concept["name"] not in total:
								total.append(concept["name"])
							if concept["name"] in nullifying_tags:
								if concept['name'] not in nullifying_tags_found:
									nullifying_tags_found.append(concept["name"])

							# Checks if the predicted tag is in the list of nature/weather keywords. If it is, it adds the predicted tag to a list:
							elif concept["name"] in nature_tags:
								if concept['name'] not in tags:
									tags.append(concept["name"])
							
					print("]\n")
				else:

					# This line uses the model to predict what is in the image using the file path for the image(If you want it to predict by url use: model.predict_by_url(url='INSERT_URL_HERE') ):
					response = model.predict_by_filename(abs_file)
					# Getting the predictions from the response:
					for frame in response["outputs"]:
						
						print("All the keywords for "+ filename+" are : [",end="")
						for concept in frame["data"]["concepts"]:
							print(concept["name"],end=', ')
							if concept["name"] not in total:
								total.append(concept["name"])
							if concept["name"] in nullifying_tags:
								nullifying_tags_found.append(concept["name"])
							elif concept["name"] in nature_tags:
								tags.append(concept["name"])

						print("] \n")
				# Moves the photo to one of the 2 folders and prints whether it's a nature photo or not:
				if len(tags)>len(nullifying_tags_found) or len(tags)/len(total) >=0.5:
					print("Nature/weather photo because these tags: "+str(tags)+" were more than the nullifying tags: "+str(nullifying_tags_found)+"\n\n\n\n")
					shutil.move(abs_file, nature_dir)
				else:
					if len(tags)<=len(nullifying_tags_found):
						print("Not a nature photo because nullifying tags: " +str(nullifying_tags_found)+" were more than the nature/weather tags \n\n\n\n")
						shutil.move(abs_file, everything_dir)

			else:
				print("The file path "+abs_file+" doesn't exist\n\n\n\n")
		else:
			print("The file's extension is not allowed\n\n\n\n")
	return 1

print("\n")

# A list of API keys. It's here so that the program can run for a longer time and predict 41,000 images before it stops(each key can take only 1000 requests per month):
keys = [KEYS HERE]

# The default reponse is test failed. This changes if a prediction was made:
response = 0

for key in keys:
	status = None

	# Tests if the key can take requests and if it can the program will continue and predict. If it fails, it will print "The key is not valid" and it will try the next key. If it succeeds it will make a prediction. :
	try:
		app = ClarifaiApp(api_key=key)

		# Creates a model that we will use to make predictions:
		model = app.public_models.general_model

		status = True
	except:
		print("The key "+key+ " is not valid\n")
		status = False
	if len(os.listdir(abs_dir)) ==1 and os.listdir(abs_dir)[0]=='.DS_Store' or len(os.listdir(abs_dir))==0:
		print("There are no files in "+IMPORT_FOLDER+" to predict")
		response=1
		break
	if status == True:
		try:
			response = predicting()
			
		except:
			print("Can't predict using "+key+"\n\n")
			response=0
	# If there are no more files to predict the program will stop.

			
		
# Prints this if all the keys fail and no prediction was made:
if response ==0:
	print("All the keys aren't valid")
