# SuperMileage RPi
The Raspberry Pi script for the SuperMileage car. Sends things such as speed and RPM to the HUD.

### About
- This is the raspberry pi script
- This sends data to the android app via TCP over ADB

### Requirements
- Python v3.0 or higher
- PyDev plugin for Eclipse (http://pydev.org/updates)
- ADB for RPi (http://forum.xda-developers.com/showthread.php?t=1924492, http://forum.xda-developers.com/attachment.php?attachmentid=1392336&d=1349930509)

### How to Clone
#### Installing the plugins
1. Install the PyDev plugin in eclipse: http://pydev.org/updates
2. Install EGit into eclipse: http://download.eclipse.org/egit/updates

#### Cloning the project
1. Create a new PyDev project with the name SM-RPi and all the default selections
2. Create a new file in the project and name it with your name
4. Right click on the project > Team > Share Project...
5. Click "Use or create repository in parent folder or project"
6. Click on the project and click Create Repository and click Finish
7. Right click on the project > Team > Commit...
8. Add a commit message and ONLY select the file with your name, then click Commit and Push
9. Click New Remote, name it master and put the URI as: https://github.com/MSOE-Supermileage/SM-RPi.git and click Finish
10. Click Next and it should give you an error: non-fast-forward, thats OK! Click Finish
11. Right click on the project > Team > Pull, it should successfully pull the current code from the repo
12. Now delete your file with your name and Commit and Push!
13. You are now all set up to begin pushing commits to the repo!