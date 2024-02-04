import cv2
import mediapipe as mp
import numpy as np
import utilitaires

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calcul_angle(a, b, c) -> int:
    '''Hyp: a est le point de gauche, b est le point du milieu et c le point de droite
    Retourne la mesure de l'angle entre a, b et c en degrée'''
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0 
stage = None
pourcentage = 0

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
            # Calculate angle
            angle = calcul_angle(shoulder, elbow, wrist)

            # Visualize angle
            cv2.putText(image, str(round(angle)), tuple(np.multiply(elbow, [image.shape[1], image.shape[0]]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Curl counter logic
            if angle > 160:
                stage = 'Monter'
            if angle < 30 and stage == 'Monter':
                stage = 'Descendre'
                counter += 1

            # On trouve le pourcentage du mouvement effectué
            if stage == 'Monter':
                pourcentage = -0.77 * angle + 123.08
            else:
                pourcentage = 0.77 * angle - 23.08

            if pourcentage > 100:
                pourcentage = 100
            elif pourcentage < 0:
                pourcentage = 0
            
            pourcentage = round(pourcentage)
        except:
            pass
        
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Rep data
        cv2.putText(image, 'Nombre de rep', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, stage, (60,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        # Pourcentage
        utilitaires.dessiner_bar_de_pourcentage(image, pourcentage)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        # Affichage de la fenêtre
        cv2.imshow('Resultat', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()