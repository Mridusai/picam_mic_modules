# picam_mic_modules
Cranfield UKSEDS Avionics Repository

1. For the picams
    As of now,To synchronous stereo is still throwing issues
    Working on stereo individually
    Script for 20 minutes of burst image captures found in pi_cam.py
    Bursts captured at 40fps, stored in buffer memory (1 second stored at a time) and then flushed to SD card
    Script currently runs for 20 minutes
    To make this launch at startup, init.sh needs to be added to cron scheduler
    Steps for this:
      1. Download and copy this rep to home directory
      2. Make init.sh executable with "chmod 755 init.sh" after copying this rep to the pi
      3. cd to home by running "cd"
      4. Create cron logs folder with "mkdir logs"
      5. Using ssh or with external monitor open crontab with "sudo crontab -e"]
      6. Make the init.sh file to launch at startup with the command "@reboot sh /home/pi/picam_mic_modules/init.sh >/home/pi/logs/cronlog 2>&1"

2. For mics
    The pin layout is as follows (Ignore the second mic attached to same rpi as we want redundancy)
    ![sensors_pi_i2s_stereo_bb](https://user-images.githubusercontent.com/36783388/167426438-50c923f8-f044-47dd-bc2d-52750e9ad158.png)
    For Setup:
        1. Download i2s module to the pi using "sudo pip3 install --upgrade adafruit-python-shell" followed by "wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py"
        2. Run the downloaded file using: "sudo python3 i2smic.py"
        3. While running i2smic.py, there is an option to load this module at startup. Press y to auto load at boot
        4. **From here on, work still needs to be done** 
            1. Script similar to pi_cam.py is written for mics and is uploaded as mic.py
            2. Still need to figure out how to run this at startup as our way of running stuff on cron makes running scripts sequential
            3. Code still needs testing with current mics
            4. mono post processing from each side will be done on the same pi in addition to this, we will be stitching each .wav files into a stereo file after moving it out of the pi and into PCs and stereo post processing will be done off pi
            5. Try to make 4 work locally on pi without any time delays
            6. Finally, mono data processing is done locally and for each 1s, therefore, if time permits, real time monitoring of mono channel data can be considered/attempted


