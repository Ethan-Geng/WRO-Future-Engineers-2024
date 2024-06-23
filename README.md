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
* Carisma Puma Hybrid Rally RC Car 1/24 AWD ([Link](https://carisma-shop.com/products/gt24-m-sport-2022-puma-hybrid-rally1))
  * Equipped with a lightweight chassis, high traction tires, and effective friction dampeners, this RC car serves as a perfect base for our team to construct our self-driving car using. With the addition of the parking lot in this year's competition, we chose this 1/24th scale size as its dimensions allow us to effectively utilize back-in parking, as opposed to parallel parking. This not only saves time, but minimizes chances of error during our parking phase of Obstacle Challenge. 

* Raspberry Pi 4 Model B ([Link](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/))
  * We chose the Raspberry Pi to act as the brain of the entire car. The code on the board handles all computing aspects, including the image processing and control signals. It's 64-bit quad-core processor coupled with 8GB of Random Access Memory (RAM) ensures fast processing of our code. 

* Hiwonder Pi Expansion Board (N/A)
  * Compact and practical, the expansion board stacks on top of our Raspberry Pi board and is attached using the board's universal input/output pins. This expansion board allows for easy connections for our servo motor, brushless motor, and Pi fan. 

* SainSmart MIPI CSI Fisheye Camera Module ([Link](https://www.sainsmart.com/products/noir-wide-angle-fov160-5-megapixel-camera-module))
  * This CSI camera conveniently connects to our Raspberry Pi board's camera module port and offers a wide 160 degree viewing angle with great 5MP resolution, colour quality, and a high frame rate. This camera is responsible for detecting walls, obstacles, and lines. 

* Micro Servo Motor ([Link](https://ca.robotshop.com/products/hs-5055mg-metal-gear-micro-servo-motor?srsltid=AfmBOopv8Z7LoCVOEqe16w05ZV-R78dNmy7dappldIxZiQzCJroxcssFc2Y))
  * PLACEHOLDER
 
* Pi Fan ([Link](https://www.amazon.ca/GeeekPi-Raspberry-Radiator-Aluminum-Heatsinks/dp/B07C9C99RM/ref=asc_df_B07C9C99RM/?tag=googleshopc0c-20&linkCode=df0&hvadid=579070369590&hvpos=&hvnetw=g&hvrand=2167868380151199729&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9000759&hvtargid=pla-995264935599&psc=1&mcid=ad78a1c125c23c7088cb21e5dde53480))
  * PLACEHOLDER

* Furitek Micro Brushless Motor + ESC
  * PLACEHOLDER

* Gens ACE 1300mAh LiPo Battery ([Link](https://www.adrenalinehobby.com/products/gens-ace-g-tech-1300mah-2s-7-4v-25c-lipo-deans-plug?_pos=1&_sid=dde29d30b&_ss=r))
  * PLACEHOLDER




