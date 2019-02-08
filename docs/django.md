# Client side application


> A client side django applcation is there to facilitate easy send of requests to the network. This takes the images and sends requests easily to the nodes.

## Running 

It is assumed that Vimana is installed. 

```
python manage.py runserver
```

should work.

But to create a new instance after deleting the existing db. 


```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```

to start the Django applciation in port `8000`, go to [localhost:8000](http://localhost:8000) to the application. 


After uploading images 

Test is used to test the models locally (Will be removed soon)

Commit is used to send requests to the ABCI.

The result of the applcation will be seen via Django app. 

## Features

Users can 
1. Change models via easy to use interface
2. Upload images and get result easily 

### What is this db ?

The db is sqlite, it's not kept in the blockchain and is only used to store locally information such as models name, accuracy etc. 