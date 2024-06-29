import sys
sys.path.append('/home/pi/TurboPi/')
import time
import HiwonderSDK.Board as Board
import cv2
from picamera2 import Picamera2

Board.setPWMServoPulse(5, 1500, 100) #Arm ESC
Board.setPWMServoPulse(1, 1500, 10) #Set Servo to 90
time.sleep(6)
leftTurns=0
rightTurns=0
clockwise=False
counterClockwise=False
turning=False

#Camera setup
picam2=Picamera2()
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format='RGB888'
picam2.preview_configuration.align()
picam2.preview_configuration.controls.FrameRate=30
picam2.configure("preview")
picam2.start()
if __name__ == '__main__':
    angle = 90
    pw_Servo = angle * 11.1 + 500
    Board.setPWMServoPulse(5,1320,100) #Speed
    while True:
        im = picam2.capture_array()
        #subim=im[265:325,0:200] #Left Wall
        #subim2=im[265:325,440:640] #Right wall
        
        subim=im[280:345,0:200]
        subim2=im[280:345,440:640]
    
        #points = [(0,265), (200,265), (200,325), (0,325)]
        points = [(0,280), (200,280), (200,345), (0,345)]
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, points[0], points[1], color, thickness)
        image = cv2.line(im, points[1], points[2], color, thickness)
        image = cv2.line(im, points[2], points[3], color, thickness)
        image = cv2.line(im, points[3], points[0], color, thickness)
    
        #points = [(440,265), (640,265), (640,325), (440,325)]
        points = [(440,280), (640,280), (640,345), (440,345)]
        color = (0, 255, 255)
        thickness = 4
        image = cv2.line(im, points[0], points[1], color, thickness)
        image = cv2.line(im, points[1], points[2], color, thickness)
        image = cv2.line(im, points[2], points[3], color, thickness)
        image = cv2.line(im, points[3], points[0], color, thickness)
    
        imgGray = cv2.cvtColor(subim, cv2.COLOR_BGR2GRAY)
        ret, imgThresh = cv2.threshold(imgGray, 60, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        leftarea=0
        leftcontourindex=0
        for i in range(len(contours)): #finding largest contour
            cnt = contours[i]
            leftarea = cv2.contourArea(cnt)
            if cv2.contourArea(cnt) > leftarea:
                leftarea = cv2.contourArea(cnt)
                leftcontourindex = i
        if(leftarea > 0): 
            print('Left wall: ',leftarea) #Displaying left contour area
            cv2.drawContours(subim, contours, i, (0, 255, 0), 2) #drawing left largest contour
        #cv2.imshow("contours", im)
    
        #Right Wall
        imgGray2 = cv2.cvtColor(subim2, cv2.COLOR_BGR2GRAY)
        ret2, imgThresh2 = cv2.threshold(imgGray2, 60, 255, cv2.THRESH_BINARY_INV)
        contours2, hierarchy2 = cv2.findContours(imgThresh2,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rightarea=0
        rightcontourindex = 0
        for i in range(len(contours2)):
            cnt2 = contours2[i]
            rightarea = cv2.contourArea(cnt2)
            if cv2.contourArea(cnt2) > rightarea:
                rightarea = cv2.contourArea(cnt2)
                rightcontourindex = i 
        if(rightarea > 0):
            print('Right Wall: ',rightarea) #displaying right contour area
            cv2.drawContours(subim2, contours2, i, (0, 255, 0), 2) #drawing largest right contour
        cv2.imshow("contours2", im)
        
        
        if leftarea < 100:
            counterClockwise=True
            clockwise=False
            
        if rightarea < 100:
            clockwise=True
            counterClockwise=False
            
        if counterClockwise = True:
            
        
        #Steering
        if (leftarea >= rightarea): #Left wall is bigger
            rightTurnStart=time.time()
            difference = leftarea-rightarea
            lastdifference = 0
            t=time.time()
            print('angle is:',angle)
            if angle>=38:
                rightTurns+=1
            print("right Turns:",rightTurns)
#             print('rightturn start:', rightTurnStart)
#             elapsed=t-rightTurnStart
#             print(elapsed)
#             if elapsed>=2:
#                 elapsed-=elapsed
#                 print('new:',elapsed)

                
                
                
            
            #Turning Right
            if angle >= 40 and (0<=difference<=500):
                steeringRightAngle = 0*difference
                angle -=(steeringRightAngle)
                pw = 11.1 * angle + 500
                pw = int(pw)
                Board.setPWMServoPulse(1, pw, 1)
                print('1')
                lastdifference = difference
            elif angle >=40 and difference>500:
                steeringRightAngle = 0.002*difference+0.000*(difference-lastdifference)
                angle -=(steeringRightAngle)
                pw = 11.1 * angle + 500
                pw = int(pw)
                Board.setPWMServoPulse(1, pw, 1)
                print('steering right angle:', steeringRightAngle)
                lastdifference = difference
#             if (angle >= 40):
#                 angle -= 1
#                 pw = 11.1 * angle + 500
#                 pw = int(pw)
#                 Board.setPWMServoPulse(1, pw, 1)
#                 time.sleep(0.1)
            
        elif (rightarea >= leftarea): #Right wall is bigger
            difference = rightarea-leftarea
            lastdifference = 0
            leftTurnStart=time.time()
            print("left Turns:",leftTurns)
            
            if leftTurnStart - time.time() >= 2:
                leftTurns += 1
                leftTurnStart=None
                print(5)
            
            #Turning Left
            if (angle <= 120) and (0<=difference<=500):
                steeringRightAngle = 0*difference
                angle -=(steeringRightAngle)
                pw = 11.1 * angle + 500
                pw = int(pw)
                Board.setPWMServoPulse(1, pw, 1)
                print('1')
                lastdifference = difference
            elif angle <=120 and difference>500:
                steeringLeftAngle = 0.002*difference+0.000*(difference-lastdifference)
                angle +=(steeringLeftAngle)
                pw = 11.1 * angle + 500
                pw = int(pw)
                Board.setPWMServoPulse(1, pw, 1)
                print('steering left angle:', steeringLeftAngle)
                lastdifference = difference
#                 angle += 1
#                 pw = 11.1 * angle + 500
#                 pw = int(pw)
#                 Board.setPWMServoPulse(1, pw, 1)
#                 time.sleep(0.1)
            
        if cv2.waitKey(1)==ord('q'): #wait until 'q' is pressed
            Board.setPWMServoPulse(5,1500,100)
            Board.setPWMServoPulse(1,1500,100)
            break
        
cv2.destroyAllWindows()


        