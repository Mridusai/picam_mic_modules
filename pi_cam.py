import io
import time
import picamera
from PIL import Image

with picamera.PiCamera() as camera:
    # VGA at 40 fps
    camera.resolution = (640, 480)
    camera.framerate = 80
    time.sleep(2)
    for data in range(1250)
            outputs = [io.BytesIO() for i in range(40)] #Using 40 here as we will be resetting memory stream every second
            camera.capture_sequence(outputs, 'jpeg', use_video_port=True)
            count = 0
            for frameData in outputs:
                rawIO = frameData
                rawIO.seek(0)
                byteImg = Image.open(rawIO)
                count += 1
                filename = data + "image" + str(count) + ".jpg"
                byteImg.save(filename, 'JPEG')

