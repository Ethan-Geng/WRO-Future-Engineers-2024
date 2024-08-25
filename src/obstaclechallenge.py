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

frames=0
count=0
endFrames = 0

turning = False
turnDirection = None

difference = 0
lastdifference = 0

displayLeftArea = 0
displayRightArea = 0
displayOrangeArea = 0
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
    Board.setPWMServoPulse(5,1322,100) #Speed
    while True:
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
        
        im = picam2.capture_array()
        
        subim=im[280:345,0:200] #Setting left wall detection area
        subim2=im[280:345,440:640] #Setting right wall detection area
        subim3=im[365:410,180:480] #Setting orange line detection area
        pillar_subim = im[218:420, 130:515]
    
        left_points = [(0,280), (200,280), (200,345), (0,345)]
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, left_points[0], left_points[1], color, thickness)
        image = cv2.line(im, left_points[1], left_points[2], color, thickness)
        image = cv2.line(im, left_points[2], left_points[3], color, thickness)
        image = cv2.line(im, left_points[3], left_points[0], color, thickness)
    
        right_points = [(440,280), (640,280), (640,345), (440,345)]
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, right_points[0], right_points[1], color, thickness)
        image = cv2.line(im, right_points[1], right_points[2], color, thickness)
        image = cv2.line(im, right_points[2], right_points[3], color, thickness)
        image = cv2.line(im, right_points[3], right_points[0], color, thickness)
        
        floor_points = [(150,365), (500,365), (500,410), (150,410)]
        color = (0, 0, 255)
        thickness = 4
        image = cv2.line(im, floor_points[0], floor_points[1], color, thickness)
        image = cv2.line(im, floor_points[1], floor_points[2], color, thickness)
        image = cv2.line(im, floor_points[2], floor_points[3], color, thickness)
        image = cv2.line(im, floor_points[3], floor_points[0], color, thickness)
        
        pillar_points = [(130, 218), (515, 218), (515, 420), (130, 420)]
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
#             print('Left wall: ',leftarea) #Displaying left contour area
            cv2.drawContours(subim, contours, i, (0, 255, 0), 2) #drawing left largest contour
            displayLeftArea = str(int(leftarea))
            cv2.putText(im, displayLeftArea, (7, 250), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
    
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
#             print('Right Wall: ',rightarea) #displaying right contour area
            cv2.drawContours(subim2, contours2, i, (0, 255, 0), 2) #drawing largest right contour
            displayRightArea = str(int(rightarea))
            cv2.putText(im, displayRightArea, (450, 250), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
#         cv2.imshow("contours2", im)
        
        #Orange Line
        line_hsv = cv2.cvtColor(subim3, cv2.COLOR_BGR2HSV)

        lower_orange = np.array([0, 111, 152]) #Lower threshold for orange colour
        upper_orange = np.array([56, 255, 255]) #Upper threshold for orange colour 
        orange_mask = cv2.inRange(line_hsv, lower_orange, upper_orange) #Orange mask
        
        orangeContours = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        for i in range(len(orangeContours)): #finding largest orange contour
            cnt3 = orangeContours[i]
            if cv2.contourArea(cnt3) > orangearea:
                orangearea = cv2.contourArea(cnt3)
                orangecontourindex = i
         
        cv2.drawContours(subim3, orangeContours, i, (0, 255, 0), 2) #drawing orange largest contour
        displayOrangeArea = str(int(orangearea))
#         cv2.putText(im, displayOrangeArea, (300, 300), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
        
#         print("Orange Area:", orangearea)
        
        #Pillar Contours
        pillar_hsv = cv2.cvtColor(subim3, cv2.COLOR_BGR2HSV)
        
        #Red
        lower_red = np.array([160, 156, 79]) #Lower threshold for red colour
        upper_red = np.array([180, 255, 255]) #Upper threshold for red colour 
        red_mask = cv2.inRange(pillar_hsv, lower_red, upper_red) #Red mask
        
        redContours = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        for i in range(len(redContours)): #finding largest red contour
            cnt4 = redContours[i]
            if cv2.contourArea(cnt4) > red_area:
                red_area = cv2.contourArea(cnt4)
                red_contour_index = i
                
        if(red_area > 0):
            cv2.drawContours(pillar_subim, redContours, i, (0, 255, 0), 2) #drawing red largest contour
            approx=cv2.approxPolyDP(cnt4, 0.01*cv2.arcLength(cnt4,True),True)
            x,y,w,h=cv2.boundingRect(approx)
            cv2.rectangle(pillar_subim,(x,y),(x+w,y+h),(235, 206, 135),2)
            
            red_y = y
            red_x = x
            
            print("Red Y:", red_y)
            print("Red X:", red_x)
            print("Red Area:", red_area)
        
        #Green
        lower_green = np.array([43, 111, 64]) #Lower threshold for green colour
        upper_green = np.array([111, 255, 255]) #Upper threshold for green colour 
        green_mask = cv2.inRange(pillar_hsv, lower_green, upper_green) #Green mask
        
        greenContours = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        for i in range(len(greenContours)): #finding largest green contour
            cnt5 = greenContours[i]
            if cv2.contourArea(cnt5) > green_area:
                green_area = cv2.contourArea(cnt5)
                green_contour_index = i
                
        if(green_area > 0):
            cv2.drawContours(pillar_subim, greenContours, i, (0, 255, 0), 2) #drawing green largest contour
            approx2=cv2.approxPolyDP(cnt5, 0.01*cv2.arcLength(cnt5,True),True)
            x2,y2,w2,h2=cv2.boundingRect(approx2)
            cv2.rectangle(pillar_subim,(x2,y2),(x2+w2,y2+h2),(235, 206, 135),2)
            
            green_y = y2
            green_x = x2
        
            print("Green Y:", green_y)
            print("Green X:", green_x)
            print("Green Area:", green_area)
        
#         print("TURN COUNT:", count)
#         print("Turning?:", turning)
#         print("Turn Direction:", turnDirection)
        
        displayTurnCount = str(int(count))
        cv2.putText(im, displayTurnCount, (560, 60), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(im, displayTurning, (7, 60), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
        
        if orangearea > 700:
            frames += 1
            if frames>45:
                count+=1
                frames=0
        
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
#             if frames>35:
#                 count+=1
#                 frames=0
                
        elif turnDirection == 'right' and turning == True:
            Board.setPWMServoPulse(1,955, 1)
            frames += 1
            print("frames:",frames)
            displayTurning = 'Turning Right'
#             if frames>35:
#                 count+=1
#                 frames=0
        
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