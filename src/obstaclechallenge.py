import sys
sys.path.append('/home/pi/TurboPi/')
import time
import HiwonderSDK.Board as Board
import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import numpy as np

Board.setPWMServoPulse(5, 1500, 100) #Arm ESC
Board.setPWMServoPulse(1, 1444, 10) #Set Servo to 85
time.sleep(6)

#Tracking turns and termination variables
frames=0
count=0
turn_around_count = 0
endFrames = 0
turning = False
turnDirection = None
turnBuffer = False
orange_seen = False

#Global Timer
timer = 0

#PD Controller Variables
difference = 0
lastdifference = 0
PD = False

#Troubleshooting / Displaying Info Variables
displayLeftArea = 0
displayRightArea = 0
displayOrangeArea = 0
displayTurnCount = 0
displayTurning = 'PD Controller'

#Pillar Maneuvering
green_pillar_seen = False
red_pillar_seen = False
last_pillar = None

#Turn Around Variables
turn_around = False
turn_around_frames = 0

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
    
    #Key Press Startup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(key2_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    # turn off LED
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
    Board.RGB.show()
    
    # turn LED white (indicator for start up)
    Board.RGB.setPixelColor(0, Board.PixelColor(255, 255, 255))
    Board.RGB.show()
    time.sleep(1)
    
    while GPIO.input(key2_pin) == GPIO.HIGH:
        pass
    
    # turn off LED
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
    Board.RGB.show()
    
    angle = 85.045 #Angle for straight wheels
    pw_Servo = angle * 11.1 + 500
    Board.setPWMServoPulse(5,1323,100) #Car Speed
    while True:
        timer += 1 #Timer for counting turns
        
        #Variables for left wall, right wall, orange line, green pillar, and red pillar area
        leftarea = 0
        leftcontourindex = 0
        rightarea = 0
        rightcontourindex = 0
        
        orangearea = 0
        orangecontourindex=0
        
        green_area = 0
        green_counter_index = 0
        
        red_area = 0
        red_counter_index = 0
        
        im = picam2.capture_array() #Capturing camera image as an array
        
        subim=im[280:345,0:200] #Setting left wall detection area
        subim2=im[280:345,440:640] #Setting right wall detection area
        subim3=im[425:465,180:480] #Setting orange line detection area
        pillar_subim = im[218:420,70:590]
    
        left_points = [(0,280), (200,280), (200,345), (0,345)] #Displaying left wall subimage rectangle (for troubleshooting)
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, left_points[0], left_points[1], color, thickness)
        image = cv2.line(im, left_points[1], left_points[2], color, thickness)
        image = cv2.line(im, left_points[2], left_points[3], color, thickness)
        image = cv2.line(im, left_points[3], left_points[0], color, thickness)
    
        right_points = [(440,280), (640,280), (640,345), (440,345)] #Displaying right wall subimage rectangle (for troubleshooting)
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, right_points[0], right_points[1], color, thickness)
        image = cv2.line(im, right_points[1], right_points[2], color, thickness)
        image = cv2.line(im, right_points[2], right_points[3], color, thickness)
        image = cv2.line(im, right_points[3], right_points[0], color, thickness)
        
        floor_points = [(180,425), (480,425), (480,465), (180,465)] #Displaying floor subimage rectangle (for troubleshooting)
        color = (255, 0, 0)
        thickness = 4
        image = cv2.line(im, floor_points[0], floor_points[1], color, thickness)
        image = cv2.line(im, floor_points[1], floor_points[2], color, thickness)
        image = cv2.line(im, floor_points[2], floor_points[3], color, thickness)
        image = cv2.line(im, floor_points[3], floor_points[0], color, thickness)
        
        pillar_points = [(70, 218), (590, 218), (590, 420), (70, 420)] #Displaying pillar subimage rectangle (for troubleshooting)
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, pillar_points[0], pillar_points[1], color, thickness)
        image = cv2.line(im, pillar_points[1], pillar_points[2], color, thickness)
        image = cv2.line(im, pillar_points[2], pillar_points[3], color, thickness)
        image = cv2.line(im, pillar_points[3], pillar_points[0], color, thickness)
        
        imgGray = cv2.cvtColor(subim, cv2.COLOR_BGR2GRAY) #Grayscaling for thresholding 
        ret, imgThresh = cv2.threshold(imgGray, 45, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(contours)): #finding largest contour
            cnt = contours[i]
            if cv2.contourArea(cnt) > leftarea:
                leftarea = cv2.contourArea(cnt)
                leftcontourindex = i
        if(leftarea > 0): 
            cv2.drawContours(subim, contours, i, (0, 255, 0), 2) #drawing left largest contour
            displayLeftArea = str(int(leftarea))
#             cv2.putText(im, displayLeftArea, (7, 250), font, 1, (100, 255, 0), 3, cv2.LINE_AA)
    
        #Right Wall
        imgGray2 = cv2.cvtColor(subim2, cv2.COLOR_BGR2GRAY) #Grayscaling preperation
        ret2, imgThresh2 = cv2.threshold(imgGray2, 45, 255, cv2.THRESH_BINARY_INV)
        contours2, hierarchy2 = cv2.findContours(imgThresh2,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(contours2)):
            cnt2 = contours2[i]
            if cv2.contourArea(cnt2) > rightarea:
                rightarea = cv2.contourArea(cnt2)
                rightcontourindex = i 
        if(rightarea > 0):
            cv2.drawContours(subim2, contours2, i, (0, 255, 0), 2) #drawing largest right contour
            displayRightArea = str(int(rightarea))
#             cv2.putText(im, displayRightArea, (550, 250), font, 1, (100, 255, 0), 3, cv2.LINE_AA)
        
        #Orange Line
        line_hsv = cv2.cvtColor(subim3, cv2.COLOR_BGR2HSV) #Converting floor subimage to HSV

        lower_orange = np.array([0, 111, 152]) #Lower threshold for orange colour
        upper_orange = np.array([56, 255, 255]) #Upper threshold for orange colour 
        orange_mask = cv2.inRange(line_hsv, lower_orange, upper_orange) #Orange mask
        
        orangeContours = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        for i in range(len(orangeContours)): #finding largest orange contour
            cnt3 = orangeContours[i]
            if cv2.contourArea(cnt3) > orangearea:
                orangearea = cv2.contourArea(cnt3)
                orangecontourindex = i
         
        cv2.drawContours(subim3, orangeContours, i, (0, 255, 0), 2) #drawing largest orange contour
        displayOrangeArea = str(int(orangearea))
#         cv2.putText(im, displayOrangeArea, (260, 320), font, 2, (100, 255, 0), 3, cv2.LINE_AA) #Displaying orange line area on screen
        
        #Pillar Contours
        pillar_hsv = cv2.cvtColor(pillar_subim, cv2.COLOR_BGR2HSV) #Converting pillar subimage to HSV
        
        #Red
        lower_red = np.array([160, 181, 100]) #Lower threshold for red colour
        upper_red = np.array([180, 255, 255]) #Upper threshold for red colour 
        red_mask = cv2.inRange(pillar_hsv, lower_red, upper_red) #Red mask
        
        redContours = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        for i in range(len(redContours)): #finding largest red contour
            cnt4 = redContours[i]
            if cv2.contourArea(cnt4) > red_area:
                red_area = cv2.contourArea(cnt4)
                red_contour_index = i
                
        if(red_area > 50):
            cv2.drawContours(pillar_subim, redContours, i, (0, 255, 0), 2) #drawing red largest contour
            approx=cv2.approxPolyDP(cnt4, 0.01*cv2.arcLength(cnt4,True),True)
            x,y,w,h=cv2.boundingRect(approx) #Approximating rectangle around pillar contours
            cv2.rectangle(pillar_subim,(x,y),(x+w,y+h),(235, 206, 135),2) #Drawing approximated rectangle around pillar contours
            
            red_x = x #x coordinate for red pillars
        
        #Green
        lower_green = np.array([66, 92, 68]) #Lower threshold for green colour
        upper_green = np.array([86, 255, 255]) #Upper threshold for green colour 
        green_mask = cv2.inRange(pillar_hsv, lower_green, upper_green) #Green mask
        
        lower_green = np.array([54, 92, 68]) #Lower threshold for green colour
        upper_green = np.array([86, 255, 255]) #Upper threshold for green colour 
        green_mask2 = cv2.inRange(pillar_hsv, lower_green, upper_green) #Second Green mask
        
        full_green_mask = green_mask | green_mask2 #Combining green masks
        
        greenContours = cv2.findContours(full_green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        for i in range(len(greenContours)): #finding largest green contour
            cnt5 = greenContours[i]
            if cv2.contourArea(cnt5) > green_area:
                green_area = cv2.contourArea(cnt5)
                green_contour_index = i
                
        if(green_area > 50):
            cv2.drawContours(pillar_subim, greenContours, i, (0, 255, 0), 2) #drawing green largest contour
            approx2=cv2.approxPolyDP(cnt5, 0.01*cv2.arcLength(cnt5,True),True)
            x2,y2,w2,h2=cv2.boundingRect(approx2) #Approximating rectangle around pillar contours
            cv2.rectangle(pillar_subim,(x2,y2),(x2+w2,y2+h2),(255, 0, 0),2) #Drawing approximated rectangle around pillar contours
            
            green_x = x2 #x coordinate for green pillars
        
        #Displaying information for troubleshooting
        print("Red X:", red_x)
        print("Green X:", green_x)
        print("TURN COUNT:", count)
        print("Turning?:", turning)
        print("Turn Direction:", turnDirection)
        print("turn counts:", turn_around_count)
        print("Green Area:", green_area)
        print("Red Area:", red_area)
        print("Last Pillar?:", last_pillar)
        print("difference is:", difference)
        print("Steering angle is:", angle)
        
        displayTurnCount = str(int(count))
        cv2.putText(im, displayTurnCount, (560, 60), font, 2, (100, 255, 0), 3, cv2.LINE_AA) #Displaying turn count on screen
        cv2.putText(im, displayTurning, (7, 60), font, 2, (100, 255, 0), 3, cv2.LINE_AA) #Displaying vehicle status on screen
        
        if orangearea > 700: #Orange line is seen
            orange_seen = True
            timer = 0
            
        if orange_seen == True and (timer//30 > 0.5): #Timer to ensure line is not counted more than once
            count+=1
            turn_around_count +=1
            orange_seen = False
            timer = 0
                
        if green_area > 700:
            if green_area > red_area: #Ensuring that the front-most pillar is detected only
                green_pillar_seen = True
                PD = False #Deactivating PD Controller
                last_pillar = 'green'
        else:
            green_pillar_seen = False
            PD = True
            
        if red_area > 700:
            if red_area > green_area: #Ensuring that the front-most pillar is detected only
                red_pillar_seen = True
                PD = False #Deactivating PD Controller
                last_pillar = 'red'
        else:
            red_pillar_seen = False
            PD = True
            
        if green_pillar_seen == True:
            #Green Pillar Maneuvering
            PD = False
            print("Green Pillar Maneuvering")
            displayTurning = 'Green Pillar'
            difference = -(green_x - 540) #540 is target x position for green pillars
            correction = 2 * difference + 0.001 * (difference - lastdifference)
            angle = 85.045 + correction
            
            if angle > 120: #Ensures that servo stays within safe limits for turning left
                angle = 120
            elif angle < 40: #Ensures that servo stays within safe limits for turning right
                angle = 40
            
            pw = int(11.1 * angle + 500)
            Board.setPWMServoPulse(1, pw, 1)
            lastdifference = difference
    
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0)) #Shows Green LED when detecting green pillar
            Board.RGB.show()
            
        if red_pillar_seen == True:
            #Red Pillar Maneuvering
            PD = False
            print("Red Pillar Maneuvering")
            displayTurning = 'Red Pillar'
            difference = -abs(int(red_x - 120)) #120 is target x position for red pillars
            correction = 2 * difference + 0.001 * (difference - lastdifference)
            angle = 85.045 + correction
            
            if angle > 120: #Ensures that servo stays within safe limits for turning left
                angle = 120
            elif angle < 40: #Ensures that servo stays within safe limits for turning right
                angle = 40
            
            pw = int(11.1 * angle + 500)
            Board.setPWMServoPulse(1, pw, 1)
            lastdifference = difference
            
            Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0)) #Shows Red LED when detecting green pillar
            Board.RGB.show()
            
        if not turning and green_pillar_seen == False and red_pillar_seen == False: 
            if leftarea < 100: #Sharp turn left
                turning = True
                turnDirection = 'left'
                print("TURNING LEFT")
                        
            elif rightarea < 100: #Sharp turn right
                turning = True
                turnDirection = 'right'
                print("TURNING RIGHT")

        if turnDirection == 'left' and turning == True: #Turning Left
            Board.setPWMServoPulse(1,1832, 1)
            PD = False
            displayTurning = 'Turning Left'
            
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0)) #Turns off LED for turning
            Board.RGB.show()
                
        elif turnDirection == 'right' and turning == True: #Turning right
            Board.setPWMServoPulse(1,955, 1)
            PD = False
            displayTurning = 'Turning Right'
            
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0)) #Turns off LED for turning
            Board.RGB.show()
        
        if turning == True and leftarea > 250 and rightarea > 250: #Detects both walls again after turn is complete
            turning = False
            turnDirection = None
            PD = True
            lastdifference = 0
        
        if not turning and turnDirection == None and PD == True:
            #PD CONTROLLER 
            print("PD ACTIVATED")
            displayTurning = 'PD Controller'
            difference = rightarea - leftarea
            correction = 0.5 * difference + 0.001 * (difference - lastdifference)
            angle = 85.045 + correction
            
            if angle > 120: #Ensures that servo stays within safe limits for turning left
                angle = 120
            elif angle < 40: #Ensures that servo stays within safe limits for turning right
                angle = 40
            
            pw = int(11.1 * angle + 500)
            Board.setPWMServoPulse(1, pw, 1)
            lastdifference = difference
            
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255)) #Shows Blue LED when PD Control is active
            Board.RGB.show()
        
        if last_pillar == 'red' and turn_around_count == 1 and red_area > 300: #Reverse direction
            turn_around = True
            
        if turn_around == True:
            turn_around_frames += 1
            
            if turn_around_frames > 125 and turn_around == True: #Ensures turn is at correct spot
                #Three Point Turn
                Board.setPWMServoPulse(5,1322,10)
                time.sleep(1)
                Board.setPWMServoPulse(1, 1830, 1)
                time.sleep(1)
                Board.setPWMServoPulse(1, 944, 1)
                time.sleep(0.5)
                Board.setPWMServoPulse(5,1595,1)
                time.sleep(2)
                Board.setPWMServoPulse(5,1500,1)
                time.sleep(0.1)
                Board.setPWMServoPulse(1, 1832, 1)
                time.sleep(1)
                Board.setPWMServoPulse(5,1325,1)
                time.sleep(0.8)
                
                turn_around_count +=1
                turn_around = False
                turn_around_frames = 0
                Board.setPWMServoPulse(5,1323,1)
                
                
        if count>=12: #all turns have been completed
            endFrames+=1
            
            if endFrames > 65: #counting frames to ensure robot ends in correct place
                Board.setPWMServoPulse(5,1500,100) #Stopping the motor
                Board.setPWMServoPulse(1,1500,100) #Straightening wheels
                
                Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
                Board.RGB.show()
            
                break #exiting loop 
        
        if len(sys.argv) > 1 and sys.argv[1] == 'Debug': #Debug mode for troubleshooting
            cv2.imshow('contours2', im)
        
            if cv2.waitKey(1)==ord('q'):
                Board.setPWMServoPulse(5,1500,100)
                Board.setPWMServoPulse(1,1444,100)
                cv2.destroyAllWindows()
                break
        
cv2.destroyAllWindows()