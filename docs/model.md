# Machine learning models

## How to change models 

Models can be changed in two ways

1. By using the [Client side](django.md) application
2. By manually adding a file named `model.h5` in `tmserver ` folder.

## Do you give models ?

No, the models are expected to be created by you and uploaded. 

## What kind of data should be send to models ?

The preprocessing for the models will be done in the client side application.
But if you wish to send directly via broadcast_tx_commit endpoint then you need to make sure the data you are sending in base64 formated numpy array of the images

## What type of input should be send for direct curl requests?

At the moment it support black and white images, we are working on this. 