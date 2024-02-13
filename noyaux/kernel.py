import noyaux.FilesManager as fm

CONFIG_FILE_NAME = '.config'
LASTE_PATH_NAME = 'projet_path'
CRYPTO_KEY_NAME = 'crypt_key'
API_KEYS = 'API_keys'

class Video_Project():
    def __init__(self, path):
        self.path = path

class Kernel():
    def __init__(self):
       
        self.config = fm.DictSave(CONFIG_FILE_NAME)
        self.config[CRYPTO_KEY_NAME] = fm.find_key(CRYPTO_KEY_NAME, self.config)
    
    def get_project_path(self):
        return self.config.get(LASTE_PATH_NAME)
    
    def new_project(self, path, directory_name):
        # création d'un nouveau dossier
        path = fm.create_directory(path, directory_name)
        # Ajout du chemain du dossier à la liste des projet
        if path != None: self.config[LASTE_PATH_NAME] = path
        return path
        
    def open_project(self):
        # ouvrir un fichier
        pass
    
    def get_cle(self):
        return self.config[CRYPTO_KEY_NAME]
    
    def save_crypt_data(self, key, value, cle=None):
        # save data crypted by key
        if cle == None: cle = self.get_cle()
        data = fm.crypter(value, cle)
        self.config[key] = data
    
    def get_crypt_data(self, key, cle=None):
        # get data crypted by key
        if cle == None: cle = self.get_cle()
        data = self.config.get(key)
        if data == None:
            return None
        else:
            return eval(fm.decrypter(self.config[key], cle))
        
    def save_data(self, value, key):
        #set config file
        if key == None:
            key = LASTE_PATH_NAME
        self.config[key] = value
    
    def get_data(self, key=None):
        # get config file data
        if key == None:
            key = LASTE_PATH_NAME
        return self.config.get(key)