import cv2

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
    cv2.putText(image, message['texte'], (texteX, 50), font, 1, couleur, 2)