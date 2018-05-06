
import random, time
import os, json, shutil

def rand_id():
	"""semplice generatore temporaneo di ID per la richiesta.

	Returns:
		prossimo id per la richiesta
	"""
	mstime = int(round(time.time() * 1000))
	coin = random.randint(0,1000000)
	number = int(str(coin) + str(mstime))
	return format(number, 'x')




class Session():
	
	__path = None
	
	@staticmethod
	def setPath(in_path):
		Session.__path = in_path
	
	@staticmethod
	def existsSession(uid):
		return os.path.exists( Session.__path + "/" + uid  )
		
	
	
	
	
	def __init__(self, uid):
		
		self.uid = uid
		self.path = Session.__path
		self.dir_sess = self.path + "/" + self.uid
		
		self.data = {}
		
		if not os.path.exists( self.dir_sess ):
			os.makedirs( self.dir_sess )
			f = open(self.dir_sess + "/data.js", 'a')
			f.write("{}")
			f.close()
		
		else:
			self.__read_from_file()
			
	def saveImg(self, bin_img):		
		bin_img.save( self.dir_sess + "/" + self.uid )
		self.set("path", self.dir_sess + "/" + self.uid)
	
	
	def getPathImg(self):
		return self.dir_sess + "/" + self.uid


	def __read_from_file(self):		
		with open(self.dir_sess + "/data.js") as json_file:  
			self.data = json.load(json_file)


	def rename(self, newuid):
		
		new_dir_session = self.path + "/" + newuid.split('.')[0]
		
		# 1 rinomina l'immgagine se esiste
		if os.path.exists( self.dir_sess + "/" + self.uid ):
			shutil.move( self.dir_sess + "/" + self.uid , self.dir_sess + "/" + newuid)
		
		# 2 rinomina la cartella della session
		shutil.move( self.dir_sess, new_dir_session)
		
		self.uid = newuid
		self.dir_sess = new_dir_session
		
		self.set("path", self.dir_sess + "/" + self.uid)
		

	def set(self, key, value):

		self.__read_from_file()
		
		self.data[key] = value
		
		with open(self.dir_sess + "/data.js", 'w') as outfile:  
			json.dump(self.data, outfile)

		
	def get(self, key):
		
		self.__read_from_file()
		
		return self.data[key]
		
		
	def getAll(self):
		
		self.__read_from_file()
		
		return self.data

