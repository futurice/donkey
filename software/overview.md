# Software - Overview

---
# Contents
 * [Hardware](hardware/overview)
   - [openCV](hardware/openCV)
   - [hall-effect sensor](hardware/hall-effect-sensor)
   - [pela-blocks](hardware/pela-blocks)
 * **Software**
   - [Web Server](software/web-server)
   - [AI/Machine Learning](software/ai)
---
   

The donkey car software consists of 3 main parts. 

1. Web server 
2. Keras "Pilot" model training scripts 
3. Command Line Utility

The web server is built using the [Tornado - web framework](http://www.tornadoweb.org/en/stable/). It's a web framework designed specifically for asynchronous tasks.

The Keras model training scrip is built using [Tensorflow - Keras](https://www.tensorflow.org/guide/keras) and takes as an input the a series of camera images and json meta data, then outputs a model that gets consumed by `[someone help here]`

The command line utility is a python CLI helper tool you can read more about it on the official docs [here](http://docs.donkeycar.com/utility/donkey/).




  