# micropython-esp32cam-to-googleDrive
Source code and tutorial: How to upload a photo taken in esp32cam-micropython to google Drive Folder


I've searched in many repos a solution to upload a image using the [ESP32-cam](https://esp32.com/) running [micropython](https://github.com/micropython/micropython). To implent this solution we need to install an esp32cam firmware, which is **NOT PRESENT** in [official micropython repository](http://micropython.org/download). I recommend the firmwares in [shariltumin esp32cam micropython repo](https://github.com/shariltumin/esp32-cam-micropython). Unfortunately, I could not build my own firmware so far. The working solution is based in [Guillermo Sampallo esp32cam tutorial](https://www.gsampallo.com/blog/2019/10/13/esp32-cam-subir-fotos-a-google-drive/) and [arduino code](https://github.com/gsampallo/esp32cam-gdrive).
