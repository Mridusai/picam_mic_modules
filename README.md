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
    
