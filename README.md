Documentation l Explorer Robotics l Team EAK
====
## Introduction
This repository contains the engineering process of Team EAK's self-driven vehicle's model participating in the WRO Future Engineers competition in the season 2024. Included in the repository are materials used, schematics, pictures, and software.

This part must be filled by participants with the technical clarifications about the code: which modules the code consists of, how they are related to the electromechanical components of the vehicle, and what is the process to build/compile/upload the code to the vehicle’s controllers.

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
* __Carisma Puma Hybrid Rally RC Car 1/24 AWD ([Link](https://carisma-shop.com/products/gt24-m-sport-2022-puma-hybrid-rally1))__
  * Equipped with a lightweight chassis, high traction tires, and effective friction dampeners, this RC car serves as a perfect base for our team to construct our self-driving car using. With the addition of the parking lot in this year's competition, we chose this 1/24th scale size as its dimensions allow us to effectively utilize back-in parking, as opposed to parallel parking. This not only saves time, but minimizes chances of error during our parking phase of Obstacle Challenge. 

* __Raspberry Pi 4 Model B ([Link](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/))__
  * We chose the Raspberry Pi to act as the brain of the entire car. The code on the board handles all computing aspects, including the image processing and control signals. It's 64-bit quad-core processor coupled with 8GB of Random Access Memory (RAM) ensures fast processing of our code. 

* __Hiwonder Pi Expansion Board (N/A)__
  * Compact and practical, the expansion board stacks on top of our Raspberry Pi board and is attached using the board's universal input/output pins. This expansion board allows for easy connections for our servo motor, brushless motor, and Pi fan. 

* __SainSmart MIPI CSI Fisheye Camera Module ([Link](https://www.sainsmart.com/products/noir-wide-angle-fov160-5-megapixel-camera-module))__
  * This CSI camera conveniently connects to our Raspberry Pi board's camera module port and offers a wide 160 degree viewing angle with great 5MP resolution, colour quality, and a high frame rate. This camera is responsible for detecting walls, obstacles, and lines. 

* __Micro Servo Motor ([Link](https://ca.robotshop.com/products/hs-5055mg-metal-gear-micro-servo-motor?srsltid=AfmBOopv8Z7LoCVOEqe16w05ZV-R78dNmy7dappldIxZiQzCJroxcssFc2Y))__
  * This programmable micro servo motor allows our team to precisely control the steering angle of our car. It's compact and lightweight design ensures that it can fit perfectly within our car chassis. 
 
* __GeeekPi Pi Fan ([Link](https://www.amazon.ca/GeeekPi-Raspberry-Radiator-Aluminum-Heatsinks/dp/B07C9C99RM/ref=asc_df_B07C9C99RM/?tag=googleshopc0c-20&linkCode=df0&hvadid=579070369590&hvpos=&hvnetw=g&hvrand=2167868380151199729&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9000759&hvtargid=pla-995264935599&psc=1&mcid=ad78a1c125c23c7088cb21e5dde53480))__
  * We decided to include this efficient fan to effectively cool and dissipate heat from our Raspberry Pi, which will help to mitigate thermal throttling and thereby improve performance under a heavy processing load. Our team found that the addition of this Pi fan can cool the Raspberry Pi up to 30 degrees celsius. 

* __Furitek Komodo Micro Brushless Motor + ESC ([Link](https://furitek.com/products/furitek-stinger-brushless-power-system-for-scx24))__
  * The Furitek brushless motor works with the spur gear in our car chassis to drive the wheels. It has a lightweight but powerful design that provides smooth driving with great speed, high torque, and zero cogging. We chose to use a brushless motor because of the increased efficiency due to the eliminaton of brushes which create friction, greater reliablilty, and overall improved performance compared to a brushed motor. 

* __Gens ACE 1300mAh LiPo Battery ([Link](https://www.adrenalinehobby.com/products/gens-ace-g-tech-1300mah-2s-7-4v-25c-lipo-deans-plug?_pos=1&_sid=dde29d30b&_ss=r))__
  * This LiPo batery provides power for the entire circuit/car system, including the servo motor, Raspberry Pi, and brushless motor. It's high 1300mAh capacity allows our car and program to run for an extended period of time, which helps during testing and improves reliability during competition.

## Hardware Assembly and Design Process
1. Our first step in our build process was to open up and strip down the __Carisma Puma Hybrid Rally RC Car 1/24 AWD__ to its chassis and remove all the components we did not need. This included taking out the built-in servo motor, the brushed motor, the battery connection, and remote control circuit board. 
2. Now with a base chassis, we were able to install our own components including the __Micro Servo Motor__ and __Furitek Komodo Micro Brushless Motor + ESC__. Replacing the RC car's original servo motor and brushed motor was a key step in our process as it allowed us to use programmable and higher quality components. We made physical modifications to the chassis by cutting the plastic body using an exacto knife to ensure that our new components would fit seamlessly.
3. With our components installed, our team moved onto creating our main platform for the car on which the __Raspberry Pi 4 Model B__, __Hiwonder Pi Expansion Board__, and __GeeekPi Pi Fan__ will sit on, as well as a tower that will house the __SainSmart MIPI CSI Fisheye Camera Module__. After brainstorming methods to create the platform and tower, we ultimately decided upon 3D printing it using PETG filament, thus ensuring a lightweight and durable product.
   * The main platform is a flat rectangle with a raised border on 2 sides and 4 mounting holes near each corner. It sits on top of our car chassis and is secured by fitting the mounting holes onto rods that stick up vertically on the car's chassis. The __Raspberry Pi 4 Model B__ is attached to the platform using the board's mounting holes and 4 small cylinders on the platform. On the left side of the platform, there is a rectangular box which the __GeeekPi Pi Fan__ can snap into.
   * The camera tower sits on the back of the platform and is secured through screws on the bottom of the platform. We then screwed in the __SainSmart MIPI CSI Fisheye Camera Module__ to the tower, which guarantees a tight fit.
4. Our final step was to connect all the wiring from the components to the Raspberry Pi and __Gens ACE 1300mAh LiPo Battery__, as well as wire management using electrical tape to make certain that no loose wiring would cause problems for our car.

## Code Overview
PLACEHOLDER 

## Building/Compiling/Uploading Process
All code for open challenge and obstacle challenge was built using Python. Our programs are coded and saved directly onto our Raspberry Pi. 

