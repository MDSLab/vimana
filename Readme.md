# Vimana

> Vimana is a Sanskrit word meaning flying object, and in ancient Vedic texts and Indian epics, Vimanas are described as vehicles used by the "gods" to travel the sky, fight wars again each other, and spread wealth and knowledge among primitive ancient people.

                               x___________x
                                    |
                               _   _|_   _
                              (i)-/   \-(i)
       _                         /\___/\                         _
      (G)______xxxxx____________( ( x ) )____________xxxxx______(G)
                                 \_____/

 ,ggg,         ,gg
dP""Y8a       ,8P
Yb, `88       d8'
 `"  88       88  gg
     88       88  ""
     I8       8I  gg    ,ggg,,ggg,,ggg,     ,gggg,gg   ,ggg,,ggg,     ,gggg,gg 
     `8,     ,8'  88   ,8" "8P" "8P" "8,   dP"  "Y8I  ,8" "8P" "8,   dP"  "Y8I 
      Y8,   ,8P   88   I8   8I   8I   8I  i8'    ,8I  I8   8I   8I  i8'    ,8I 
        Yb,_,dP  _,88,_,dP   8I   8I   Yb,,d8,   ,d8b,,dP   8I   Yb,,d8,   ,d8b,
        "Y8P"   8P""Y88P'   8I   8I   `Y8P"Y8888P"`Y88P'   8I   `Y8P"Y8888P"`Y8

    Codename: Angry Arianna

Using Tendermint BFT system.


Python 3.6.5+

> Broken works only for earlier versions.

## Install 

1. Install [tendermint](https://github.com/tendermint/tendermint)

2. Clone this repo and install all the requirements 

optionally create a virtualenv for this 
```

virtualenv venv
source venv/bin/activate
```

go inside the folder 
`cd vimana`

install all the requirements

`pip -r req.txt` 

3. To run the application 


`cd tendermint`

RUN the abci (application blockchain interface)

`python3 app.py`

This will start the abci on port 266658

4. Run Tendermint

first  initalise tendermint

`tendermint init`

`tendermint node`

Use the flags to remove empty blocks optionally.

You should be able to send requests to rendermint now. Send curl requests to 25556

5. Webserver made to send curl requests easily

Go to main folder. 

`cd ..`

`python manage.py runserver`

Now visit port 8000 to send requests to the tendermint node easily. 