# Futucar

These instructions are shortcuts for more general knowledge found in [donkeycar docs](http://docs.donkeycar.com/)

Install the SW stack using those instructions. If using OSX then remember to use the same version of Tensorflow as in the car (atm ==v 1.8)

Note!! Keras models are NOT compatible between different tensorflow versions!


## Create car

We have our own template, create it to your home folder like this:

   ´donkey createcar --template donkey2futucar ~/futucar´

## Gather training data

TODO using the real car

Or using the simulator, just follow [donkey instructions](http://docs.donkeycar.com/guide/simulator/#typical-use)

## Train the model

    ´cd ~/futucar´
    ´python manage.py train --model=<output-path-to-model> --tub=<path-to-data> --type=<linear|categorical>´   


## Test the model

TODO Either using the car

Or the simulator, first run the server and then using the simulator app.

    ´donkey sim --type <linear|categorical> --model <path-to-model>´

## Doing stuff with the car
You need the wlan router, turn it on. Turn the car on by plugging in
the usb cable to the rasberry pi. The password for the wlan and
raspberry pi are written on the router.

Connect to the raspberry pi

    ´ssh pi@192.168.8.102´

cd to the mycar dir

    ´cd ~/mycar´

to run car and record training data run

    ´python manage.py drive --js´

to see stuff from the camera and debug stuff run

    ´python manage.py drive´
