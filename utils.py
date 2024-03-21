import cv2
import numpy as np
import unicodedata
import exercices

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def dessiner_bar_de_pourcentage(image, pourcentage) -> None:
    couleur = (51, 51, 255)
    if 30 < pourcentage <= 60:
        couleur = (0, 165, 255)
    elif 60 <= pourcentage <= 90:
        couleur = (0, 255, 255)
    elif 90 < pourcentage <= 100:
        couleur = (0, 255, 0)

    largeur =  image.shape[1]

    cv2.rectangle(image, (largeur - 160, 100), (largeur - 85, 650), couleur, 3)
    cv2.rectangle(image, (largeur - 160, 650 - int(pourcentage * 5.5)), (largeur - 85, 650), couleur, cv2.FILLED)
    cv2.putText(image, f'{str(pourcentage)}%', (largeur - 160, 690), cv2.FONT_HERSHEY_SIMPLEX, 1.3, couleur, 2, cv2.LINE_AA)


def dessiner_message(image, message) -> None:
    if message['type'] == None:
        return

    couleur = (0,255,0)
    if message['type'] == 'erreur':
        couleur = (51,51,255)

    # Centrage du texte
    font = cv2.FONT_HERSHEY_SIMPLEX
    texte_taille = cv2.getTextSize(message['texte'], font, 1, 2)[0]
    texteX = (image.shape[1] - texte_taille[0]) // 2

    # Ajout du texte sur l'image
    cv2.rectangle(image, (texteX - 10, 50 + 10), (texteX + texte_taille[0] + 10, 50 - texte_taille[1] - 10), couleur, cv2.FILLED)
    cv2.putText(image, message['texte'], (texteX, 50), font, 1, (255,255,255), 2)

def marquer_angle(image, articulation, angle) -> None:
    cv2.putText(image, str(round(angle)), tuple(np.multiply(articulation, [image.shape[1], image.shape[0]]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)

def calcul_angle(a, b, c) -> float:
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

def dessiner_compteur(image, compteur, mouvement, stage):
    couleur = (245,117,16)

    if stage == None:
        return

    # On affiche un compteur spécial pour les secondes des pauses
    if mouvement != exercices.PAUSE:
        texte = strip_accents(f'Il vous reste {compteur} {mouvement}')
        # Centrage du texte
        font = cv2.FONT_HERSHEY_SIMPLEX
        texte_taille = cv2.getTextSize(texte, font, 1, 2)[0]
        texteX = (image.shape[1] - texte_taille[0]) // 2

        # Ajout du texte sur l'image
        cv2.rectangle(image, (texteX - 10, 50 + 10), (texteX + texte_taille[0] + 10, 50 - texte_taille[1] - 10), couleur, cv2.FILLED)
        cv2.putText(image, texte, (texteX, 50), font, 1, (255,255,255), 2)
    else:
        texte = f'{compteur}s'
        # Centrage du texte
        font = cv2.FONT_HERSHEY_SIMPLEX
        texte_taille = cv2.getTextSize(texte, font, 3, 2)[0]
        texteX = (image.shape[1] - texte_taille[0]) // 2

        # Ajout du texte sur l'image
        cv2.rectangle(image, (texteX - 10, 250 + 10), (texteX + texte_taille[0] + 10, 250 - texte_taille[1] - 10), couleur, cv2.FILLED)
        cv2.putText(image, texte, (texteX, 250), font, 3, (255,255,255), 2)

    # Affichage état du mouvement
    texte = stage.upper()
    # Centrage du texte
    font = cv2.FONT_HERSHEY_SIMPLEX
    texte_taille = cv2.getTextSize(texte, font, 1, 2)[0]
    texteX = (image.shape[1] - texte_taille[0]) // 2
    cv2.rectangle(image, (texteX - 10, 100 + 10), (texteX + texte_taille[0] + 10, 100 - texte_taille[1] - 10), couleur, cv2.FILLED)
    cv2.putText(image, texte, (texteX, 100), font, 1, (255,255,255), 2)

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()