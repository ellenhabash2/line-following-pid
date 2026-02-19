# Line Following with PID & Odometry

Robotics project implementing an autonomous LEGO NXT robot capable of stable line following using PID control, sensor feedback, and trajectory reconstruction.

## Overview

This project explores control systems and robotics navigation by comparing non-PID and PID-based controllers for accurate path tracking.

Key goals:

- Implement closed-loop PID steering
- Improve trajectory stability
- Record odometry data for offline analysis
- Evaluate performance tradeoffs between speed and accuracy

## Technologies

- NXC (Not eXactly C) for robot control
- Python for trajectory reconstruction
- Odometry logging
- PID control systems

## Features

- Differential drive robot
- Real-time sensor feedback
- Data logging to CSV
- Offline trajectory plotting

## Architecture

Robot → Sensor Input → PID Controller → Motor Output → CSV Logs → Python Analysis

## Results

The PID controller significantly improved path stability and reduced oscillations compared to the baseline controller.

## Repository Structure

robot_code/ – Embedded robot programs  
analysis/ – Python scripts for trajectory visualization  
media/ – Images and experiment results  
report/ – Full technical documentation  

## Author

Ellen Habash  
Final-Year Computer Science Student — Robotics & Software Engineering
