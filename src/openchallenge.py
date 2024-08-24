import sys
sys.path.append('/home/pi/TurboPi/')
import time
import HiwonderSDK.Board as Board
import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO 

Board.setPWMServoPulse(5, 1500, 100) #Arm ESC
Board.setPWMServoPulse(1, 1444, 10) #Set Servo to 85
time.sleep(6)
frames=0
count=0
endFrames = 0

turning = False
turnDirection = None
PD = False

difference = 0
lastdifference = 0

displayLeftArea = 0
displayRightArea = 0
displayTurnCount = 0
displayTurning = 'PD Controller'

font = cv2.FONT_HERSHEY_SIMPLEX

#Camera setup
picam2=Picamera2()
picam2.preview_configuration.main.size = (640,480) #Camera Resolution
picam2.preview_configuration.main.format='RGB888'
picam2.preview_configuration.align()
picam2.preview_configuration.controls.FrameRate=30 #Camera Framerate
picam2.configure("preview")
picam2.start()
if __name__ == '__main__':
    key2_pin = 16
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(key2_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    # turn off LED
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
    Board.RGB.show()
    
    # turn LED green
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))
    Board.RGB.show()
    time.sleep(1)
    
    while GPIO.input(key2_pin) == GPIO.HIGH:
        pass
    
    # turn off LED
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
    Board.RGB.show()
    
    angle = 85.045
    pw_Servo = angle * 11.1 + 500
    Board.setPWMServoPulse(5,1315,100) #Speed
    while True:
        leftarea=0
        leftcontourindex=0
        rightarea=0
        rightcontourindex=0
        
        im = picam2.capture_array()
        
        subim=im[280:345,0:200] #Setting left wall detection area
        subim2=im[280:345,440:640] #Setting right wall detection area
    
        points = [(0,280), (200,280), (200,345), (0,345)]
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, points[0], points[1], color, thickness)
        image = cv2.line(im, points[1], points[2], color, thickness)
        image = cv2.line(im, points[2], points[3], color, thickness)
        image = cv2.line(im, points[3], points[0], color, thickness)
    
        points = [(440,280), (640,280), (640,345), (440,345)]
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, points[0], points[1], color, thickness)
        image = cv2.line(im, points[1], points[2], color, thickness)
        image = cv2.line(im, points[2], points[3], color, thickness)
        image = cv2.line(im, points[3], points[0], color, thickness)
    
        imgGray = cv2.cvtColor(subim, cv2.COLOR_BGR2GRAY) #Grayscaling for thresholding 
        ret, imgThresh = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(contours)): #finding largest contour
            cnt = contours[i]
            if cv2.contourArea(cnt) > leftarea:
                leftarea = cv2.contourArea(cnt)
                leftcontourindex = i
        if(leftarea > 0): 
#             print('Left wall: ',leftarea) #Displaying left contour area
            cv2.drawContours(subim, contours, i, (0, 255, 0), 2) #drawing left largest contour
            displayLeftArea = str(int(leftarea))
            cv2.putText(im, displayLeftArea, (7, 250), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
    
        #Right Wall
        imgGray2 = cv2.cvtColor(subim2, cv2.COLOR_BGR2GRAY) #Grayscaling preperation
        ret2, imgThresh2 = cv2.threshold(imgGray2, 50, 255, cv2.THRESH_BINARY_INV)
        contours2, hierarchy2 = cv2.findContours(imgThresh2,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(contours2)):
            cnt2 = contours2[i]
            if cv2.contourArea(cnt2) > rightarea:
                rightarea = cv2.contourArea(cnt2)
                rightcontourindex = i 
        if(rightarea > 0):
#             print('Right Wall: ',rightarea) #displaying right contour area
            cv2.drawContours(subim2, contours2, i, (0, 255, 0), 2) #drawing largest right contour
            displayRightArea = str(int(rightarea))
            cv2.putText(im, displayRightArea, (450, 250), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
#         cv2.imshow("contours2", im)
        
        print("TURN COUNT:", count)
        print("Turning?:", turning)
        print("Turn Direction:", turnDirection)
        
        displayTurnCount = str(int(count))
        cv2.putText(im, displayTurnCount, (560, 60), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
        
        cv2.putText(im, displayTurning, (7, 60), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
        
        if not turning: 
            if leftarea < 100: #Sharp turn left
                turning = True
                turnDirection = 'left'
                print("TURNING LEFT")
                        
            elif rightarea < 100: #Sharp turn right
                turning = True
                turnDirection = 'right'
                print("TURNING RIGHT")

        if turnDirection == 'left' and turning == True:
            Board.setPWMServoPulse(1,1832, 1)
            frames += 1
            print("frames:",frames)
            displayTurning = 'Turning Left'
            if frames>35:
                count+=1
                frames=0
                
        elif turnDirection == 'right' and turning == True:
            Board.setPWMServoPulse(1,955, 1)
            frames += 1
            print("frames:",frames)
            displayTurning = 'Turning Right'
            if frames>35:
                count+=1
                frames=0
        
        if turning == True and leftarea > 250 and rightarea > 250:
            turning = False
            turnDirection = None
            lastdifference = 0
            
        if not turning and turnDirection == None:
            #PD CONTROLLER 
            print("PD ACTIVATED")
            displayTurning = 'PD Controller'
            difference = rightarea - leftarea
            correction = 0.005 * difference + 0.001 * (difference - lastdifference)
            angle = 85.045 + correction
            
            if angle > 120:
                angle = 120
            elif angle < 40:
                angle = 40
            
            pw = int(11.1 * angle + 500)
            Board.setPWMServoPulse(1, pw, 1)
            lastdifference = difference
    
        if count>=12: #all turns have been completed
            endFrames+=1
            
            if endFrames > 85: #counting frames to ensure robot ends in correct place
                Board.setPWMServoPulse(5,1500,100) #Stopping the motor
                Board.setPWMServoPulse(1,1500,100) #Straightening wheels
                break #exiting loop 
        
        if len(sys.argv) > 1 and sys.argv[1] == 'Debug': #Debug mode
            cv2.imshow('contours2', im)
        
            if cv2.waitKey(1)==ord('q'):
                Board.setPWMServoPulse(5,1500,100)
                Board.setPWMServoPulse(1,1444,100)
                cv2.destroyAllWindows()
                break
        
cv2.destroyAllWindows()