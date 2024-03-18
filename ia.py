import cv2
import mediapipe as mp
import utils
import exercices
import time

def lancer(séance):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Capture de la video depuis la caméra de l'ordi
    cap = cv2.VideoCapture(0)

    # Variable de comptage
    index_exercice = 0
    compteur = séance.exercices[index_exercice][1]
    stage = None
    pourcentage = 0
    mouvement = séance.exercices[index_exercice][0]

    # Message de réussite ou d'erreur
    message = {
        'type': None,
        'texte': ''
    }

    # Variable pour le compteur de la pause
    fin_pause = False

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Detection des points par l'IA
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            message['type'] = None
            
            try:
                # On extrait le squelette
                squelette = results.pose_landmarks.landmark

                if mouvement == exercices.HALTERE_GAUCHE or mouvement == exercices.HALTERE_DROIT:
                    # Récupère les coordonnées des articulations
                    if mouvement == exercices.HALTERE_GAUCHE:
                        epaule = [squelette[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, squelette[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        coude = [squelette[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, squelette[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                        poignet = [squelette[mp_pose.PoseLandmark.LEFT_WRIST.value].x, squelette[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    elif mouvement == exercices.HALTERE_DROIT:
                        epaule = [squelette[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, squelette[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        coude = [squelette[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, squelette[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                        poignet = [squelette[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, squelette[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    
                    # Première état
                    if stage == None:
                        stage = 'monter'
                    
                    # Calcul et visualisation de l'angle
                    angle = utils.calcul_angle(epaule, coude, poignet)
                    utils.marquer_angle(image, coude, angle)

                    # Logique de comptage
                    if angle > 160:
                        stage = 'monter'
                    if angle < 30 and stage == 'monter':
                        stage = 'descendre'
                        compteur -= 1

                    # On trouve le pourcentage du mouvement effectué
                    pourcentage = -0.77 * angle + 123.08
                elif mouvement == exercices.SQUAT:
                    if stage == None:
                        stage = 'descendre'

                    # Jambe gauche
                    if squelette[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility >= 0.7:
                        epaule = [squelette[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, squelette[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        hanche = [squelette[mp_pose.PoseLandmark.LEFT_HIP.value].x, squelette[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        genou = [squelette[mp_pose.PoseLandmark.LEFT_KNEE.value].x, squelette[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                        cheville = [squelette[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, squelette[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    # Jambe droite
                    elif squelette[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility >= 0.7:
                        epaule = [squelette[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, squelette[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        hanche = [squelette[mp_pose.PoseLandmark.RIGHT_HIP.value].x, squelette[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        genou = [squelette[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, squelette[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        cheville = [squelette[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, squelette[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    else:
                        message = {
                            'type': 'erreur',
                            'texte': 'PLACEZ VOUS DE PROFIL DEVANT LA CAMERA'
                        }
                        pourcentage = 0
                        raise
                    

                    
                    # Calcul de l'angle du genou
                    angle_genou = utils.calcul_angle(hanche, genou, cheville)
                    utils.marquer_angle(image, genou, angle_genou)

                    # On utilise l'angle avec une droite "perpendiculaire" à la hanche pour déterminer le penchement du dos
                    point_fictif = hanche.copy()
                    point_fictif[1] -= 0.2
                    angle_hanche = utils.calcul_angle(epaule, hanche, point_fictif)
                    if angle_hanche > 40:
                        message = {
                            'type': 'erreur',
                            'texte': 'REDRESSEZ VOTRE DOS'
                        }
                    
                    # Si le squat descend trop bas
                    if angle_genou < 70:
                        message = {
                            'type': 'erreur',
                            'texte': 'SQUAT TROP BAS'
                        }

                    if angle_genou <= 90:
                        stage = 'monter'
                    if angle_genou >= 170 and stage == 'monter':
                        stage = 'descendre'
                        compteur -= 1

                    # On trouve le pourcentage du mouvement effectué
                    pourcentage = -1.25 * angle_genou + 212.5
                elif mouvement == exercices.PAUSE:
                    if fin_pause == False:
                        longueur = compteur
                        fin_pause = time.time() + longueur

                    compteur = round(fin_pause - time.time())
                    
                    pourcentage = ((longueur - compteur) / longueur) * 100
                    
                    if compteur <= 0:
                        fin_pause = False

                    stage = 'pause'
                
                elif mouvement == exercices.FENTE_GAUCHE or mouvement == exercices.FENTE_DROIT:
                    if stage == None:
                        stage = 'descendre'
                    
                    if squelette[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility >= 0.7 and squelette[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility >= 0.7:
                        if mouvement == exercices.FENTE_GAUCHE:
                            hanche_avant = [squelette[mp_pose.PoseLandmark.LEFT_HIP.value].x, squelette[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                            genou_avant = [squelette[mp_pose.PoseLandmark.LEFT_KNEE.value].x, squelette[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                            cheville_avant = [squelette[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, squelette[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                        else:
                            hanche_avant = [squelette[mp_pose.PoseLandmark.RIGHT_HIP.value].x, squelette[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                            genou_avant = [squelette[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, squelette[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                            cheville_avant = [squelette[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, squelette[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        
                        # Calcul de l'angle du genou
                        angle_genou = utils.calcul_angle(hanche_avant, genou_avant, cheville_avant)
                        utils.marquer_angle(image, genou_avant, angle_genou)

                        if angle_genou <= 90:
                            stage = 'monter'
                        if angle_genou >= 170 and stage == 'monter':
                            stage = 'descendre'
                            compteur -= 1

                        # On trouve le pourcentage du mouvement effectué
                        pourcentage = -1.25 * angle_genou + 212.5
                    else:
                        message = {
                            'type': 'erreur',
                            'texte': 'PLACEZ VOUS DE PROFIL DEVANT LA CAMERA'
                        }
                        pourcentage = 0
                        raise

                # On arrondit le pourcentage
                if pourcentage > 100:
                    pourcentage = 100
                elif pourcentage < 0:
                    pourcentage = 0
                pourcentage = round(pourcentage)
            except:
                print('caca')
                pass
            
            # Rendu du squelette
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )
            
            # Affichage du compteur et du stage
            utils.dessiner_compteur(image, compteur, mouvement, stage)

            # Pourcentage
            utils.dessiner_bar_de_pourcentage(image, pourcentage)

            # Message de succès ou d'erreur
            utils.dessiner_message(image, message)

            # Presser q pour quitter
            cv2.putText(image, 'Pressez Q pour quitter', (20, image.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            # Affichage de la fenêtre
            cv2.imshow('Seance', image)

            # Lorsqu'on a fini l'exercices, on passe au prochain
            if compteur <= 0:
                index_exercice += 1
                # Si on a finit la séance on ferme la fenêtre
                if index_exercice == len(séance.exercices):
                    break
                else:
                    compteur = séance.exercices[index_exercice][1]
                    stage = None
                    pourcentage = 0
                    mouvement = séance.exercices[index_exercice][0]

            # On ferme la fenêtre lorsque la touche 'Q' est préssée
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'):
                break

        cap.release()
        cv2.destroyWindow('Seance')
