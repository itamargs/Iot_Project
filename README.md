

<p align="center">
  <img src="https://mspalliance.com/wp-content/uploads/2017/03/IoT.png">
</p>


Our project is developed as part of the requirements for our B.Sc studying at [Azrieli College of Engineering, Jerusalem, Israel](https://www.jce.ac.il/).
The project is advisored by Dr. Guy Leshem, and created by [our team](https://github.com/itamargs/Iot_Project/wiki/Our-Team)


Our project deals with compressing and sending data between IoT devices to minimize the storage data without damaging it is rehabilitee or it is relevance.
The project will deal with the "flood" information problem as well as be suitable for diverse types of information.


Relevant Links:


 |Category|Status|
|---|---|
| Version Control System| [![git](https://img.shields.io/badge/Version%20Control-Git-green.svg)](https://git-scm.com/) & [![github](https://img.shields.io/badge/Version%20Control-Github-green.svg)](https://github.com/) |
| Issues | [![GitHub issues](https://img.shields.io/github/issues/meitarsh/m.s-aluminium-manager-app.svg?style=flat)](https://github.com/itamargs/Iot_Project/issues) |
| Project Management Board| [![here](https://img.shields.io/badge/Project%20Management%20Board-On%20demand-lightgrey.svg)](https://github.com/itamargs/Iot_Project/projects/1) |
| Documnetation | [![Inline docs](http://inch-ci.org/github/meitarsh/m.s-aluminium-manager-app.svg?branch=master)](https://github.com/itamargs/Iot_Project/wiki/Documents) |
| Diary |  [![link](https://img.shields.io/badge/Diary-On%20demand-blue.svg)](https://calendar.google.com/calendar/embed?src=e0luturcbaalb57knbt17hq83k%40group.calendar.google.com&ctz=Asia%2FJerusalem) |
| Releases |  [![release](http://github-release-version.herokuapp.com/github/meitarsh/m.s-aluminium-manager-app/release.svg?style=flat)](https://github.com/itamargs/Iot_Project/releases) |
| License | [![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/itamargs/Iot_Project/blob/master/LICENSE)|
---
*How To Use:*

On RasberyPi-Os (Should be the same or slightly different in other Linux distributions)

Install Python3 Packages on your device:
	
	pip3 install dill
	
	pip3 install firebase_admin
	
	pip3 install pydub
	
	pip3 install pyrebase
	
Install libav-tools for audio encoding:

	sudo apt-get install libav-tools
	
Run program:

	python3 device_[sensor name].py
Run master (server):

	python3 Master.py

Insert Files into input folder for compression- filesPool

Note: 
	microphone only support .WAV files
