import json
from tkinter.ttk import Entry, Combobox
from tkscrolledframe import ScrolledFrame
from tkinter import Tk, Button, Label, Frame, Toplevel, PhotoImage, Canvas, StringVar

import ia
import utils
import exercices

class ListeEntrées(Frame):
    def __init__(self, parent, titre_entrée):
        Frame.__init__(self, parent, padx=10, pady=10, bg=parent['bg'])
        
        self.nombre = 0
        self.entrées = []
        self.titre_entrée = titre_entrée

        Label(self, text='Choix de l\'exercice', font=('Arial', 16), bg=parent['bg']).grid(row=0, column=0, padx=(0, 80))
        Label(self, text='Quantité', font=('Arial', 16), bg=parent['bg']).grid(row=0, column=1)

        self.pack()

        sf = ScrolledFrame(parent, scrollbars='vertical', borderwidth=0, highlightthickness=0, width=535, height=470)
        sf.pack()

        # Scroll avec la roue de la souris et des flèches
        sf.bind_scroll_wheel(root)
        self.conteneur = sf.display_widget(Frame, fit_width=True)

        Button(parent, text='Ajouter un exercice', command=self.ajouter).pack()
        self.ajouter()

    def ajouter(self):
        self.nombre += 1
        self.entrées.append(Entrée(self.conteneur, self.nombre))

    def extraire(self):
        return Séance(self.titre_entrée.get(), [(entrée.exercice, entrée.valeur_quantité) for entrée in self.entrées]) 

class Entrée():
    def __init__(self, parent, index):
        liste_menu = exercices.TOUS
        
        self.index = index
        self.exercice = liste_menu[0]

        font = 'Arial 15 roman normal'

        self.menu = Combobox(parent, font=font, state='readonly', values=liste_menu, width=28)
        self.menu.current(0)
        self.menu.bind('<<ComboboxSelected>>', self.on_select)
        self.menu.grid(row=self.index, column=0, pady=3, padx=5)

        self.label_quantité = Label(parent, font=font, text='secondes')
        self.label_quantité.grid(row=self.index, column=2, padx=5)

        # On filtre pour que la valeur de la quantité reste un int
        self.valeur_quantité = 0
        def filtrer(*args):
            try:
                if quantité.get().strip() == '':
                    self.valeur_quantité = 0
                    quantité.set(self.valeur_quantité)
                else:
                    self.valeur_quantité = int(quantité.get())
            except:
                quantité.set(self.valeur_quantité)

        quantité = StringVar(parent, 0)
        quantité.trace_add('write', filtrer)
        entrée_quantité = Entry(parent, font=font, textvariable=quantité, width=8, justify='left')
        entrée_quantité.grid(row=self.index, column=1)
    
    def on_select(self, event):
        self.exercice = self.menu.get()
        if self.exercice == exercices.PAUSE:
            self.label_quantité.configure(text='secondes')
        else:
            self.label_quantité.configure(text='répétitions')

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

class Séance:
    def __init__(self, titre: str, exercices: list):
        self.titre = titre
        self.exercices = exercices

    def lancer_seance(self, _):
        ia.lancer(self)
        open_popup(self.titre)

def créer_liste_séances(object, séances):

    nombre_ligne = len(séances) // 3

    for i in range(nombre_ligne):
        object.grid_rowconfigure(i, weight=1)
    
    object.grid_columnconfigure(0, weight=1)
    object.grid_columnconfigure(1, weight=1)
    object.grid_columnconfigure(2, weight=1)

    i = 0
    for index_ligne in range(nombre_ligne + 1):
        for index_colonne in range(3):
            if i >= len(séances):
                break
            séance = séances[i]

            # On construit l'affichage de l'entrainement
            cadre = Frame(object, pady=20, padx=20, borderwidth=1, relief='solid')

            cadre.config(width=100, height=100)
            cadre.grid(column=index_colonne, row=index_ligne, sticky='nswe', padx=10, pady=10)
            cadre.grid_propagate(False)
            
            titre = Label(cadre, text=séance.titre, font=('Arial', 30, 'bold'), pady=8)
            titre.pack()

            for j in range(len(séance.exercices)):
                exercice = séance.exercices[j]
                contenu = Label(cadre,
                    text=f'• {exercice[0]} {exercice[1]}',
                    font=('Arial', 20),
                    anchor='w',
                    justify='left',
                    wraplength=root.winfo_screenwidth() / 3 - 65
                    )

                if exercice[0] == exercices.PAUSE:
                    contenu['text'] += ' s'
                else:
                    contenu['text'] += ' rep'
                
                # On place une petite marge entre le dernier exercices et le bouton
                if i == len(séance.exercices) - 1:
                    contenu.pack(fill='x', pady=(0,20))
                else:
                    contenu.pack(fill='x')
            
            lancer_bouton = Label(cadre, text='Lancer cette séance', cursor='hand2', font=('Arial', 19), fg='#fff', bg='#006c80', padx=10, pady=10)
            lancer_bouton.bind('<Button-1>', séance.lancer_seance)
            lancer_bouton.pack(side='bottom')
            
            i += 1

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('JustFit')
    
        # On lance l'app en plein écran fenetré
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.width}x{self.height - 30}')

        # On centre la fenêtre sur l'écran
        utils.center(self.root)
        
        # Couleur de fond de l'app
        self.background_color = '#52D1DC'
        self.second_color = '#5F4BB6'
        self.root.configure(background=self.background_color)

        # Police de l'application
        self.font = ('Roboto', 18)

        # On ouvre les séances enregistrés précédemment par l'utilisateur
        self.save_file = 'séances.json'
        self.séances = self.ouvrir_sauvegarde()

    def page_de_lancement(self):
        page = Frame(self.root)

        canvas = ResizingCanvas(page, bg=self.background_color, width=self.width, height=self.height, bd=0, highlightthickness=0, relief='ridge')
        canvas.pack(expand='yes', fill='both')

        # On récupère les coordonées du centre de l'écran    
        center_x = (canvas.winfo_reqwidth() // 2) 
        center_y = (canvas.winfo_reqheight() // 2.75) 

        # On place le logo au centre
        logo = PhotoImage(file='ressources/logo-JustFit.png', master=page)
        canvas.create_image(center_x, center_y, anchor='center', image=logo)
        self.logo = logo

        # Utilisez create_window pour placer le bouton dans le canvas
        
        button = Label(page, text='Cliquez pour commencer', cursor='hand2', font=('Arial', 25), fg='#fff', bg=self.second_color, padx=20, pady=10)
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
        page = Frame(bg=self.background_color)
        page.pack(expand='yes', fill='both')

        # On place le titre dans une frame
        header_conteneur = Frame(page, bg=self.background_color)
        titre = Label(header_conteneur, text='Sélectionnez votre entraînement ou ', pady=20, padx=10, font=('Arial', 25), bg=self.background_color)
        titre.pack(side='left')

        bouton_créer = Label(header_conteneur, text='Créer une séance', cursor='hand2', font=('Arial', 20), fg='#fff', bg=self.second_color, padx=10, pady=10)
        bouton_créer.bind('<Button-1>', lambda x: self.transition_création_séance(page))
        bouton_créer.pack(side='right')

        header_conteneur.pack(side='top')

        # On crée la Frame scrollable
        sf = ScrolledFrame(page, scrollbars='vertical', bg=self.background_color)
        sf.pack(side='bottom', expand='yes', fill='both')

        # Scroll avec la roue de la souris et des flèches
        sf.bind_scroll_wheel(root)

        # Create a frame within the ScrolledFrame
        liste_séance = sf.display_widget(Frame, fit_width=True)
        liste_séance['bg'] = self.background_color
        créer_liste_séances(liste_séance, self.séances)

    def transition_selection(self, page):
        page.destroy()
        self.root.title('JustFit - Sélection des séances')
        self.selection_seances()
    
    def creation_séance(self):
        page = Frame(self.root, bg=self.background_color, pady=20, padx=30)
        page.pack(expand='yes', fill='both')

        # Le titre modifiable de la séance
        titre_entrée = Entry(page, font=('Arial',20), justify='center')
        titre_entrée.insert(0, 'Ma nouvelle séance')
        titre_entrée.pack(side='top')

        liste = ListeEntrées(page, titre_entrée)
        def ajouter(_):
            self.séances.append(liste.extraire())
            self.sauvegarder_séances()
            self.transition_selection(page)

        ajouter_au_menu = Label(page, text='Ajouter au menu', cursor='hand2', font=('Arial', 25), fg='#fff', bg=self.second_color, padx=10, pady=10)
        ajouter_au_menu.bind('<Button-1>', ajouter)
        ajouter_au_menu.pack(side='bottom')

        page.pack(expand='yes')

    def transition_création_séance(self, page):
        page.destroy()
        self.root.title('JustFit - Création d\'une séance')
        self.creation_séance()

    def sauvegarder_séances(self):
        '''Sauvegarde les séances de l'utilisateur dans un fichier JSON'''
        output = []

        for séance in self.séances:
            output.append({
                'titre': séance.titre,
                'exercices': séance.exercices
            })
        with open(self.save_file, 'w') as file:
            json.dump(output, file, indent=4)
        
    def ouvrir_sauvegarde(self) -> [Séance]:
        '''Renvoie la liste des séances depuis le fichier de sauvegarde JSON'''
        file = open(self.save_file)
        data = json.load(file)
        
        output = []
        for séance in data:
            output.append(Séance(séance['titre'], séance['exercices']))
        return output

root = Tk()
app = App(root)
app.page_de_lancement()

root.mainloop()