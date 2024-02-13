#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 18:29:08 2023

@author: joan
"""

import json
from cryptography.fernet import Fernet
import os

def crypter(chaine, cle):
    """
    Cette fonction prend en entrée une chaîne de caractères et une clé de cryptage,
    et retourne la chaîne de caractères cryptée.
    
    Args:
    chaine (str): La chaîne de caractères à crypter.
    cle (bytes): La clé de cryptage.
    
    Returns:
    str: La chaîne de caractères cryptée.
    """
    f = Fernet(cle)
    message = str(chaine).encode('utf-8')
    message_crypte = f.encrypt(message)
    return message_crypte.decode('utf-8')

def decrypter(chaine_cryptee, cle):
    """
    Cette fonction prend en entrée une chaîne de caractères cryptée et une clé de cryptage,
    et retourne la chaîne de caractères décryptée.
    
    Args:
    chaine_cryptee (str): La chaîne de caractères cryptée.
    cle (bytes): La clé de cryptage.
    
    Returns:
    str: La chaîne de caractères décryptée.
    """
    f = Fernet(cle)
    message_crypte = chaine_cryptee.encode('utf-8')
    message = f.decrypt(message_crypte)
    return message.decode('utf-8')


class DictSave(dict):
    """
    Cette classe hérite de la classe dict de Python et permet de sauvegarder un dictionnaire en
    JSON dans un fichier en utilisant une clé de cryptage.
    """
    
    def __init__(self,  fichier, cle='', *args, **kwargs):
        """
        Cette méthode initialise l'objet en chargeant les données du fichier JSON spécifié, ou en
        créant un nouveau dictionnaire vide s'il n'existe pas encore.
        
        Args:
        cle (bytes): La clé de cryptage.
        fichier (str): Le nom du fichier de sauvegarde.
        """
        self.cle = cle
        self.fichier = fichier
        try:
            with open(fichier, 'r') as f:
                if self.cle == '':
                    data = json.load(f)
                else:
                    donnees_cryptees = f.read()
                    donnees = decrypter(donnees_cryptees, cle)
                    data = json.loads(donnees)
                super().__init__(data, *args, **kwargs)
        except FileNotFoundError:
            super().__init__({}, *args, **kwargs)
            self.sauvegarder()
            
    def sauvegarder(self):
        """
        Cette méthode sauvegarde les données du dictionnaire dans le fichier JSON spécifié en
        utilisant une clé de cryptage.
        """
        with open(self.fichier, 'w') as f:
            donnees = json.dumps(self)
            if self.cle != '':
                donnees = crypter(donnees, self.cle)
            f.write(donnees)
    
    def __setitem__(self, key, valeur):
        """
        Cette méthode permet de mettre à jour une valeur en la cryptant au préalable.
        
        Args:
        cle (any): La clé de la valeur à mettre à jour.
        valeur (any): La nouvelle valeur à affecter à la clé spécifiée.
        """
        dict.__setitem__(self, key, valeur)
        self.sauvegarder()

def find_key(name, liste):
    key_crypt = liste.get(name)
    if key_crypt == None:
        liste[name] = Fernet.generate_key().decode('utf-8') # génère une nouvelle clé de cryptage aléatoire
        
    return liste[name]
        
def create_directory(path, directory_name):
    """Crée un dossier avec un nom donné à l'emplacement spécifié s'il n'existe pas déjà."""
    directory_path = os.path.join(path, directory_name)
    if os.path.exists(directory_path):
        print(f"Le dossier '{directory_name}' existe déjà à l'emplacement '{path}'.")
        return None
    else:
        os.makedirs(directory_path)
        print(f"Le dossier '{directory_name}' a été créé avec succès à l'emplacement '{path}'.")
        return directory_path

if __name__ == "__main__":
    ### saugarde de la clef dans config
    config = DictSave('config.json')
    key = find_key('crypt_key', config).encode('utf-8')
    
    mes_donnees = DictSave('data.cry', key)
    print(mes_donnees)
    mes_donnees['API_key'] = {'SableDiffusion':'fvhvjvybkudsgfngndgdg', 'OpenIA':'fvhvjvybku56342dsgfngndgdg'}
    print(mes_donnees)
    print(mes_donnees['API_key'])
    print(mes_donnees['API_key']['SableDiffusion'])
    
    
    ### test cryptage ###
    # cle = Fernet.generate_key() # génère une nouvelle clé de cryptage aléatoire
    # chaine = "Bonjour le monde !"
    # chaine_cryptee = crypter(chaine, cle)
    # print(f"{chaine_cryptee}")
    
    # chaine_decryptee = decrypter(chaine_cryptee, cle)
    # print(chaine_decryptee)


