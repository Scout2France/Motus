##INITIALISATION

from tkinter import*
from random import*
import pygame
from PIL import Image, ImageTk
liste_mots = open("liste.txt").read().split("\n")

alphabet = "abcdefghijklmnopqrstuvwxyz"
pygame.mixer.init()

def play_gagnant(): ##initialisation de la fonction permettant de jouer la musique de victoire
    pygame.mixer.music.load("gagnant.mp3")
    pygame.mixer.music.play(loops=0)

def play_perdant(): ##initialisation de la fonction permettant de jouer la musique de défaite
    pygame.mixer.music.load("perdant.mp3")
    pygame.mixer.music.play(loops=0)

compteur = 0
positionLettre = 0

LeMot = choice(liste_mots)
dicoMot = {i: LeMot.count(i) for i in alphabet} ##Dictionnaire pour connaitre les occurences de chaque lettre de l'alphabet dans notre mot
reponseUser = LeMot[0]


fen = Tk()
image=Image.open('beccaro_content.jpg') ##Chargement de l'image de victoire
img=image.resize((600, 600))
Gigaimg=ImageTk.PhotoImage(img)



image1=Image.open('beccaro_pas_content.jpg') ##Chargement de l'image de défaite
img1=image1.resize((600, 600))
Gigaimg1=ImageTk.PhotoImage(img1)

cote = 600
coteCases = 500
debut = 50

coteCarre = coteCases/7

aire = Canvas(fen, width = 600, height = 600)
aire.pack()

##Creation de la grille
for hauteur in range(6):
    for largeur in range (7):
        aire.create_rectangle(debut+coteCarre*largeur, debut+coteCarre*hauteur, debut+coteCarre*largeur+coteCarre, debut+coteCarre*hauteur+coteCarre, fill='darkblue')


##On ecrit la première lettre du mot à trouver
aire.create_text(debut+coteCarre*positionLettre+coteCarre/2, debut+coteCarre*(compteur)+coteCarre/2, text = LeMot[0].capitalize(), font = ("Courier", 30), fill="white")
positionLettre = 1

def Verification(event): ##fonction comptant les lettres
    global compteur
    global LeMot
    global positionLettre
    global reponseUser
    dico = dicoMot.copy()
    reponse = reponseUser
    if reponse not in liste_mots: ##On vérifie que le mot existe dans la langue française
        return
    if len(reponse) != len(LeMot): ##On vérifie que le mot est de bonne longueur
        return
    compteur += 1
    nonobstant = 0
    oskur = [True for _ in range(7)]
    for i in range (len(reponse)):
        if reponse[i] == LeMot[i]: ## si les lettres correspondent au même endroit
            nonobstant += 1
            dico[reponse[i]] -= 1
            oskur[i] = False
            aire.create_rectangle(debut+coteCarre*i, debut+coteCarre*(compteur-1), debut+coteCarre*i+coteCarre, debut+coteCarre*(compteur-1)+coteCarre, fill='red') ##creation du rectangle rouge
    if nonobstant == len(reponse): ##Condition de victoire

        aire.create_image(300,300, image=Gigaimg)
        play_gagnant()
        return

    if compteur == 6: ##Condition de défaite
        aire.create_image(300,300, image=Gigaimg1)
        play_perdant()
        return
    for i in range (len(reponse)):
         if dico[reponse[i]] > 0 and oskur[i] == True: ##Creation des ronds jaunes
            aire.create_oval(debut+coteCarre*i, debut+coteCarre*(compteur-1), debut+coteCarre*i+coteCarre, debut+coteCarre*(compteur-1)+coteCarre, fill='yellow')
            dico[reponse[i]] -= 1
         aire.create_text(debut+coteCarre*i+coteCarre/2, debut+coteCarre*(compteur-1)+coteCarre/2, text = reponse[i].capitalize(), font = ("Courier", 30), fill="white")


    reponseUser = LeMot[0]
    positionLettre = 0
    aire.create_text(debut+coteCarre*positionLettre+coteCarre/2, debut+coteCarre*(compteur)+coteCarre/2, text = LeMot[0].capitalize(), font = ("Courier", 30), fill="white") ##Re création de la première letrre du mot pour une nouvelle ligne
    positionLettre = 1

fen.bind('<Return>', Verification) ##on assigne cette fonction à la touche Entrée

def rajoutLettre(event): ##fonction permettant d'ajouter une lettre
    global positionLettre
    global reponseUser
    if 1<= positionLettre <= len(LeMot)-1: ##Si on peut ajouter la lettre
        if 65 <= event.keycode <= 90: ##Si c'est une lettre
            aire.create_text(debut+coteCarre*positionLettre+coteCarre/2, debut+coteCarre*(compteur)+coteCarre/2, text = event.keysym.capitalize(), font = ("Courier", 30), fill="white") ##creation de la lettre dans la grille
            reponseUser += str(event.keysym) ##ajout de lettre a la reponse de l'utilisateur
            positionLettre += 1
fen.bind('<Any-KeyPress>', rajoutLettre) ##on assigne cette fonction à la presse d'une touche


def retirerLettre(event): ##fonction permettant de retier une lettre
    global positionLettre
    global reponseUser
    if 2<= positionLettre <= len(LeMot): ##Si nous pouvons retirer la lettre
        aire.create_rectangle(debut+coteCarre*(positionLettre-1), debut+coteCarre*(compteur), debut+coteCarre*(positionLettre-1)+coteCarre, debut+coteCarre*(compteur)+coteCarre, fill='darkblue') ##creation d'un rectangle bleu par dessus la lettre
        reponseUser = reponseUser[:-1] ##on enleve la lettre de la reponse de l'utilisateur
        positionLettre -= 1
fen.bind('<BackSpace>', retirerLettre) ##on assigne cette fonction a la touche effacer



fen.mainloop()