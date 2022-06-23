import cv2
import keyInputs as keyinput 
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        imageHeight, imageWidth, _ = image.shape
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        co = []
        tip = []
        pip = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.WRIST":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,normalizedLandmark.y,imageWidth, imageHeight)
                        try:
                            co.append(list(pixelCoordinatesLandmark))
                        except:
                            continue

                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.MIDDLE_FINGER_PIP":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,normalizedLandmark.y,imageWidth, imageHeight)
                        try:
                            pip.append(list(pixelCoordinatesLandmark))
                        except:
                            continue

                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.MIDDLE_FINGER_TIP":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,normalizedLandmark.y,imageWidth, imageHeight)
                        try:
                            tip.append(list(pixelCoordinatesLandmark))
                        except:
                            continue

        if len(co)==2 and len(tip)==2 and len(pip)==2:
            if co[0][0] < co[1][0] and tip[1][1] < pip[1][1] and tip[0][1] > pip[0][1]:
                print("1Accelerate")
                keyinput.release_key('l')
                keyinput.press_key('r')           

            elif co[1][0] < co[0][0] and tip[0][1] < pip[0][1] and tip[1][1] > pip[1][1]:
                print("2Accelerate")
                keyinput.release_key('l')
                keyinput.press_key('r')
                
            elif co[0][0] < co[1][0] and tip[0][1] < pip[0][1] and tip[1][1] > pip[1][1]:
                print("1Break")
                keyinput.release_key('r')
                keyinput.press_key('l')
                
            elif co[1][0] < co[0][0] and tip[1][1] < pip[1][1] and tip[0][1] > pip[0][1]:
                print("2Break")
                keyinput.release_key('r')
                keyinput.press_key('l')
                
            else:
                print("release")
                keyinput.release_key('r')
                keyinput.release_key('l')
  
        # cv2.imshow('Hands',cv2.flip(image, 1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
