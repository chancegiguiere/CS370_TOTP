CS 370 Project 3: TOTP with Google Authenticator
Chance Giguiere

1 - Extract the contents of the .tar folder to a directory.

2 - If needed, install the necesarry required libraries from requirements.txt
    (use "pip install -r requirements")

3 - Run the program with python3 using "python3 totp.py --[generate-qr || get-otp]"

In order to generate a secret.txt file as well as a qr code that can be scanned by Google Authenticator, run the program with --generate-qr
After this, run the program again with --get-otp in order to print the One Time Passwords to the screen.
The program will sleep for up to 30 seconds in order to synchronize with the codes produced by Google Authenticator. 

This program was tested on the OSU FLIP server using Python3 version 3.6.8
The QR codes were tested using Google Authenticator on an Android 12 smartphone, although there is no indication that they won't work on an Apple device.