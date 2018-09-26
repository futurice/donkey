# Futucar

These instructions are shortcuts for more general knowledge found in [donkeycar docs](http://docs.donkeycar.com/)

Install the SW stack using those instructions. If using OSX then remember to use newer version of Tensorflow (at least 1.8)

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