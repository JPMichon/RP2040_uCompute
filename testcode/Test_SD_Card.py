from machine import Pin
import uos
import sdcard
import utime


_MicroSD_Detect = 7 # détection de la présence d'ube carte MicroSD (GP07)
_Led_System = 25 # définition du port pour le del systeme (GP25)
_CD_SDCARD = 13 # définition du port Pour le Select du SDCARD

#Initialisation des IOs
System_LED = Pin(_Led_System,Pin.OUT)
MicroSD_Detect = Pin(_MicroSD_Detect,Pin.IN)

def TestSDCARD():
    CS = machine.Pin(_CD_SDCARD, machine.Pin.OUT)
    spi = machine.SPI(1,baudrate=1000000,polarity=0,phase=0,bits=8,firstbit=machine.SPI.MSB,sck=machine.Pin(14),mosi=machine.Pin(15),miso=machine.Pin(12))

    sd = sdcard.SDCard(spi,CS)

    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
    print("--- Initialisation de la carte ---")
    # Print SD card size
    print("Size: {} MB".format(sd.sectors/2048))
    print("--- Contenu de la carte ---")
    # List SD contents
    #print(uos.getcwd())
    print(uos.ilistdir("/sd"))
    print("-----------------------------")
    # Create a file and write something to it
    with open("/sd/data.txt", "w") as file:
        print("Writing to data.txt...")
        file.write("Welcome to microcontrollerslab!\r\n")
        file.write("This is a test\r\n")

    # Open the file we just created and read from it
    with open("/sd/data.txt", "r") as file:
        print("Reading data.txt...")
        data = file.read()
        print(data)    
    # List SD contents
    print(os.ilistdir("/sd"))
    uos.umount("/sd")
    print("--- Test complété ---")
    
def SDCARD_detect():
    print("")
    if MicroSD_Detect.value()==0:
        print ("Carte MicroSD présente")
    else:
        print ("Carte MicroSD absente")
    print("")
    
    
while True:
    TestSDCARD()
    utime.sleep(5)    