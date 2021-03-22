#import evdev
from evdev import InputDevice, categorize, ecodes
from laberel import sendToPrinter
from label import generateLabel

#creates object 'gamepad' to store the data
#you can call it whatever you like
buttonsPad = InputDevice('/dev/input/event2')
imgFolder = '/home/pi/csf-labeler/Imaging/'

#print label
blueBtn = 291
#start new count new lot
yellowBtn = 290
#pause machine
redBtn = 289
#re-print last label
greenBtn = 288

pause = False
count = 0
dayLot = 1
lastLabel = ''

#Update state
def updateCount():
    global count
    count = count + 1
    
def updateLastLabel(label):
    global lastLabel
    lastLabel = label

#Start new lot and count
def startNewLot():
    global dayLot, count
    dayLot = dayLot + 1
    count = 0
    
def setPause():
    global pause
    pause = not pause
    
#prints out device info at start
print(buttonsPad)

#evdev takes care of polling the controller in a loop
for event in buttonsPad.read_loop():
    #print(categorize(event))
        #filters by event type
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            #print(event)
            if event.code == blueBtn and not pause:
                print("Blue Btn pressed")
                updateCount()
                label = generateLabel(dayLot, count)
                route = imgFolder + label
                updateLastLabel(label)
                sendToPrinter(route)
                #print(event)
            if event.code == yellowBtn and not pause:
                print("Yellow Btn pressed")
                startNewLot()
                #   print(event)
            if event.code == redBtn:
                print("Red Btn pressed")
                setPause()
                #print(event)
            if event.code == greenBtn and not pause:
                print("Green Btn pressed")
                route = imgFolder + lastLabel
                sendToPrinter(route)
                #print(event)