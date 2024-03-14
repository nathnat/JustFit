from tkinter import *
import tkinter.ttk as ttk
import exercices

fenetre = Tk()  # on crée une unique fenêtre dont on modifiera l'affichage

prog = {}

def effacer_fenetre():
    for element in fenetre.winfo_children():  # récupère et parcours tous les éléments "accrochés" à cette fenêtre
        element.destroy()


def affichage_2():
    # même principe que affichage_1(): on nettoie d'abord notre fenêtre puis on ajoute tous nos éléments à cette fenetre
    effacer_fenetre()
   
    recapf = Frame(fenetre,bg='white')
    entreeNom = Frame(fenetre,bg='white')   
    label_title = Label(fenetre, text="Mon programme:", font=("Arial",40),bg="white",fg="black" ) #ajout du titre :
    label_title.pack()   
    entre = Entry(fenetre, font=('Arial',15), bg='#F5F5DC') #entree pour que l'ultilisateur tape son nom de programme
    entre.pack() 
    def getText():
        nom= entre.get()
        liste.config(text=nom)
        entre.delete(0, END)
        prog['nomProgramme'] = nom
        print(prog)
   
    liste = Label(fenetre,font=("Arial",15))
    liste.pack(padx=50)
    bouton=Button(fenetre, text="enregister le nom du programme:",font=('Arial',20),bg='black',fg="white", command=getText)
    bouton.pack(side=TOP,pady=25)
    texte="Récapitulatif de mon programme: \n"
    for cle in prog: 
        nom = prog[cle][0]
        nb= prog[cle][1]
        texte+= f"Exercice :{nom} {nb} répétitions \n"
    recap=Label(recapf, text=texte ,font=('Arial',25),bg="white",fg='black')#Afficher le recap du programme 
    recap.pack()
    
    recapf.pack(side=LEFT) 
    entreeNom.pack()
    btn = Button(text="Retour au menu", font=('Arial',25),bg="black",fg='white',command=affichage_1)
    #Ici plutot que de rappeler la fonction qui créer la page d'avant 
    #tu mets le nom de la fonction qui créer le menu et normalement ça marche 
    btn.pack(side=BOTTOM,fill=X)
    
    print(prog)



def affichage_1():
    global prog
    effacer_fenetre()  


    # listemenu = ['Sélectionner', 'Squat', 'Pompe', 'Jumping jack', 'Curl biceps', 'Abdo']
    
    # for i in range(len(listemenu)):
    #     titre = Frame()
    #     titre_exercice = Label(titre, text=f'Exercice {i + 1}', font=('Arial', 25))
    #     titre_exercice.pack()
    #     titre.pack()


        
    #     menu = ttk.Combobox(titre, values=listemenu, font=('Arial',16))
    #     menu.current(0)
    #     menu.pack()
    #     menu.bind("<<ComboboxSelected>>",action)
    #     l1 = Label(titre, text = "Nombre de répétition" , font=('Arial',13))
    #     a = Entry(titre)
    #     a.insert(0, 'username')


    # titre2=Frame()
    # titre_exercice2= Label (titre2, text='Exercice2', font=('Arial', 25))
    # titre_exercice2.pack()
    # titre2.pack()
    # def action(event):
    #     '''affiche l2'''
    #     select = menu2.get()
    #     l2.pack()
    #     b.pack()
    # menu2 = ttk.Combobox(titre2, values=listemenu, font=('Arial',16))
    # menu2.current(0)
    # menu2.pack()
    # menu2.bind("<<ComboboxSelected>>",action)
    # l2 = Label(titre2, text = "Nombre de répétition" , font=('Arial',13))
    # b= Entry(titre2)
        
    # titre3=Frame(fenetre)
    # titre_exercice3= Label (titre3, text='Exercice 3', font=('Arial', 25))
    # titre_exercice3.pack()
    # titre3.pack()
    # def action(event):
    #     '''affiche l3'''
    #     select = menu3.get()
    #     l3.pack()
    #     c.pack()
    # menu3 = ttk.Combobox(titre3, values=listemenu, font=('Arial',16))
    # menu3.current(0)
    # menu3.pack()
    # menu3.bind("<<ComboboxSelected>>",action)
    # l3 = Label(titre3, text = "Nombre de répétition" , font=('Arial',13))
    # c= Entry(titre3)
    
    # titre4=Frame(fenetre)
    # titre4.pack()
    # titre_exercice4= Label (titre4, text='Exercice 4', font=('Arial', 25) )
    # titre_exercice4.pack()
    # def action(event):
    #     '''affiche l4'''
    #     select = menu4.get()
    #     l4.pack()
    #     d.pack()
    # menu4 = ttk.Combobox(titre4, values=listemenu, font=('Arial',16))
    # menu4.current(0)
    # menu4.pack()
    # menu4.bind("<<ComboboxSelected>>",action)
    # l4 = Label( titre4, text = "Nombre de répétition" , font=('Arial',13))
    # d= Entry(titre4)
    
    # titre5=Frame(fenetre)
    # titre5.pack()
    # titre_exercice5= Label (titre5, text='Exercice 5', font=('Arial', 25))
    # titre_exercice5.pack()
    # def action(event):
    #     '''affiche l5'''
    #     select = menu5.get()
    #     l5.pack()
    #     e.pack()
    # menu5 = ttk.Combobox(titre5, values=listemenu, font=('Arial',16))
    # menu5.current(0)
    # menu5.pack()
    # menu5.bind("<<ComboboxSelected>>",action)
    # l5 = Label( titre5, text = "Nombre de répétition" , font=('Arial',13))
    # e= Entry(titre5)
        # PAS SUPPRIMER
    def sauvegarde():#pour garder en mémoire les paramètres des exos 
        prog['exercice 1']=(menu1.get(),a.get())
        # prog['exercice 2']=(menu2.get(),b.get())
        # prog['exercice 3']=(menu3.get(),c.get())
        # prog['exercice 4']=(menu4.get(),d.get()) 
        # prog['exercice 5']=(menu5.get(),e.get())
        
        affichage_2()#appel pour passer à la page suivante 
        
    btn = Button(text="Suivant",font=('Arial',25),bg="black",fg='white', command=sauvegarde)    
    btn.pack(side=BOTTOM,fill=X)

class ListeEntrées(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.nombre = 0
        self.liste_menu = ['Sélectionner', 'Squat', 'Pompe', 'Jumping jack', 'Curl biceps', 'Abdo']
        self.entrées = []

        Label(self, text='Choix de l\'exercice', font=('Arial', 18)).grid(row=0, column=0)
        Label(self, text='Quantité', font=('Arial', 18)).grid(row=0, column=1)

    def ajouter(self):
        self.nombre += 1
        self.entrées.append(Entrée(self, self.nombre))
    
    def extraire(self):
        for entrée in self.entrées:
            print(entrée.exercice, entrée.valeur_quantité)

class Entrée():
    def __init__(self, parent, index):
        liste_menu = exercices.TOUS

        self.index = index
        self.exercice = liste_menu[0]

        self.menu = ttk.Combobox(parent, values=liste_menu)
        self.menu.current(0)
        self.menu.bind('<<ComboboxSelected>>', self.on_select)
        self.menu.grid(row=self.index, column=0)
        
        self.label_quantité = Label(parent, text='secondes')
        self.label_quantité.grid(row=self.index, column=2)

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
        entrée_quantité = Entry(parent, textvariable=quantité, width=5)
        entrée_quantité.grid(row=self.index, column=1)
    
    def on_select(self, event):
        self.exercice = self.menu.get()
        if self.exercice == exercices.PAUSE:
            self.label_quantité.configure(text='secondes')
        else:
            self.label_quantité.configure(text='répétitions')
        


def fonction_principale():


    titre = StringVar(fenetre, 'Ma nouvelle séance')
    titre_entrée = Entry(fenetre, textvariable=titre, font=('Arial',20), justify='center')
    titre_entrée.pack(side='top')
    
    liste = ListeEntrées(fenetre)
    liste.ajouter()
    liste.pack()
    Button(fenetre, text='Ajouter un exercice', command=liste.ajouter).pack()
    
    def sauvegarder(c):
        liste.extraire()

    ajouter_au_menu = Label(fenetre, text='Ajouter au menu', cursor='hand2', font=('Arial', 25), fg='#fff', bg='#006c80', padx=10, pady=10)
    ajouter_au_menu.bind('<Button-1>', sauvegarder)
    ajouter_au_menu.pack(side='bottom')

    fenetre.mainloop()
    
fonction_principale()