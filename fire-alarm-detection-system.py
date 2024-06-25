# Importing neccessary libraries

import cv2
import numpy as np
import smtplib
import playsound
import threading
import os

# initialize status flags and counters
Alarm_Status=False
Email_Status=False
Fire_Reported=0

# Fuction to play the alarm soun in one loop

def play_alarm_sound_function():
    while Alarm_Status: # add a condition to 
        playsound.playsound('alarm-sound.mp3', True)
        
        
# Fuction to send an email notification
def send_email_function():
    recipitenEmail='siddhanbhattarai@ismt.edu.np'
    recipitenEmail=recipitenEmail.lower()
    
    try:
        # setup an SMTP server and send the email
        
        server=smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("chaudharyparmila75@gmail.com", "") 
        server.sendmail("chaudharyparmila75@gmail.com", recipitenEmail, "Subject:Fire Accident Warning\n\nWarning: A fire has been ")
        server.quit()
    except Exception as e:
        print(f"Failed to send email:{e}")
        
    
# functiion to relese resources on exit

def cleanup():
    global Alarm_Status
    Alarm_Status=False
    cv2.destroyAllWindows()
    video.release()
    
# main code 
try:
    video=cv2.VideoCapture("videoplayback.mp4")
    
    while True:
        grabbed, frame=video.read()
        if not grabbed:
            break
        
        
        # resize the frame for consistent processing
        frame=cv2.resize(frame, (960, 540))
        
        # Apply Gaussian blur and convert to HSV color space
        blur=cv2.GaussianBlur(frame, (21, 21), 0)
        hsv=cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        
        
        # Define color range for detecting fire(red/orange)
        lower=[18, 50, 50]
        upper=[35, 255, 255]
        lower=np.array(lower, dtype='uint8')
        upper=np.array(upper, dtype='uint8')
        
        # apply the mask to detect the fire color range
        mask=cv2.inRange(hsv, lower, upper)
        
        # apply the mask to original frame
        output=cv2.bitwise_and(frame, frame, mask=mask)
        
        # count the number of non-zero pixel in the mask
        no_red=cv2.CountNonZero(mask)
        
        # if a significant number of red pixel are detected 
        if int(no_red)>15000:
            Fire_Reported += 1
            
            # Dispaly the processed out frame
            cv2.imshow('output', output)
            
        # check if a fire has been reported
        if Fire_Reported >=1:
            # start playoing the sound 
            if not Alarm_Status:
                Alarm_Status=True
                threading.Thread(target=play_alarm_sound_function, daemon=True)
                
            if not Email_Status:
                Email_Status=True
                threading.Thread(target=play_alarm_sound_function, daemon=True)
                
                
                
        # check if the 'q' key is pressed to exit the loop
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            # Release resources and close windows            
            cleanup()
            
except KeyboardInterrupt:
    cleanup()
    print("Program interrrupted and exited cleanly.")
except Exception as e:
    cleanup()
    print(f"An error occured: {e}")
            
        