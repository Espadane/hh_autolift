from os import getenv
from sys import exit

hh_login = getenv("MY_EMAIL")
if not hh_login:
    exit("Error. User login not found")

hh_password = getenv("MY_PASSWORD")
if not hh_password:
    exit("Error. User password not found")

user_agent = []
ex_path = '/absolute/path/to/chromedriver/' #Абсолютный путь до веб-драйвера, можно узнать находясь в каталоге командой "pwd"
#возможно придется дать права драйверу на исполнение. Делается командой chmod 755 chromedriver - находясь в каталоге
