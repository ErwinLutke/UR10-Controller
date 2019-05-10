# UR10-Controller
An new interface has been developed for the UR in the repo: https://github.com/ErwinLutke/UR 
It can be used to build your application for the UR.
 

A small python program for controlling a Universal Robot with URScripting.

Written in Python 3.7 no extra modules needed.

The program is a small GUI with a few buttons.
With it you can connect to a hardcoded socket and start sending data over tcp/ip

Sending too many commands seems to overload the UR and freezes the positioning data on the robot's panel.
