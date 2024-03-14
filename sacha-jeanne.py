from tkinter import *
import tkinter.ttk as ttk

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
    entre = Entry(fenetre,font=('Arial',15),bg='#F5F5DC') #entree pour que l'ultilisateur tape son nom de programme
    entre.pack() 
    def getText():
        nom= entre.get()
        liste.config(text=nom)
        entre.delete(0, END)
        prog['nomProgramme']=nom
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
    
    listemenu = ['Sélectionner','Squat','Pompe','Jumping jack','Curl biceps','Abdo']
    titre1 = Frame()
    titre_exercice1= Label (titre1, text='Exercice 1', font=('Arial', 25))
    titre_exercice1.pack()
    titre1.pack()
    def action(event):
       '''affiche l1'''
       select = menu1.get()
       l1.pack()
       a.pack()
    menu1 = ttk.Combobox(titre1, values=listemenu, font=('Arial',16))
    menu1.current(0)
    menu1.pack()
    menu1.bind("<<ComboboxSelected>>",action)
    l1 = Label(titre1, text = "Nombre de répétition" , font=('Arial',13))
    a= Entry(titre1)

    titre2=Frame()
    titre_exercice2= Label (titre2, text='Exercice2', font=('Arial', 25))
    titre_exercice2.pack()
    titre2.pack()
    def action(event):
        '''affiche l2'''
        select = menu2.get()
        l2.pack()
        b.pack()
    menu2 = ttk.Combobox(titre2, values=listemenu, font=('Arial',16))
    menu2.current(0)
    menu2.pack()
    menu2.bind("<<ComboboxSelected>>",action)
    l2 = Label(titre2, text = "Nombre de répétition" , font=('Arial',13))
    b= Entry(titre2)
        
    titre3=Frame(fenetre)
    titre_exercice3= Label (titre3, text='Exercice 3', font=('Arial', 25))
    titre_exercice3.pack()
    titre3.pack()
    def action(event):
        '''affiche l3'''
        select = menu3.get()
        l3.pack()
        c.pack()
    menu3 = ttk.Combobox(titre3, values=listemenu, font=('Arial',16))
    menu3.current(0)
    menu3.pack()
    menu3.bind("<<ComboboxSelected>>",action)
    l3 = Label(titre3, text = "Nombre de répétition" , font=('Arial',13))
    c= Entry(titre3)
    
    titre4=Frame(fenetre)
    titre4.pack()
    titre_exercice4= Label (titre4, text='Exercice 4', font=('Arial', 25) )
    titre_exercice4.pack()
    def action(event):
        '''affiche l4'''
        select = menu4.get()
        l4.pack()
        d.pack()
    menu4 = ttk.Combobox(titre4, values=listemenu, font=('Arial',16))
    menu4.current(0)
    menu4.pack()
    menu4.bind("<<ComboboxSelected>>",action)
    l4 = Label( titre4, text = "Nombre de répétition" , font=('Arial',13))
    d= Entry(titre4)
    
    titre5=Frame(fenetre)
    titre5.pack()
    titre_exercice5= Label (titre5, text='Exercice 5', font=('Arial', 25))
    titre_exercice5.pack()
    def action(event):
        '''affiche l5'''
        select = menu5.get()
        l5.pack()
        e.pack()
    menu5 = ttk.Combobox(titre5, values=listemenu, font=('Arial',16))
    menu5.current(0)
    menu5.pack()
    menu5.bind("<<ComboboxSelected>>",action)
    l5 = Label( titre5, text = "Nombre de répétition" , font=('Arial',13))
    e= Entry(titre5)
        # PAS SUPPRIMER
    def sauvegarde():#pour garder en mémoire les paramètres des exos 
        prog['exercice 1']=(menu1.get(),a.get())
        prog['exercice 2']=(menu2.get(),b.get())
        prog['exercice 3']=(menu3.get(),c.get())
        prog['exercice 4']=(menu4.get(),d.get()) 
        prog['exercice 5']=(menu5.get(),e.get())
        
        affichage_2()#appel pour passer à la page suivante 
        
    btn = Button(text="Suivant",font=('Arial',25),bg="black",fg='white', command=sauvegarde)    
    btn.pack(side=BOTTOM,fill=X)

 
def fonction_principale():
    # Je crée une fonction principale qui paramètre ce qui ne changera pas dans mon programme et qui lance la boucle
    # d'affichage Tkinter (fenetre.mainloop)
    fenetre.title("Mon programme:")
    fenetre.geometry("1080x1080")
    fenetre.config(background="white")
    affichage_1()  # J'appelle la fonction qui me crée le premier affichage que je veux afficher lors du démarrage
    fenetre.mainloop()
    
 
    
fonction_principale()