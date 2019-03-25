# UR10-Controller
A small python program for controlling a Universal Robot with URScripting.

Written in Python 3.7 no extra modules needed.

The program is a small GUI with a few buttons.
With it you can connect to a hardcoded socket and start sending data over tcp/ip

Sending too many commands seems to overload the UR and freezes the positioning data on the robot's panel.
