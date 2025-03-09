# Rubik's Cube Solver

This Rubik's cube Solver is currently capable of solving the following cubes:

- 4x4

Larger Cubes are possible, but still need improvement.<br>
For the Machine to work properly you will need one 3D Printed Part.

Download it right here: <a href="https://www.tinkercad.com/things/d0IxvU92B2h?sharecode=Jh8IfUun2b3GN0zdoSJT3zGORd8c5wm-otYE1JK7ZZI">EV3 Cube Holder</a> 

## Showcase

<a href="https://youtube.com/watch?v=n9ZGZy9EfsQ">4x4 Solver Demonstration</a>

## Solving the Cube

Huge thanks to dwalton76 for providing his very efficient <a href="https://github.com/dwalton76/rubiks-cube-NxNxN-solver">NxN Solver.</a>

# Setup

## Preparation

- Flash Raspberry Pi OS Lite

![image](https://github.com/JohnGrubba/EV3-NxN-Cuber/assets/63007476/90b90f96-c6ed-4c61-96c8-0f0a16919649)
![image](https://github.com/JohnGrubba/EV3-NxN-Cuber/assets/63007476/472d5559-bda6-4ab7-ac01-c3f6f472740d)

- Clone this repository
```sh
git clone https://github.com/JohnGrubba/EV3-NxN-Cuber
```

- Install all Dependencies
- Make sure you are on root
```sh
sudo pip install -r requirements.txt
```

- Fix OpenCV Error (Import Error)
```
sudo apt install libgl1
```

- Fix Permissions Error (Run with sudo)
To allow Python access to the USB Connection you need to run the program with sudo. And this is why you should also install all dependencies with sudo
```
sudo python3 main.py
```
You can change the cube size in the main.py file via the Constant at the top. This will eventually be changed to a command line arg.
