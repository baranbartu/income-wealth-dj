# income-wealth-dj

Mathematical approaches on income/wealth (economic) entries. Predictions over the years, wealth/income inequality factors between two different groups etc.
Regarding Rest API end points are also prepared to make all of them SAAS

# Instructions For MacOS Sierra

```bash
   # PRE condition: export DJANGO_SETTINGS_MODULE=incomewealth.settings
   # 1- Clone repo
   # 2- create "env" directory under the root(income-wealth-dj)
   # 3- go into env and run 'virtualenv income-wealth' (can be specified python
   # version like '--python=/usr/bin/python/2.7.10')
   # 4- go back again to root directory and run 'source env/income-wealth/bin/activate' 
   # 5- Install MySQL: 'brew install mysql'
   # 6- Install brew services first: brew tap homebrew/service
   # 7- Start mysql as a service: brew services start mysql
   # 8- pip install -r requirements.txt 
   #     # In case of error while installing mysqlclient 
   #     8.1- xcode-select --install
   #     8.2- env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install mysqlclient
   # 9- open mysql cli: 'mysql -u root' no password should be specified
   # 10- create database: 'CREATE DATABASE incomewealth CHARACTER SET utf8;'
   # 11- create user: "CREATE USER 'incomewealth'@'localhost' IDENTIFIED BY '8e5HLr7gWas=';" (can be used 'openssl rand -base64 8' for random password)
   # 12- grant privileges: GRANT ALL PRIVILEGES ON incomewealth.* TO 'incomewealth'@'%' IDENTIFIED BY '8e5HLr7gWas=' WITH GRANT OPTION; 
   # 13- execute migrations: 'python manage.py migrate' it will also populate the db with initial data
   # 14- create super user (optional): python manage.py createsuperuser
   # 15- run tests: coverage run manage.py test -v 2
   # 16- run server: python manage.py runserver
   # ENJOY! all the endpoints are under the localhost:8000/api/v1/
```

# Docker Instructions (Also MacOS Sierra)

```bash
   # 1- brew install docker docker-compose docker-machine xhyve docker-machine-driver-xhyve
   # 2- sudo chown root:wheel $(brew --prefix)/opt/docker-machine-driver-xhyve/bin/docker-machine-driver-xhyve
   # 3- sudo chmod u+s $(brew --prefix)/opt/docker-machine-driver-xhyve/bin/docker-machine-driver-xhyve
   # 4- docker-machine create default --driver xhyve --xhyve-experimental-nfs-share
   # 5- eval $(docker-machine env default)
   # 6- docker-compose up
   # 7- get docker machine ip and visit 8080. port: "docker-machine ls | awk '{print $5}'"
   # ENJOY!
```

~~# P.S. Currently there is a little incident while running docker which will be resolved in a few days~~
