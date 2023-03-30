import cv2
from cvzone.HandTrackingModule import HandDetector
import os
import numpy as np
from AppOpener import open

width, height = 1280, 720
folderPath = 'slides'

cap = cv2.VideoCapture(0)

cap.set(3, width)
cap.set(4, height)


imagesPath = sorted(os.listdir(folderPath))
imageNumber = 0
buttonPressed = False
buttonCounter = 0
buttonDelay = 10

ws, hs = int(120*1),int(213*1)


detector = HandDetector(maxHands=2)
active = True
Showimage = True
while active:
    sucess, img = cap.read()
    # img = cv2.flip(img, 1)

    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, imagesPath[imageNumber])
    currentImage = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img, flipType=True)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        h, w, _ = currentImage.shape

        lmList = hand['lmList']
        xVal = int(np.interp(lmList[8][0], [width // 2, w], [0, width]))

        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))

        indexFinger = xVal, yVal
           
        if fingers == [0,1,0,0,0]:
            if imageNumber > 0:
                buttonPressed = True

                imageNumber -= 1

        if fingers == [0,0,0,0,1]:
            if imageNumber < len(imagesPath) -1:
                buttonPressed = True
                imageNumber += 1  

        
        if fingers == [1,1,0,0,1]:
            active = False
        
        if fingers == [0,1,1,0,0]:
            open("chrome")
        

    if buttonPressed:
        buttonPressed += 1
        if buttonPressed > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    
    # smallImg = cv2.resize(img, (ws, hs))
    
    # currentImage[0:hs, w - ws:w] = smallImg  


    cv2.imshow("Teste", img)
    cv2.imshow("slide", currentImage)

    key = cv2.waitKey(1)