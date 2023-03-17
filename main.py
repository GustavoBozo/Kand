import cv2
from cvzone.HandTrackingModule import HandDetector
import os

width, height = 480, 480
folderPath = 'slides'

cap = cv2.VideoCapture(0)

cap.set(3, width)
cap.set(4, height)


imagesPath = sorted(os.listdir(folderPath))
imageNumber = 0
buttonPressed = False
buttonCounter = 0
buttonDelay = 10

ws, hs = int(240*1),int(240*1)

detector = HandDetector(maxHands=2)

while True:
    sucess, img = cap.read()
    # img = cv2.flip(img, 1)


    pathFullImage = os.path.join(folderPath, imagesPath[imageNumber])
    currentImage = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        print(fingers)
           
        if fingers == [0,1,0,0,0]:
            if imageNumber > 0:
                buttonPressed = True

                imageNumber -= 1

        if fingers == [0,0,0,0,1]:
            if imageNumber < len(imagesPath) -1:
                buttonPressed = True
                imageNumber += 1  

    if buttonPressed:
        buttonPressed += 1
        if buttonPressed > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    
    smallImg = cv2.resize(img, (ws, hs))
    h, w, _ = currentImage.shape

    currentImage[0:hs, w - ws:w] = smallImg  


    cv2.imshow("Teste", img)
    cv2.imshow("slide", currentImage)

    key = cv2.waitKey(1)