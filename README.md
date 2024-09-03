Documentation l Explorer Robotics l Team French Fries
====
## Introduction
This repository contains the engineering process of Team French Fries' self-driven vehicle's model participating in the WRO Future Engineers competition in the season 2024. Included in the repository are materials used, schematics, pictures, and software.

## Team Members
* Ethan Geng (EMAIL: ethan.geng7@gmail.com)
* Alexandra Chao-Lau (EMAIL: alexandra.clau3@gmail.com)
* Kenneth Mac (EMAIL: kennethmacrobotics@gmail.com)

## Content

* `t-photos` contains 2 photos of the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains one or several schematic diagrams in form of JPEG, PNG or PDF of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `src` contains code of control software for all components which were programmed to participate in the competition
* `models` is for the files for models used by 3D printers, laser cutting machines and CNC machines to produce the vehicle elements. If there is nothing to add to this location, the directory can be removed.
* `other` is for other files which can be used to understand how to prepare the vehicle for the competition. It may include documentation how to connect to a SBC/SBM and upload files there, datasets, hardware specifications, communication protocols descriptions etc. If there is nothing to add to this location, the directory can be removed.

## Parts List & Design Choice

| Part  | Description  | Photo  |
|:----------|:----------|:----------|
| __Carisma Puma Hybrid Rally RC Car 1/24 AWD ([Link](https://carisma-shop.com/products/gt24-m-sport-2022-puma-hybrid-rally1))__    | Equipped with a lightweight chassis, high traction tires, and effective friction dampeners, this RC car serves as a perfect base for our team to construct our self-driving car using. With the addition of the parking lot in this year's competition, we chose this 1/24th scale size as its dimensions allow us to effectively utilize back-in parking, as opposed to parallel parking. This not only saves time, but minimizes chances of error during our parking phase of Obstacle Challenge.     | ![Rally Car Chassis](https://carisma-shop.com/cdn/shop/products/87868_12.jpg?v=1673246397)    |
| __Raspberry Pi 4 Model B ([Link](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/))__    | We chose the Raspberry Pi to act as the brain of the entire car. The code on the board handles all computing aspects, including the image processing and control signals. It's 64-bit quad-core processor coupled with 8GB of Random Access Memory (RAM) ensures fast processing of our code.     | ![Raspberry Pi 4 Model B](https://cdn.robotshop.com/media/r/ras/rb-ras-26/img/raspberry-pi-4-b-4g-computer-board-desc1.webp)    |
| __Hiwonder Pi Expansion Board (N/A)__    | Compact and practical, the expansion board stacks on top of our Raspberry Pi board and is attached using the board's universal input/output pins. This expansion board allows for easy connections for our servo motor, brushless motor, and Pi fan.    | N/A    |
| __SainSmart MIPI CSI Fisheye Camera Module ([Link](https://www.sainsmart.com/products/noir-wide-angle-fov160-5-megapixel-camera-module))__    | This CSI camera conveniently connects to our Raspberry Pi board's camera module port and offers a wide 160 degree viewing angle with great 5MP resolution, colour quality, and a high frame rate. This camera is responsible for detecting walls, obstacles, and lines.    | ![MIPI Camera](https://www.sainsmart.com/cdn/shop/products/2_78_2_1024x1024.jpg?v=1499267387)    |
| __Micro Servo Motor ([Link](https://ca.robotshop.com/products/hs-5055mg-metal-gear-micro-servo-motor?srsltid=AfmBOopv8Z7LoCVOEqe16w05ZV-R78dNmy7dappldIxZiQzCJroxcssFc2Y))__    | This programmable micro servo motor allows our team to precisely control the steering angle of our car. It's compact and lightweight design ensures that it can fit perfectly within our car chassis.    | ![Servo Motor](https://ca.robotshop.com/cdn/shop/files/hs-5055mg-metal-gear-micro-servo-motor-1.webp?v=1720506823&width=500)    |
| __GeeekPi Pi Fan ([Link](https://www.amazon.ca/GeeekPi-Raspberry-Radiator-Aluminum-Heatsinks/dp/B07C9C99RM/ref=asc_df_B07C9C99RM/?tag=googleshopc0c-20&linkCode=df0&hvadid=579070369590&hvpos=&hvnetw=g&hvrand=2167868380151199729&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9000759&hvtargid=pla-995264935599&psc=1&mcid=ad78a1c125c23c7088cb21e5dde53480))__    | We decided to include this efficient fan to effectively cool and dissipate heat from our Raspberry Pi, which will help to mitigate thermal throttling and thereby improve performance under a heavy processing load. Our team found that the addition of this Pi fan can cool the Raspberry Pi up to 30 degrees celsius.    | ![Pi Fan](https://cdn.hepsiglobal.com/prod/media/5380/20230111/c4e31f24-b0c2-4e9c-9e52-d1a2d049156f.jpg)    |
| __Furitek Komodo Micro Brushless Motor + ESC ([Link](https://furitek.com/products/furitek-stinger-brushless-power-system-for-scx24))__    | The Furitek brushless motor works with the spur gear in our car chassis to drive the wheels. It has a lightweight but powerful design that provides smooth driving with great speed, high torque, and zero cogging. We chose to use a brushless motor because of the increased efficiency due to the eliminaton of brushes which create friction, greater reliablilty, and overall improved performance compared to a brushed motor.    | ![Motor and ESC](https://www.bigboyswithcooltoys.ca/cdn/shop/files/FRU2102_A0_7UY8Y8Z9_x700.jpg?v=1705165760)    |
| __Gens ACE 1300mAh LiPo Battery ([Link](https://www.adrenalinehobby.com/products/gens-ace-g-tech-1300mah-2s-7-4v-25c-lipo-deans-plug?_pos=1&_sid=dde29d30b&_ss=r))__    | This LiPo batery provides power for the entire circuit/car system, including the servo motor, Raspberry Pi, and brushless motor. It's high 1300mAh capacity allows our car and program to run for an extended period of time, which helps during testing and improves reliability during competition.    | ![LiPo Battery](https://m.media-amazon.com/images/I/61uJIdaLJUL._AC_UF894,1000_QL80_.jpg)    |


## Hardware Assembly and Design Process
1. Our first step in our build process was to open up and strip down the __Carisma Puma Hybrid Rally RC Car 1/24 AWD__ to its chassis and remove all the components we did not need. This included taking out the built-in servo motor, the brushed motor, the battery connection, and remote control circuit board. 
2. Now with a base chassis, we were able to install our own components including the __Micro Servo Motor__ and __Furitek Komodo Micro Brushless Motor + ESC__. Replacing the RC car's original servo motor and brushed motor was a key step in our process as it allowed us to use programmable and higher quality components. We made physical modifications to the chassis by cutting the plastic body using an exacto knife to ensure that our new components would fit seamlessly.
3. With our components installed, our team moved onto creating our main platform for the car on which the __Raspberry Pi 4 Model B__, __Hiwonder Pi Expansion Board__, and __GeeekPi Pi Fan__ will sit on, as well as a tower that will house the __SainSmart MIPI CSI Fisheye Camera Module__. After brainstorming methods to create the platform and tower, we ultimately decided upon 3D printing it using PETG filament, thus ensuring a lightweight and durable product.
   * The main platform is a flat rectangle with a raised border on 2 sides and 4 mounting holes near each corner. It sits on top of our car chassis and is secured by fitting the mounting holes onto rods that stick up vertically on the car's chassis. The __Raspberry Pi 4 Model B__ is attached to the platform using the board's mounting holes and 4 small cylinders on the platform. On the left side of the platform, there is a rectangular box which the __GeeekPi Pi Fan__ can snap into.
   * The camera tower sits on the back of the platform and is secured through screws on the bottom of the platform. We then screwed in the __SainSmart MIPI CSI Fisheye Camera Module__ to the tower, which guarantees a tight fit. Additionally, we added velcro to the back of the camera tower to house our __Gens ACE 1300mAh LiPo Battery__.
4. Our final step was to connect all the wiring from the components to the Raspberry Pi and __Gens ACE 1300mAh LiPo Battery__, as well as wire management using electrical tape, 3M Command Strips, and Velcro to make certain that no loose wiring would cause problems for our car.

## Code Overview
Both the code for Open Challenge and Obstacle Challenge follow similar sequential program logic, with the key differences being in their main loop. The general program structure for these two challenges is as follows:

1. Initializing Variables
   * Initializes variables responsible for turning, image processing, troubleshooting, turn/lap counting, and contour detection 
2. Servo/Motor Setup
   * Straightening car tires and preparing motor
3. Camera Setup
   * Setting camera resolution and framerate for capturing image
4. Push Button Start
   * Waits until a push button is pressed before starting the main loop (uses a white LED as a ready indicator)
5. Main Loop (See below sections)

To program our self-driving car's "vision" and camera operations, our team utilized OpenCV. Other libraries we used include: Time for programming delays; PiCamera2 for controlling our camera; RPi.GPIO for push button start; numpy for image processing; and HiwonderSDK for operating our Raspberry Pi Hat. 

## Open Challenge Main Loop Overview 
The main loop for Open Challenge can be broken down into 4 main sections:

* __Image Processing & Contour Detection__
   * First, the camera captures the left wall, right wall, and floor Region of Interest (ROI) subimages as arrays. For the left and right wall ROI, various image processes including grayscaling and thresholding are conducted to prepare for contour detection, a computer vision technique which detects the edges/boundaries of an object. Similarily, the floor ROI is prepared for contour detection through a BGR (Blue, Green, Red) to HSV (Hue, Saturation, Value) colour conversion, colour thresholds, and a colour mask. Following these processes, the right wall, left wall, and orange line contours are found, as well as their areas'. This information is instrumental in the following processes of the program.

* __Wall Following__
   * Our vehicle uses a Proportional-Derivative (PD) Controller, a simplified version of the common Proportional-Integral-Derivative (PID) controller. The proportional term of the controller produces outputs based on the current error between the system's desired position (the exact middle of the two walls) and its actual position. In our case, the error is calculated to be the difference in area between the left and right wall. If the difference in area is large (e.g the vehicle is next to the right wall), the controller will produce a strong output (e.g. turning sharply left). The derivative term of the controller measures the rate of change of the error to "predict the future". Using this information, it can "dampen" the system's response to reduce oscillations and overshoots. In our case, the derivative is calculated as the difference between the current error and the previous error.

* __Vehicle Turning and Lap Counting__
   * To turn, our vehicle uses the areas of the left and right wall. If it detects that the area of the right wall suddenly drops below a certain threshold, it will disable its PD controller and conduct a sharp right turn. Similarily, if the left wall's area drops below the threshold, it will turn sharply left. The turn will continue until the vehicle detects that both walls are again above a certain threshold. As a preventative measure, our program uses a "turn buffer" that ensures that the turn lasts for at least 7 frames before ending. This prevents unwanted disruptions to the turn. To count its turns, the vehicle uses the floor ROI to detect the orange line. If the vehicle detects the orange line, it will add to its turn counts. 

* __Program Termination__
   * Once the vehicle detects that 12 turns, and therefore 3 laps, have been completed, it will continue for 85 frames/almost 3 seconds (to ensure it stops in the correct area) before stopping and exiting the main loop.

## Obstacle Challenge Main Loop Overview
The main loop for Obstacle Challenge can be broken down into 6 main sections:

* __Image Processing & Contour Detection__
   * Similar to open challenge, the camera captures the left wall, right wall, and floor Region of Interest (ROI) subimages as arrays and conducts contour detection on them. With obstacle challenge, there is an additional pillar region of interest. In this subimage, red and green pillars are detected through contour detection after performing a HSV colour conversion and using colour masks. Additionally, we used an OpenCV2 function called boundingRect() to approximate a rectangle around the pillars. This gives us the x position of the pillar.

* __Pillar Maneuvering__
   * Once we have the x position of the upcoming pillar, we applied a PD controller to navigate the vehicle to either the right side of a red pillar or the left side of a green pillar. To do so, we set a target x position for the pillars. For red pillars, our target x position is on the left side of the screen, as we want our vehicle to pass it on the right side. The opposite works for green pillars. We calculated the error in our PD controller to be the difference between the pillar's actual x position and our target x position. 

* __Wall Following__
   * If our vehicle does not detect any pillars and is not in a turn, it will use the same wall following logic as Open Challenge to navigate the course. 

* __Vehicle Turning and Lap Counting__
   * To turn, our vehicle also uses the same logic as Open Challenge, with the exception of the removal of our turn buffer. Since there may be a pillar directly after the turn, it is disadvantageous for our vehicle to continue its turn for a set amount of time, as it may need to quickly adjust its path to avoid a pillar. Furthermore, we continue to use the orange line to detect turns for Obstacle Challenge. 

* __Three Point Turn__
   * If our vehicle detects the last pillar to be red after 2 laps, it will disengage its wall following, pillar detection, turn detection, and camera to follow a set procedure for a three point turn. After it has successfully reversed its direction, its processes will start again. 

* __Program Termination__
   * Once the vehicle detects that 12 turns, and therefore 3 laps, have been completed, it will continue for a set amount of frames before stopping and exiting the main loop.

## Building/Compiling/Uploading Process
All code for open challenge and obstacle challenge was built using Python. Our programs are coded and saved directly onto our Raspberry Pi. To do so, we used an application called Real VNC to remotely access our Raspberry Pi's graphical desktop. 
