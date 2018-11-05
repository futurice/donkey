# donkeycar: a python self driving library -- THE FUTU FORK
---
# Contents
 * [Hardware](hardware/overview)
   - [openCV](hardware/openCV)
   - [hall-effect sensor](hardware/hall-effect-sensor)
   - [pela-blocks](hardware/pela-blocks)
 * [Software](software/overview)
   - [Web Server](software/web-server)
   - [AI/Machine Learning](software/ai)
---
   
Description of project

# Getting Started - driving
The car's current location is on the 7th Floor in the Helsinki office.

`[picture of location]`

## Checklist Before Driving

 - [ ] 1 white Xbox controller
 - [ ] block to elevate the car wheels off the ground
 - [ ] Check power bank has charge
 - [ ] Plug Raspberry Pi to power bank
 - [ ] 1 Huawai 4g access point / router
 - [ ] Check you can connect to AP over SSID `DonkeyCarWLAN`
 - [ ] Check you have access to AP admin panel
    - Access AP: `192.168.8.1`
    - Username: `admin`
    - Password: `donkeycar4000`
 - [ ] Write down Raspberry Pi's IP address it's host name is `HKI-cowcatcher`
 - [ ] check you can ssh into raspberry pi (`HKI-cowcatcher`)

## Driving
Once you've checked all of the above place the car on the block

`[picture example]`

and turn on the car.

`[picture where the switch is]`

Next, ssh into the pi and start the donkeycar web server with the "joystick flag"

```bash
cd mycar
python manage.py drive --js
```

If everything worked out you should see the on the console output from the xbox controller.

Check that the steering and accelerations works. If its all good you can start driving.

!> The donkey car server records data **only** on throttle.

?> To see stuff from the camera and debug stuff run  `python manage.py drive`

## Contributing Training Data

Once you've driven a few laps around the test course adding that data to [Google Drive](https://drive.google.com/drive/u/0/folders/1FD8rDuJKrGzUeDxjR1MyKP8O-NLbiSWo) will help the AI team further train their models.

[pi to colab](_media/diagrams/pi-to-colab.html ':include :type=html width=100% height=400px')

**Steps to transfer data to Drive**
1. ssh into pi
2. use `~donkeycar/zipForColab.sh` to zip all the files in the `data` folder
```bash
~donkeycar/zipForColab.sh --path /path/to/data/folder
```
3. copy the zipped file to your computer
```bash
scp -r pi@192.168.8.100:/home/pi/mycar/tub/MM_DD_YY_HH_MM_SS_data.zip .
```
5. copy the zipped folder to 