from tkinter import Tk, Button, Label, Frame, Toplevel, PhotoImage, Canvas
from PIL import ImageTk, Image
from tkscrolledframe import ScrolledFrame
import platform
import exercices
import ia
import utils

class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind('<Configure>', self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
        self.scale('all', 0, 0, wscale, hscale)

def open_popup(titre):
    top = Toplevel(root)
    w = 500
    h = 200
    top.geometry(f'{w}x{h}')
    frame = Frame(top, pady=25)
    top.title('JustFit - Fin de séance')
    Label(frame, text='Bravo vous venez de finir', font=('Arial 18')).pack(side='top')

    def close():
        top.destroy()
        top.update()

    label = Label(frame, text=titre,  font=('Arial 23 bold'), pady=25)
    button = Button(frame, text='FERMER', command=close)

    frame.pack(expand=True, fill='both')
    label.pack()
    button.pack(side='bottom')
    utils.center(top)

class Séance():
    def __init__(self, titre: str, exercices: list):
        self.titre = titre
        self.exercices = exercices

    def lancer_seance(self):
        ia.lancer(self)
        open_popup(self.titre)

def créer_liste_séances(object, séances):

    nombre_ligne = len(séances) // 3

    for i in range(nombre_ligne):
        object.grid_rowconfigure(i, weight=1)
    
    object.grid_columnconfigure(0, weight=1)
    object.grid_columnconfigure(1, weight=1)
    object.grid_columnconfigure(2, weight=1)

    for index_ligne in range(nombre_ligne + 1):
        for index_colonne in range(3):
            if len(séances) == 0:
                break
            séance = séances.pop()

            # On construit l'affichage de l'entrainement
            cadre = Frame(object, pady=20, padx=20, borderwidth=1, relief='solid')

            cadre.config(width=100, height=100)
            cadre.grid(column=index_colonne, row=index_ligne, sticky='nswe', padx=10, pady=10)
            cadre.grid_propagate(False)
            
            titre = Label(cadre, text=séance.titre, font=('Arial', 30, 'bold'))
            titre.pack()

            for exercice in séance.exercices:
                contenu = Label(cadre,
                    text=f'• {exercice[0]} {exercice[1]}',
                    font=('Arial', 23),
                    anchor='w',
                    justify='left',
                    wraplength=root.winfo_screenwidth() / 3 - 65
                    )
                
                if exercice[0] == exercices.PAUSE:
                    contenu['text'] += ' s'
                else:
                    contenu['text'] += ' rep'
                
                contenu.pack(fill='x')
            
            Button(cadre,
                text='Lancer cette séance',
                font=('Arial', 25),
                pady=10,
                command=séance.lancer_seance
                ).pack(side='bottom')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('JustFit')
    
        # On lance l'app en plein écran fenetré
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.width}x{self.height}')

        # On centre la fenêtre sur l'écran
        utils.center(self.root)
        
        # Couleur de fond de l'app
        self.background_color = '#0097B2'
        self.root.configure(background=self.background_color)

        # Police de l'application
        self.font = ('Roboto', 18)

    def page_de_lancement(self):
        page = Frame(self.root)

        canvas = ResizingCanvas(page, bg='#0097b2', width=self.width, height=self.height, bd=0, highlightthickness=0, relief='ridge')
        canvas.pack(expand='yes', fill='both')

        # On récupère les coordonées du centre de l'écran    
        center_x = (canvas.winfo_reqwidth() // 2) 
        center_y = (canvas.winfo_reqheight() // 2.75) 

        # On place le logo au centre
        logo = PhotoImage(file='ressources/logo-JustFit.png', master=page)
        canvas.create_image(center_x, center_y, anchor='center', image=logo)
        self.logo = logo

        # Utilisez create_window pour placer le bouton dans le canvas
        
        button = Label(page, text='Cliquez pour commencer', cursor='hand2', font=('Arial', 25), fg='#fff', bg='#006c80', padx=10, pady=10)
        button.bind('<Button-1>', lambda x: self.transition_selection(page))

        buttonStart_window = canvas.create_window(center_x, center_y + 350, anchor='center', window=button)

        # On place le gif de l'homme
        frame_count1 = 31
        homme_frames = [PhotoImage(file='ressources/homme_muscu.gif', format='gif -index %i' % i, master=page) for i in range(frame_count1)]
        gif_label1 = canvas.create_image(center_x / 3, center_y, anchor='center', image=homme_frames[0])
        def update(ind):
            frame = homme_frames[ind]
            ind += 1
            if ind == frame_count1:
                ind = 0
            canvas.itemconfig(gif_label1, image=frame)
            canvas.tag_raise(gif_label1)
            page.after(120, update, ind)

        # On place le gif de la femme
        frame_count2 = 12
        femme_frames = [PhotoImage(file='ressources/femme_muscu.gif', format='gif -index %i' % i, master=page) for i in range(frame_count2)]
        gif_label2 = canvas.create_image(canvas.winfo_reqwidth() - (center_x / 3), center_y, anchor='center', image=femme_frames[0])
        def update2(ind):
            frame = femme_frames[ind]
            ind += 1
            if ind == frame_count2:
                ind = 0
            canvas.itemconfig(gif_label2, image=frame)
            canvas.tag_raise(gif_label2)
            page.after(180, update2, ind)


        # GIF du cercle qui tourne autour du logo
        frame_count3 = 20
        cercle_frames = [PhotoImage(file='ressources/cercle.gif', format='gif -index %i' % i, master=page) for i in range(frame_count3)]
        gif_label3 = canvas.create_image(center_x, center_y, anchor='center', image=cercle_frames[0])
        def update3(ind):
            frame3 = cercle_frames[ind]
            ind += 1
            if ind == frame_count3:
                ind = 0
            canvas.itemconfig(gif_label3, image=frame3)
            canvas.tag_raise(gif_label3) 
            page.after(100, update3, ind)

        page.after(0, update, 0)
        page.after(0, update2, 0)
        page.after(0, update3, 0)

        page.pack(expand='yes')
    
    def selection_seances(self):
        page = Frame().pack()

        # On place le titre dans une frame
        titre = Label(page, text='Sélectionnez votre entraînement', pady=20, font=('Helvetica', 25))
        titre.pack(side='top')

        test = [
            Séance('Jambe jeanne 🦵🔥', [
                (exercices.HALTERE_GAUCHE, 5),
                (exercices.PAUSE, 10),
                (exercices.HALTERE_DROIT, 5),
                (exercices.PAUSE, 10),
                (exercices.HALTERE_DROIT, 5),
            ]),
            Séance('Squat', [
                (exercices.SQUAT, 10),
                (exercices.PAUSE, 20),
                (exercices.HALTERE_GAUCHE, 10)
            ]),
            Séance('On sait pas trop', [
                (exercices.SQUAT, 10),
                (exercices.PAUSE, 20),
                (exercices.HALTERE_GAUCHE, 10)
            ]),
            Séance('FENTE', [
                (exercices.FENTE_GAUCHE, 3),
                (exercices.PAUSE, 10),
                (exercices.FENTE_DROIT, 3),
                (exercices.HALTERE_GAUCHE, 10)
            ]),
            Séance('PAUSE', [
                (exercices.PAUSE, 5)
            ])
        ]

        # On crée la Frame scrollable
        sf = ScrolledFrame(page, scrollbars='vertical')
        sf.pack(side='bottom', expand='yes', fill='both')

        # Scroll avec la roue de la souris et des flèches
        sf.bind_arrow_keys(root)
        sf.bind_scroll_wheel(root)

        # Create a frame within the ScrolledFrame
        liste_séance = sf.display_widget(Frame)
        créer_liste_séances(liste_séance, test)
        # liste_séance['padx'] = root.winfo_screenwidth() / 100

    def transition_selection(self, page):
        page.destroy()
        self.root.title('JustFit - Sélection des séances')
        self.selection_seances()
    

        
root = Tk()
app = App(root)
app.page_de_lancement()

root.mainloop()