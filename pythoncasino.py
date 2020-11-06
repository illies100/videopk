"""
Pythoncasino projet OUAOTMANE Elias
"""
# import des modules que nous utilisons.
from collections import defaultdict
from random import randrange
import sys
import time
from tkinter import Tk, Button, Label, LabelFrame, PhotoImage
from tkinter import messagebox, DISABLED, NORMAL, Menu, E, W
from tkinter import Toplevel, INSERT, scrolledtext
import webbrowser


class Pok:
    """variables."""
    btn1_held = None
    btn2_held = None
    btn3_held = None
    btn4_held = None
    btn5_held = None

    card_one = 'blank'
    card_two = 'blank'
    card_three = 'blank'
    card_four = 'blank'
    card_five = 'blank'

    high_score = 0

    hold_btn1 = None
    hold_btn2 = None
    hold_btn3 = None
    hold_btn4 = None
    hold_btn5 = None

    no_card_holding = True

    plyr_credits = 100
    plyr_winnings = 0
    plyr_stake = 1

    ranks = ''
    stake_btn = None
    suits = ''
    winning_hand = ''

# Interface.
root = Tk()
root.title('Vidéo Poker')
root.resizable(False, False)

# Fenetre.
pay_table_frame = LabelFrame(root)
pay_table_frame.grid(row=0, column=0)

# Chargement et affichage.
pay_table_lbl = Label(pay_table_frame)
PHOTO = PhotoImage(file=r'cartes/pay-table-bg-386x200.png')
pay_table_lbl.config(image=PHOTO)
pay_table_lbl.grid(row=0, column=0, padx=2, pady=2)
pay_table_lbl.photo = PHOTO

# Fenetre des messages.
msg_frame = LabelFrame(root)
msg_frame.grid(row=1, column=0)

# Message de départ.
msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                text='Choisissez une mise puis cliquez sur Deal')
msg_lbl.grid(row=1, column=0)

# Fenetre pour les images.
cards_frame = LabelFrame(root)
cards_frame.grid(row=2, column=0)

# Fenetre banque.
bank_frame = LabelFrame(root)
bank_frame.grid(row=4, column=0, sticky=W+E)

# Score le plus haut.
high_score_frame = LabelFrame(root)
high_score_frame.grid(row=5, column=0, sticky=W+E)

result_frame = LabelFrame(root)
result_frame.grid(row=6, column=0, sticky=W+E)

def logo_result_frame():
    """ Resultat."""
    result_frame_lbl = Label(result_frame)
    PHOTO = PhotoImage(file=r'cartes/result-frame.png')
    result_frame_lbl.config(image=PHOTO)
    result_frame_lbl.grid(row=6, column=0, padx=2, pady=2)
    result_frame_lbl.photo = PHOTO

# Appel du logo principal.
logo_result_frame()

def show_winner_logo():
    """Afficher l’image de la main gagnante."""
    result_frame_lbl = Label(result_frame)
    PHOTO = PhotoImage(file=r'cartes/result-frame-winner.png')
    result_frame_lbl.config(image=PHOTO)
    result_frame_lbl.grid(row=6, column=0, padx=2, pady=2)
    result_frame_lbl.photo = PHOTO

def show_loser_logo():
    """Afficher l'image de la main perdante."""
    result_frame_lbl = Label(result_frame)
    PHOTO = PhotoImage(file=r'cartes/result-frame-loser.png')
    result_frame_lbl.config(image=PHOTO)
    result_frame_lbl.grid(row=6, column=0, padx=2, pady=2)
    result_frame_lbl.photo = PHOTO

def load_high_score():
    """Charger la variable de score élevé à partir du fichier
       et la stocker dans Pok.high_score."""
    with open(r'cartes/high-score.txt', 'r') as contents:
        SAVED_HIGH_SCORE = contents.read()
        if SAVED_HIGH_SCORE > '':
            Pok.high_score = int(SAVED_HIGH_SCORE)

# Chargement du score le plus haut.
load_high_score()

def game_over():
    """rejouer la partie oui ou non."""
    quest = messagebox.askyesno('Video Poker',
                                'game over, plus de thunes.\n'
                                'Voulez-vous jouer une nouvelle partie?')

    if quest:
        # Nouvelle partie.
        hand = [Pok.card_one, Pok.card_two, Pok.card_three,
                Pok.card_four, Pok.card_five]
        hand_value = check_hand(hand)
        Pok.plyr_credits = 100
        Pok.plyr_winnings = 0
        # ne pas mettre à jour.
        high_score_lbl = Label(high_score_frame, font=('Helvetica', 10, 'bold'),
                               text='Top Score: €'+str(Pok.high_score)+'     ')
        high_score_lbl.grid(row=4, column=0)

        start_game()
        return

    else:
        # Fermeture du programme
        root.destroy()
        sys.exit()
