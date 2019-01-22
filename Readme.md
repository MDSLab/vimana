# Vimana

> Vimana is a Sanskrit word meaning flying object, and in ancient Vedic texts and Indian epics, Vimanas are described as vehicles used by the "gods" to travel the sky, fight wars again each other, and spread wealth and knowledge among primitive ancient people.

Viamana aims to solve the problem of centralised powers in AI.  

Using Tendermint POS BFT system.

Python 3.6.5+

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